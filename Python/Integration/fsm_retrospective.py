import logging
import os.path
import orthanc.API
import urllib.parse
from tqdm import tqdm
from orthanc.query import orthanc_query
from pathlib import Path
from joblib import Parallel, delayed
import multiprocessing
from DICOM.validate import DICOM_validate

logger = logging.getLogger()

# Getting credential from the environment.
#url, username, password = orthanc.API.get_prod_orthanc_credentials()
url, username, password = orthanc.API.get_dev_orthanc_credentials()

url_instances = urllib.parse.urljoin(url, "/instances")

def read_file(path_file):
    """
    Read a file from the OS.walked path.
    :param walk_root:
    :param walk_file:
    :return:
    """
    # PreRead the file.

    file = open(path_file, "rb")
    content = {'file': file.read()}
    file.close()
    return content

def read_upload_file(path_file):

    # check if the file is validated before continueing
    if (DICOM_validate.file(path_file)):
        content = read_file(path_file)

        # Upload and keep track of success.
        success = orthanc_query.upload(path_file, url_instances, username, password, content)
        print(f"Finished uploading:{path_file}")
        return success
    else:
        return False


def upload_retrospective_study(path_study_root_folder_path: Path):
    """
    Sample script to recursively import in Orthanc all the DICOM files
    that are stored in some path. Please make sure that Orthanc is running
    before starting this script. The files are uploaded through the REST
    API.

    Usage: %s [hostname] [HTTP port] [path]
    Usage: %s [hostname] [HTTP port] [path] [username] [password]
    For instance: %s 127.0.0.1 8042 .

    :param path_study_root_folder_path:
    :return: 1
    """

    success_count = 0
    total_file_count = 0


    if os.path.isfile(path_study_root_folder_path):
        # Upload a single file
        total_file_count = 1
        success_count = orthanc_query.upload(path_study_root_folder_path, url_instances, username, password)
    else:
        # Recursively upload a directory
        for root, dirs, files in os.walk(path_study_root_folder_path):

            list_files = []

            # Generate hte list of files as input.
            for f in tqdm(files):
                path_file = os.path.join(root, f)
                list_files.append(path_file)

            total_file_count = len(list_files)

            # Parallel process them
            num_cores = multiprocessing.cpu_count()
            results = Parallel(n_jobs=num_cores)(delayed(read_upload_file)(i) for i in list_files)
            success_count = sum(results)

    
    if success_count == total_file_count:
        logger.info("\nSummary: all %d DICOM file(s) have been imported successfully" % success_count)
    else:
        logger.warning("\nSummary: %d out of %d files have been imported successfully as DICOM instances" % (success_count, total_file_count))


if __name__=="__main__":
    import time
    start = time.time()
    logging.basicConfig(level=logging.INFO)
    path_input = Path(r"/toshiba4/bayX_backup/Research PAC/Registry_Raw/")
    upload_retrospective_study(path_input)
    end = time.time()
    print(str((end - start)/60)+" minutes")