import sys
import sqlite3
import json
from pathlib import Path
import pydicom
import datetime
import DICOMTransit.LORIS.API
from tqdm import tqdm

def initialize_database(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # Create the table Anonymized_Patients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Anonymized_Patients (
            MRN INTEGER PRIMARY KEY,
            CNBPID TEXT,
            StudyDate TEXT,
            Folder TEXT,
            StudyID TEXT,
            SeriesID TEXT
        )
    ''')
    
    connection.commit()
    connection.close()

def patient_exists_in_db(db_path, patient_id):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT CNBPID, StudyID, StudyDate, SeriesID, Folder FROM Anonymized_Patients WHERE MRN=?", (patient_id,))
    result = cursor.fetchone()
    connection.close()
    return result

def insert_patient_record(db_path, mrn, cnbpid, study_id, study_date, series_id, folder):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Anonymized_Patients (MRN, CNBPID, StudyID, StudyDate, SeriesID, Folder)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (mrn, cnbpid, json.dumps([study_id]), json.dumps([study_date]), json.dumps([series_id]), json.dumps([folder])))
    connection.commit()
    connection.close()

def update_patient_record(db_path, mrn, new_study_id, new_study_date, new_series_id, new_folder):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    # Fetch the existing patient record
    cursor.execute("SELECT StudyID, StudyDate, SeriesID, Folder FROM Anonymized_Patients WHERE MRN=?", (mrn,))
    result = cursor.fetchone()
    
    if result:
        study_id_list = json.loads(result[0]) if result[0] else []
        study_date_list = json.loads(result[1]) if result[1] else []
        series_id_list = json.loads(result[2]) if result[2] else []
        folder_list = json.loads(result[3]) if result[3] else []

        # Add new values if they aren't already present
        if new_study_id not in study_id_list:
            study_id_list.append(new_study_id)
        if new_study_date not in study_date_list:
            study_date_list.append(new_study_date)
        if new_series_id not in series_id_list:
            series_id_list.append(new_series_id)
        if new_folder not in folder_list:
            folder_list.append(new_folder)

        # Update the patient record with new lists
        cursor.execute('''
            UPDATE Anonymized_Patients
            SET StudyID=?, StudyDate=?, SeriesID=?, Folder=?
            WHERE MRN=?
        ''', (json.dumps(study_id_list), json.dumps(study_date_list), json.dumps(series_id_list), json.dumps(folder_list), mrn))
        
        connection.commit()
    connection.close()

def anonymize_dicom_global(global_folder, db_path):
    """
    Anonymization function that anonymizes DICOM files at a given directory with generated IDs from LORIS.
    :param global_folder: Path to the main folder containing patient subfolders and DICOM files
    :param db_path: Path to the SQLite database for logging
    """
    # Checks if global folder path exists
    if global_folder != "" and global_folder is not None:
        global_folder = Path(global_folder)
        if not global_folder.exists() or not global_folder.is_dir():
            print("\nError: Global folder path does not exist or is invalid.\n")
            return
    else:
        print("Error: You must enter a valid global folder path to proceed.\n")
        return

    # Dictionary to store the mapping of patient IDs to CNBPIDs
    patient_id_mapping = {}

    # Iterate through subfolders in the global folder
    for patient_folder in global_folder.iterdir():
        if patient_folder.is_dir():
            # Iterate through session subfolders (S1, S2, etc.)
            for session_folder in patient_folder.iterdir():
                if session_folder.is_dir():
                    # Anonymize DICOM files in the session folder
                    anonymize_dicom_session(session_folder, patient_id_mapping, db_path)

    print("Global Anonymization Complete!\n")

def anonymize_dicom_session(session_folder, patient_id_mapping, db_path):
    try:
        # Makes a list of all .dcm files in the session folder
        files = [str(file) for file in session_folder.rglob("*.dcm")]

        if not files:
            print(f"\nError: No DICOM files found in {session_folder}.\n")
            return

        # Extract values from the first DICOM file
        first_dcm_file = pydicom.dcmread(files[0])
        patient_id = first_dcm_file.PatientID
        study_id = first_dcm_file.StudyInstanceUID
        study_date = first_dcm_file.StudyDate
        series_id = first_dcm_file.SeriesInstanceUID

        # Check if patient ID has been encountered before
        if patient_id not in patient_id_mapping:
            # Format birth date to '%Y-%m-%d' for LORIS API
            birth_date = first_dcm_file.PatientBirthDate
            if birth_date:
                birth_date = datetime.datetime.strptime(birth_date, '%Y%m%d').strftime('%Y-%m-%d')
            # Mapping for DICOM PatientSex codes to LORIS API expected values
            gender_mapping = {'M': 'Male', 'F': 'Female'}
            mapped_patient_sex = gender_mapping.get(first_dcm_file.PatientSex, 'Unknown')

            # Generate unique patient IDs using the LORIS API
            success, _, PSCID = DICOMTransit.LORIS.API.create_candidate(
                "loris", birth_date, mapped_patient_sex
            )
            if success:
                cnbpid = PSCID
            else:
                print(f"\nError: Failed to generate unique ID for patient {patient_id}. Skipping...\n")
                return

            # Store the mapping of patient ID to CNBPID
            patient_id_mapping[patient_id] = cnbpid

        else:
            # Retrieve CNBPID from the mapping
            cnbpid = patient_id_mapping[patient_id]

        # Anonymize DICOM files with the generated IDs and additional fields
        print(f"\nAnonymizing DICOM files in {session_folder}:")
        with tqdm(total=len(files)) as progress_bar:
            for file_path in files:
                dicom_file = pydicom.dcmread(file_path)
                dicom_file.PatientID = cnbpid
                dicom_file.PatientBirthDate = ''
                dicom_file.PatientName = ''
                dicom_file.StudyDate = ''
                dicom_file.SeriesDate = ''
                dicom_file.AcquisitionDate = ''
                dicom_file.ContentDate = ''
                dicom_file.AccessionNumber = ''
                dicom_file.ReferringPhysicianName = ''
                dicom_file.InstitutionName = ''
                dicom_file.StationName = ''
                dicom_file.StudyID = ''
                dicom_file.ProtocolName = ''
                dicom_file.save_as(file_path)
                progress_bar.update(1)
        
        # Check if the patient already exists in the database
        folder_name = session_folder.parent.name
        if patient_exists_in_db(db_path, patient_id):
            update_patient_record(db_path, patient_id, study_id, study_date, series_id, folder_name)
        else:
            insert_patient_record(db_path, patient_id, cnbpid, study_id, study_date, series_id, folder_name)

        print(f"\nAnonymization of session {session_folder.name} complete!\n")

    except Exception as e:
        print(f"Error during anonymization of session {session_folder}: {e}")

if __name__ == '__main__':
    # Path to the logging database
    db_path = '/home/jhilpatel/DICOMTransit/SQL/LoggingDB.sqlite'
    
    # Initialize the database
    initialize_database(db_path)
    
    # Checks if arguments are provided when script is deployed
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        print("\nDICOM Anonymization: \n")
        # Asks user for folder path
        folder_path = input("Enter the folder path containing DICOM files: \n").strip() or None

    if folder_path:
        anonymize_dicom_global(folder_path, db_path)
    else:
        print("Error: No folder path provided. Exiting...")
