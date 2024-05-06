import pydicom
from pathlib import Path
import datetime
import DICOMTransit.LORIS.API
from tqdm import tqdm

def anonymize_dicom(folder_path):
    """
    Anonymization function that anonymizes DICOM files (Patient Name, ID, Sex, and Birthday) at a given directory with generated IDs from LORIS.
    :param folder_path: Path to the folder containing DICOM files
    """
    # Checks if folder path exists
    if folder_path != "" and folder_path is not None:
        folder_path = Path(folder_path)
        if not folder_path.exists() or not folder_path.is_dir():
            print("\nError: Folder path does not exist or is invalid.\n")
            return
    else:
        print("Error: You must enter a valid folder path to proceed.\n")
        return

    # Makes a list of all .dcm files at file path by searching through all subdirectories
    files = [str(file) for file in folder_path.rglob("*.dcm")]

    # Checks if files list is valid
    if not files:
        print("\nError: No files found, make sure the folder path is correct and that it contains .dcm files.\n")
        return

    # Gets confirmation from user to proceed with anonymization
    confirmation = input(f"\nAre you sure you want to anonymize all DICOM files in {folder_path} ?\nThis action cannot be undone! (Enter Yes/No): \n")

    # Anonymizes the patient IDs with provided ID
    if confirmation.lower() == "yes" or confirmation.lower() == "y":
        print("\nAnonymizing patient IDs and additional fields...\n")

        # Extract patient IDs and birth dates from DICOM files
        patient_info = {}
        for file_path in files:
            if file_path.endswith('.dcm'):
                dicom_file = pydicom.dcmread(file_path)
                patient_id = dicom_file.PatientID
                patient_birth_date = dicom_file.PatientBirthDate
                patient_info.setdefault(patient_id, []).append((file_path, patient_birth_date))

        # Generate unique patient IDs using the LORIS API
        unique_patient_ids = {}
        for patient_id, file_info_list in patient_info.items():
            first_file_path, first_birth_date = file_info_list[0]
            if first_birth_date:
                parsed_patient_birth_date = str(datetime.datetime.strptime(first_birth_date, '%Y%m%d').date())
                patient_sex = dicom_file.PatientSex
                gender_mapping = {'M': 'Male', 'F': 'Female'}
                mapped_patient_sex = gender_mapping.get(patient_sex, 'Unknown')

                # Call LORIS API to generate unique ID
                success, DCCID, PSCID = DICOMTransit.LORIS.API.create_candidate(
                    "loris", parsed_patient_birth_date, mapped_patient_sex 
                )

                # Store the unique ID for all files associated with the patient
                for file_path, _ in file_info_list:
                    unique_patient_ids[file_path] = (PSCID, first_birth_date)
            else:
                # If birth date is empty, store a placeholder value for patient ID and keep the birth date
                for file_path, _ in file_info_list:
                    unique_patient_ids[file_path] = ("Unknown_Patient_ID", first_birth_date)

        # Anonymize DICOM files with the generated IDs and additional fields
        print("\nAnonymizing DICOM files:")
        with tqdm(total=len(unique_patient_ids)) as pbar:
            for file_path, (anonymized_patient_id, _) in unique_patient_ids.items():
                dicom_file = pydicom.dcmread(file_path)
                dicom_file.PatientID = anonymized_patient_id
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
                pbar.update(1)
        
        # Create log directory if none existent
        log_directory = Path("Anonymization_Logs")
        log_directory.mkdir(exist_ok=True)

        # Create log file with each DICOM files modified from folder path and save it at log directory
        print(f"\nCreating log file...\n")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        log_file_path = log_directory / f"{current_time}_{folder_path.stem}_log.txt"
        with open(log_file_path, "a") as log_file:
            log_file.write(f"""DICOM Anonymization Log
----------------------------------------------------------------------------------------------------
This log file contains the path to all files that were modified during the anonymization process.
----------------------------------------------------------------------------------------------------

Anonymization Attempt Timestamp: {current_time}

Anonymized PatientName
Anonymized PatientID
Anonymized PatientBirthDate
Anonymized StudyDate
Anonymized SeriesDate
Anonymized AcquisitionDate
Anonymized ContentDate
Anonymized AccessionNumber
Anonymized ReferringPhysicianName
Anonymized InstitutionName
Anonymized StationName
Anonymized StudyID
Anonymized ProtocolName

Files modified:
""")
            log_file_path_txt = ""
            for file_path in files:
                try:
                    log_file_path_txt += f"\n{file_path}"

                except Exception as e:
                    log_file.write(f"\nError processing DICOM file: {file_path}: {e}\n")
                    print(f"\nError: Failed to read DICOM file {file_path}: {e}\n")
            log_file.write(log_file_path_txt)

        print(f"Log file created and saved to {log_file_path}\n")
        print("Anonymization Complete!\n")

    else:
        print("\nStopping Anonymization...\n")
