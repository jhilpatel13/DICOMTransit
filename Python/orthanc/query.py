import requests
import logging
import os
import shutil
import zipfile
import sys
from PythonUtils.file import is_name_unique, unique_name, current_funct_name
from requests.auth import HTTPBasicAuth
from settings import config_get
from tqdm import tqdm

class orthanc_query:

    @staticmethod
    def authenticateOrthanc():
        #todo: all the get, set can be potentially using a decorator function to authenticate.
        raise NotImplementedError
        pass

    @staticmethod
    def getOrthanc_noauth(endpoint):
        """
        Get from a Orthanc endpoint
        :param endpoint:
        :return: bool on if such PSCID (INSTITUTIONID + PROJECTID + SUBJECTID) exist already.
        """
        logger = logging.getLogger(current_funct_name())
        logger.debug("Getting Orthanc endpoint: "+ endpoint)

        with requests.Session() as s:
            r = s.get(endpoint)
            logger.debug(f"Get Result: {str(r.status_code)} {r.reason}")
            return r.status_code, r.json()


    @staticmethod
    def getOrthanc(endpoint, orthanc_user, orthanc_password):
        """
        Get from a Orthanc endpoint
        :param endpoint:
        :return: bool on if such PSCID (INSTITUTIONID + PROJECTID + SUBJECTID) exist already.
        """
        logger = logging.getLogger(current_funct_name())
        logger.debug("Getting Orthanc endpoint: "+ endpoint)

        with requests.Session() as s:
            r = s.get(endpoint, auth=HTTPBasicAuth(orthanc_user, orthanc_password))
            logger.debug(f"Get Result: {str(r.status_code)} {r.reason}")
            return r.status_code, r.json()


    @staticmethod
    def postOrthanc(endpoint, orthanc_user, orthanc_password, data):
        """
        Get from a Orthanc endpoint
        :param endpoint:
        :param data
        :return: bool on if such PSCID (INSTITUTIONID + PROJECTID + SUBJECTID) exist already.
        """
        logger = logging.getLogger(current_funct_name())
        logger.debug("Post Orthanc endpoint: "+ endpoint)
        with requests.Session() as s:
            r = s.post(endpoint, auth=HTTPBasicAuth(orthanc_user, orthanc_password), files=data)
            logger.debug(f"Post Result: {str(r.status_code)} {r.reason}")
            return r.status_code, r

    @staticmethod
    def deleteOrthanc(endpoint, orthanc_user, orthanc_password):
        """
        Delete from a Orthanc endpoint
        :param endpoint:
        :return: bool on if such PSCID (INSTITUTIONID + PROJECTID + SUBJECTID) exist already.
        """
        logger = logging.getLogger(current_funct_name())
        logger.debug(f"Deleting Orthanc endpoint: {endpoint} at")
        with requests.Session() as s:
            r = s.delete(endpoint, auth=HTTPBasicAuth(orthanc_user, orthanc_password))
            logger.debug(f"Deletion Result: {str(r.status_code)} {r.reason}")
        return r.status_code, r.json()

    @staticmethod
    def getPatientZipOrthanc(endpoint, orthanc_user, orthanc_password):
        """
        Get Orthanc endpoint archive ZIP files.
        :param endpoint:
        :return: status of the get requests, and the actual local file name saved in the process.
        """

        logger = logging.getLogger(current_funct_name())
        logger.debug(f"Downloading Orthanc endpoint: {endpoint}")

        zip_path = config_get("ZipPath")
        with requests.Session() as s:
            r = s.get(endpoint, stream=True, verify=False, auth=HTTPBasicAuth(orthanc_user, orthanc_password))

            # Compute total size to be downloaded
            total_size = int(r.headers.get('content-length', 0))
            total_size_mb =  round(total_size/1024/1024, 3)
            # Generate the full output path
            local_file_full_path = os.path.join(zip_path, f"{unique_name()}.zip")

            progress_bar = tqdm(unit="Mb", total=total_size_mb)

            # NOTE the stream=True parameter
            with open(local_file_full_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        chunk_mb = round(len(chunk)/1024/1024, 3)
                        progress_bar.update()
                        f.write(chunk)

        logger.debug(str(r.status_code) + r.reason)
        logger.info(f"Download to {local_file_full_path} is fully complete!")
        return r.status_code, local_file_full_path

    @staticmethod
    def flatUnZip(input_zip, out_dir):
        """
        Inspired by https://stackoverflow.com/questions/4917284/extract-files-from-zip-without-keeping-the-structure-using-python-zipfile
        Added function to hanlde non-unique file names which are probably standarderized by Orthanc.
        :param input_zip:
        :param out_dir:
        :return:
        """

        with zipfile.ZipFile(input_zip) as zip_file:
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                # skip directories
                if not filename:
                    continue

                # copy file (taken from zipfile's extract)
                source = zip_file.open(member)

                proposed_filename = os.path.join(out_dir, filename)
                # handle duplicate names!
                _, unique_output_filename = is_name_unique(proposed_filename)
                target = open(unique_output_filename, "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
