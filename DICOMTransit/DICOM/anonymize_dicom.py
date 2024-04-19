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
    
    #Displays each patient information found at folder path  before anonymization (currently not used because it floods the terminal)
    '''
    print("Patient information before anonymization:")
    for file_path in folder_path.rglob("*.dcm"):
        try:
            read = pydicom.dcmread(file_path)
            print(f"File: {file_path}")
            print(f"Patient Name: {read.PatientName}")
            print(f"Patient ID: {read.PatientName}")
        except Exception as e:
            print("Failed to read DICOM file {file_path}: {e}")
    '''
    #Anonymizes the files
    DICOMTransit.DICOM.anonymize.DICOM_anonymize.filelist(files, new_ID)
    
    #Displays each patient information found at folder path after anonymization (currently not used because it floods the terminal)
    '''
    print("Patient information before anonymization:")
    for file_path in folder_path.rglob("*.dcm"):
        try:
            read = pydicom.dcmread(file_path)
            print(f"File: {file_path}")                
            print(f"Patient Name: {read.PatientName}")
            print(f"Patient ID: {read.PatientName}")
        except Exception as e:
            print("Failed to read DICOM file {file_path}: {e}")
    '''
    print("\n***** ANONYMIZATION COMPLETE *****\n")