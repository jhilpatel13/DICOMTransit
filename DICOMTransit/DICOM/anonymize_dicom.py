import datetime
import pydicom
import DICOMTransit.DICOM.anonymize
from pathlib import Path

def anonymize_dicom():
    print("\nDICOM Anonymization: \n")

    #Asks user for folder path
    folder_path = input("Enter the folder path containing DICOM files: \n")

    #Checks if folder path exists
    if not folder_path  == "":
        folder_path = Path(folder_path)
        if not folder_path.exists() or not folder_path.is_dir():
            print("\nError: Folder path does not exist or is invalid.\n")
            return
    else:
        print("\nError: You must enter a valid folder path to proceed.\n")
        return

    #Makes a list of all .dcm files at file path by searching through all subdirectories 
    files = [str(file) for file in folder_path.rglob("*.dcm")]
    
    #Checks if files list is valid
    if not files:
        print("\nError: No files found, make sure the folder path is correct and that it contains .dcm files.\n")
        return 
    
    #Asks user for new ID for Patient Name and Patient ID
    new_ID = input("\nEnter the new ID for Patient Name and Patient ID: \n")
    
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
            log_file.write("DICOM Anonymization Log\n")
            log_file.write("-----------------------------------------------------------------------------------------------\n")
            log_file.write("This log file contains information about all files that were modified during the anonymization.\n")
            log_file.write("Each entry includes current details about the anonymized DICOM files.\n")
            log_file.write("-----------------------------------------------------------------------------------------------\n")
            log_file.write(f"\nAnonymization Attempt Timestamp: {current_time}\n\n")
            for file_path in folder_path.rglob("*.dcm"):
                try:
                    read = pydicom.dcmread(file_path)
                    log_file.write(f"File modified: {file_path}\n")
                    log_file.write(f"   Changed PatientName to: {read.PatientName}\n")
                    log_file.write(f"   Changed PatientID to: {read.PatientID}\n")
                except Exception as e:
                    log_file.write(f"\nError processing DICOM file: {file_path}: {e}\n")
                    print(f"\nError: Failed to read DICOM file {file_path}: {e}\n")
            log_file.write("\n-----------------------------------------------------------------------------------------------")

        print(f"Log file created and saved to {log_file_path}\n")
        print("Anonymization Complete!\n")
    
    else:
        print("\nStopping Anonymization...\n")
    
    