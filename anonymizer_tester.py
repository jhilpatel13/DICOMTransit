import datetime
import subprocess
import unittest
from DICOMTransit.DICOM.anonymize import DICOM_anonymize
import pydicom

from DICOMTransit.LORIS.test_LORIS import test_LORIS
    
if __name__ == '__main__':
    unittest.main()
    
    #command = ["python3", "/home/jhilpatel/DICOMTransit/anonymizer_driver.py", "/home/jhilpatel/Anonymization_test_files/sub-B031S1", "test command line argument"]
    #output = subprocess.run(command)

    """dt1 = "19990101"
    dt2 = "19990411"
    age = "100D"
    print(DICOM_anonymize.verify_patient_age(age,dt1,dt2))"""

    
    