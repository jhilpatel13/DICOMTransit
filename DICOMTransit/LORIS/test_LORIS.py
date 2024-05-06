import unittest
import pydicom
import DICOMTransit.LORIS.API
import DICOMTransit.LocalDB.API
from DICOMTransit.DICOM.DICOMPackage import DICOMPackage
from DICOMTransit.settings import config_get
import os

class test_LORIS(unittest.TestCase):
    @staticmethod
    def test_LORIS():

        dicom_file = pydicom.dcmread("/home/jhilpatel/Anonymization_test_files/sub-B031S1/sub-B031S1_dicom/MR_3Plane_Loc_SSFSE/MR000000.dcm")
        patient_sex = dicom_file.PatientSex
        patient_birth_date = dicom_file.PatientBirthDate
        
        # print(create_candidate("loris", patient_birth_date, patient_sex))
       

        # DICOM_package = DICOMPackage(dicom_folder)

        # DICOM_package.project = "loris"

        # create new PSCID and get DCCID
        success, DCCID, PSCID = DICOMTransit.LORIS.API.create_candidate(
            "loris", "2023-02-24", "Male"
        )
        print(success)
        print(DCCID)
        print(PSCID)

        """# Local Variable for anonymization.
        DICOM_package.DCCID = DCCID
        DICOM_package.CNBPID = PSCID
        DICOM_package.timepoint = "V1"  # auto generated.
"""