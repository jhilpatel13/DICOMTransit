import datetime
import pydicom
import DICOMTransit.DICOM.anonymize
from pathlib import Path

def anonymize_dicom(folder_path, new_ID):
    """
    Anonymization function that anonymizes DICOM files (Patient Name, ID and Birthday) at a given directory wtih given ID
    More fields to anonymize can be added in this function: DICOMTransit.DICOM.anonymize.DICOM_anonymize.save_as()
    :param folder_path:
    :param new_ID:
    """
    #Checks if folder path exists
    if folder_path  != "" and folder_path is not None:
        folder_path = Path(folder_path)
        if not folder_path.exists() or not folder_path.is_dir():
            print("\nError: Folder path does not exist or is invalid.\n")
            return
    else:
        print("Error: You must enter a valid folder path to proceed.\n")
        return

    #Makes a list of all .dcm files at file path by searching through all subdirectories 
    files = [str(file) for file in folder_path.rglob("*.dcm")]
    
    #Checks if files list is valid
    if not files:
        print("\nError: No files found, make sure the folder path is correct and that it contains .dcm files.\n")
        return 
    
    #Gets confirmation from user to proceed with anonymization
    confirmation = input(f"\nAre you sure you want to anonymize all DICOM files in {folder_path} ?\nThis action cannot be undone! (Enter Yes/No): \n")
    
    #Anonymizes the files with provided ID
    if confirmation.lower() == "yes" or confirmation.lower() == "y":
        print("\nAnonymizing files...\n")
        DICOMTransit.DICOM.anonymize.DICOM_anonymize.filelist(files, new_ID)
        
        #Creates log directory if none existant
        log_directory = Path("Anonymization_Logs")
        log_directory.mkdir(exist_ok=True)
        
        #Creates log file with each DICOM files modified from folder path and saves it at log directory
        print(f"\nCreating log file...\n")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        log_file_path = log_directory / f"{current_time}_{folder_path.stem}_log.txt" 
        with open (log_file_path, "a") as log_file:
            log_file.write(f"""DICOM Anonymization Log
-----------------------------------------------------------------------------------------------
This log file contains the path to  all fow level function used to retrieve elements from DICOM object that has already been loaded and return a LIST of matching element. ACCEPT PARTIAL MATCHiles that were modified during the anonymization.
Each file listed here has their Patient Name and Patient ID anonymized to : {new_ID}
-----------------------------------------------------------------------------------------------

Anonymization Attempt Timestamp: {current_time}

Changed PatientName to: {new_ID}
Changed PatientID to: {new_ID}
Changed PatientBirthDate to: <undefined>

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
    
    