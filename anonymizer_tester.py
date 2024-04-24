import subprocess

if __name__ == '__main__':
    
    command = ["python3", "/home/jhilpatel/DICOMTransit/anonymizer_driver.py", "/home/jhilpatel/Anonymization_test_files/sub-B031S1", "test command line argumant"]
    
    output = subprocess.run(command)