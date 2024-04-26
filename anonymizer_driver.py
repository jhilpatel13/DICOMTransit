import sys

from DICOMTransit.DICOM.anonymize_dicom import anonymize_dicom

if __name__ == '__main__':
    
    #Checks if arguments are provided when script is deployed
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
        new_ID  = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        print("\nDICOM Anonymization: \n")
        #Asks user for folder path
        folder_path = input("Enter the folder path containing DICOM files: \n").strip() or None

        #ID for Patient Name, Patient ID (Default: None)
        new_ID = "None"

    anonymize_dicom(folder_path, new_ID)