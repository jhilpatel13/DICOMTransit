import datetime
import DICOMTransit
import DICOMTransit.LORIS.API
from DICOMTransit.DICOM.validate import DICOM_validate
from DICOMTransit.DICOM.elements import DICOM_elements
import logging
import pydicom
from tqdm import tqdm
from PythonUtils.PUFolder import recursive_list

from typing import List

logger = logging.getLogger()

class DICOM_anonymize:
    @staticmethod
    def folder(input_folder: str, new_ID: str) -> List[str]:
        """
        Iterate through a folder and anonymize everything in the folder that is DICOM.
        DICOM file check happens at the lowest DICOM_element level.
        :param input_folder:
        :param new_ID:
        :return:
        """
        files_list = recursive_list(input_folder)
        list_bad_files = DICOM_anonymize.filelist(files_list, new_ID)
        return list_bad_files

    @staticmethod
    def filelist(file_list: List[str]) -> List[str]:
        """
        Iterate through a filelist and anonymize everything in it  that is DICOM.
        DICOM file check happens at the lowest DICOM_element level.
        :param file_list:
        :return:
        """

        exception_count = 0
        exception_files = []

        for file in tqdm(file_list, position=0):
            # logger.debug(f"Anonymizing: {file}")
            save_success = DICOM_anonymize.save(file)
            if not save_success:
                exception_count = +1
                # exception_files = exception_files.append(file)

        logger.debug(
            f"Total exception encountered during anonymization: {str(exception_count)}"
        )
        return exception_files

    @staticmethod
    def save(file_path: str) -> bool:
        """
        Anonymize the DICOMS to remove any identifiable information. this overwrites the original file.
        DICOM file check happens at the lowest DICOM_element level. Added LORIS's ID anonymization functionality
        :param file_path: path of the file to be anonymized
        :param NewID: the new ID used to anonymize the subjects. It will overwrite patient names and IDs
        :return:
        """
        dicom_file = pydicom.dcmread(file_path)
        patient_sex = dicom_file.PatientSex
        patient_birth_date = dicom_file.PatientBirthDate
        parsed_patient_birth_date = str(datetime.datetime.strptime(patient_birth_date,'%Y%m%d').date())
        gender_mapping = {'M': 'Male', 'F': 'Female'}
        mapped_patient_sex = gender_mapping.get(patient_sex, 'Unknown')

        success, DCCID, PSCID = DICOMTransit.LORIS.API.create_candidate(
            "loris", parsed_patient_birth_date, mapped_patient_sex 
        )

        save_as_success = DICOM_anonymize.save_as(file_path, PSCID, file_path)
        return save_as_success

    @staticmethod
    def save_as(in_path: str, NewID: str, out_path: str) -> bool:
        """
        Anonymize the DICOM to remove any identifiable information from a file and to a output file provided.
        This operate at the memory level so should be quite a bit faster.
        DICOM file check happens at the lowest DICOM_element level.

        # NOTE! Expand here if you need to anonymize additional fields.
undefined
        :return:
        """
        success, DICOM = DICOM_validate.file(in_path)
        if not success:
            return False
        
        dicom_file = pydicom.dcmread(in_path)
        patient_age = dicom_file.PatientAge
        patient_birth_date = dicom_file.PatientBirthDate
        patient_study_date = dicom_file.StudyDate

        if DICOM_anonymize.verify_patient_age(patient_age, patient_birth_date, patient_study_date) == "Patient Age is accurate":
        
            # Anonymize PatientID with the NewID provided.
            success1, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM, "PatientID", NewID
            )
            if not success1:
                return False

            # Anonymize PatientName with the NewID provided.
            success2, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "PatientName", ""
            )
            if not success2:
                return False

            # Additionnal field added: Anonymize PatientBirthDate to undefined.
            success3, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "PatientBirthDate", ""
            )
            if not success3:
                return False
            
            # Additionnal field added: Anonymize StudyDate to undefined.
            success4, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "StudyDate", ""
            )
            if not success4:
                return False

            # Additionnal field added: Anonymize SeriesDate to undefined.
            success5, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "SeriesDate", ""
            )
            if not success5:
                return False

            # Additionnal field added: Anonymize SeriesDate to undefined.
            success6, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "AcquisitionDate", ""
            )
            if not success6:
                return False
            
            # Additionnal field added: Anonymize ContentDate to undefined.
            success7, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "ContentDate", ""
            )
            if not success7:
                return False

            # Additionnal field added: Anonymize AccessionNumber with the NewID provided.
            success8, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "AccessionNumber", ""
            )
            if not success8:
                return False
            
            # Additionnal field added: Anonymize ReferringPhysicianName with the NewID provided.
            success9, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "ReferringPhysicianName", ""
            )
            if not success9:
                return False
            
            # Additionnal field added: Anonymize InstitutionName with the NewID provided.
            success10, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "InstitutionName", ""
            )
            if not success10:
                return False
            
            # Additionnal field added: Anonymize StationName with the NewID provided.
            success11, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "StationName", ""
            )
            if not success11:
                return False
            
            """# Additionnal field added: Anonymize PerformedStationName with the NewID provided.
            success12, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "PerformedStationName", NewID
            )
            if not success12:
                return False
            """
            # Additionnal field added: Anonymize StudyID with the NewID provided.
            success13, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "StudyID", ""
            )
            if not success13:
                return False
            
            """# Additionnal field added: Anonymize PerformedLocation with the NewID provided.
            success14, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "PerformedLocation", NewID
            )
            if not success14:
                return False
            """
            # Additionnal field added: Anonymize ProtocolName with the NewID provided.
            success15, DICOM_updated = DICOM_elements.update_in_memory(
                DICOM_updated, "ProtocolName", ""
            )
            
            # Return after encuring both anonymization process are successful.
            if success15:
                DICOM_updated.save_as(out_path)
                return True
            else:
                return 
        elif DICOM_anonymize.verify_patient_age(patient_age, patient_birth_date, patient_study_date) == "Patient Age is not accurate":
            print(f"Error at {in_path}\nPatient age is not accurate according to the difference between his birthday and scan date.\n Skipping anonymization...")
            return False
        else:
            print(f"file:{in_path} is already anonymized")

    @staticmethod
    def verify_patient_age(patient_age, patient_birth_date, patient_study_date):
        if (patient_birth_date is not None and patient_birth_date != '') and (patient_study_date is not None and patient_study_date != ''):
            unit = patient_age[-1]

            difference = str((datetime.datetime.strptime(patient_study_date,"%Y%m%d") - datetime.datetime.strptime(patient_birth_date,"%Y%m%d")).days)

            if unit == "D":
                age = int(patient_age[:-1])
                
            if unit == "W":
                age = int(patient_age[:-1]) * 7

            if unit == "Y":
                age = int(patient_age[:-1]) * 365

            if difference == str(age):
                return "Patient Age is accurate"
            else:
                return "Patient Age is not accurate"
        else:
            return "Patient Age is invalid"
                
# if __name__ is "__main__":
