import datetime
import pydicom
import DICOMTransit.DICOM.anonymize
import DICOMTransit.DICOM.API
from pathlib import Path

def anonymize_dicom():

    #Asks user for folder path
    folder_path = input("Enter the folder path containing DICOM files: \n")

    #Checks if folder path exists
    folder_path = Path(folder_path)
    if not folder_path.exists():
        print("Error: Folder path does not exist.")
        return
    
    #Makes a list of all .dcm files at file path by searching through all subdirectories 
    files = [str(file) for file in folder_path.rglob("*.dcm")]
    
    #Checks if files list is valid
    if not files:
        print("Error: No files found, make sure the folder path is correct and that it contains .dcm files.")
        return 
    
    #Asks user for new ID for Patient Name and Patient ID
    new_ID = input("Enter the new ID for Patient Name and Patient ID: \n")
    
    #Anonymizes the files with provided ID
    DICOMTransit.DICOM.anonymize.DICOM_anonymize.filelist(files, new_ID)
    
    #Creates log directory if none existant
    log_directory = Path("Anonymization_Logs")
    log_directory.mkdir(exist_ok=True)
    
    #Creates log file with each DICOM files modified from folder path and saves it at log directory
    print(f"\nCreating log file...\n")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log_file_path = log_directory / f"{current_time}_{folder_path.stem}_log.txt" 
    with open (log_file_path, "a") as log_file:
        log_file.write(f"Anonymization Timestamp: {current_time}\n\n")
        for file_path in folder_path.rglob("*.dcm"):
            try:
                read = pydicom.dcmread(file_path)
                log_file.write(f"Anonymization Log for file: {file_path}\n")
                log_file.write(f"   Patient Name: {read.PatientName}\n")
                log_file.write(f"   Patient ID: {read.PatientID}\n")
            except Exception as e:
                log_file.write(f"Error processing DICOM file: {file_path}: {e}\n")
                print(f"Error: Failed to read DICOM file {file_path}: {e}\n")

    print(f"Log file saved to {log_file_path}\n")
    print("Anonymization Complete!\n")
