import datetime
from DICOMTransit.DICOM.validate import DICOM_validate
from DICOMTransit.DICOM.elements import DICOM_elements
import logging
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
    def filelist(file_list: List[str], new_ID: str) -> List[str]:
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
            save_success = DICOM_anonymize.save(file, new_ID)
            if not save_success:
                exception_count = +1
                exception_files = exception_files.append(file)

        logger.debug(
            f"Total exception encountered during anonymization: {str(exception_count)}"
        )
        return exception_files

    @staticmethod
    def save(file_path: str, NewID: str) -> bool:
        """
        Anonymize the DICOMS to remove any identifiable information. this overwrites the original file.
        DICOM file check happens at the lowest DICOM_element level.
        :param file_path: path of the file to be anonymized
        :param NewID: the new ID used to anonymize the subjects. It will overwrite patient names and IDs
        :return:
        """
        save_as_success = DICOM_anonymize.save_as(file_path, NewID, file_path)
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

        # Anonymize PatientID with the NewID provided.
        success1, DICOM_updated = DICOM_elements.update_in_memory(
            DICOM, "PatientID", NewID
        )
        if not success1:
            return False

        # Anonymize PatientName with the NewID provided.
        success2, DICOM_updated = DICOM_elements.update_in_memory(
            DICOM_updated, "PatientName", NewID
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
            DICOM_updated, "AccessionNumber", NewID
        )
        if not success8:
            return False
        
        # Additionnal field added: Anonymize ReferringPhysicianName with the NewID provided.
        success9, DICOM_updated = DICOM_elements.update_in_memory(
            DICOM_updated, "ReferringPhysicianName", NewID
        )
        if not success9:
            return False
        
        # Additionnal field added: Anonymize InstitutionName with the NewID provided.
        success10, DICOM_updated = DICOM_elements.update_in_memory(
            DICOM_updated, "InstitutionName", NewID
        )
        if not success10:
            return False
        
        # Additionnal field added: Anonymize StationName with the NewID provided.
        success11, DICOM_updated = DICOM_elements.update_in_memory(
            DICOM_updated, "StationName", NewID
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
            DICOM_updated, "StudyID", NewID
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
            DICOM_updated, "ProtocolName", NewID
        )
        
        # Return after encuring both anonymization process are successful.
        if success15:
            DICOM_updated.save_as(out_path)
            return True
        else:
            return False

# if __name__ is "__main__":
