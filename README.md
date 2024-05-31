[![GitHub license](https://img.shields.io/github/license/CNBP/DICOMTransit.svg)](https://github.com/CNBP/DICOMTransit/blob/master/LICENSE) [![Build Status](https://travis-ci.com/CNBP/DICOMTransit.svg?branch=master)](https://travis-ci.com/CNBP/DICOMTransit) [![GitHub issues](https://img.shields.io/github/issues/CNBP/DICOMTransit.svg)](https://github.com/CNBP/DICOMTransit/issues) [![Coverage Status](https://coveralls.io/repos/github/CNBP/DICOMTransit/badge.svg?branch=DICOMAnonimization)](https://coveralls.io/github/CNBP/DICOMTransit?branch=DICOMAnonimization) [![codebeat badge](https://codebeat.co/badges/77d7fbdb-2823-49f2-a311-2eea70d4eb28)](https://codebeat.co/projects/github-com-cnbp-dicomtransit-master) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/CNBP/DICOMTransit/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/CNBP/DICOMTransit/?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/36f48abc2a8c3802914a/maintainability)](https://codeclimate.com/github/CNBP/DICOMTransit/maintainability) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/03a4b7ba72c54989ad8f063693184c04)](https://www.codacy.com/app/dyt811/DICOMTransit?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=CNBP/DICOMTransit&amp;utm_campaign=Badge_Grade) 

![DICOMTranist Logo](https://github.com/CNBP/DICOMTransit/blob/master/logo.png)

An intermediate server that built around Orthanc server to include several commonly used components to serve a variety of functions to facilicate data transport and exchange from the scanner all the way to data storage services such as LORIS or offsite tertiary storage servers. 


## Planned features and other details forthcoming:
- @TODO: Sphinx documentation
- @TODO: HeuDiCom conversion of incoming DICOM files into BIDS compatible format.
- @TODO: Automated BIDS validation. 

## Deployment: 
- Containerized and deployable via Docker or Docker-Compose.
- Bundled Osimis Orthanc for MRI console connectivity

## Incoming Data Stream:
- Listen to Orthanc server at the default configuration.  

## Automated Conversion, DICOM Manipuation:
- Basic anonymization routine to guarantee the removal of the NAME and SUBJECT ID for now. 
- Basic SQLite database to store the anonymization process and the results research ID substitution. 

## Outgoing:
- Remote SSH upload
- Conversation/interaction (e.g LORIS) with remote system substitute and modify DICOM. E.g. obtain an ID remotely, write info into DICOM. 

## Security / Logging:
- Finite State Machine implementation: Sentry.IO remote automated bug report. 
- @TODO: Unerasble, auditable trail of all actions taken.
- @TODO: Unerasble, auditable record of all settings.

# Funding and Support:
* Currently, Canadian Neonatal Brain Platform, Canada

# Continuous Integration:
- TravisCI for unit testings
- Sentry for Logging
- @TODO: Appveyor

# How to setup DICOMTransit:
- Clone the repository
- Create a virtual environment inside the cloned repository with:
	- $ python3 -m venv dicom-env (dicom-env is what I used, you can name it anything you want)
+ Activate your virtual environment with:	
	- $ source .../dicom-env/bin/activate
+ Deactivate your virtual environment with:
	- $ deactivate
- Once your virtual environment is active, download all requirements:
	- $ pip install -r requirements.txt 	
- Initialise the submodules with:
	- $ git submodule init
- Update the submodules with:
	- $ git submodule update
- Modify line #8 in route.py from datagator/app/auth/routes.py with:
  - $ nano datagator/app/auth/routes.py
  - from werkzeug.urls import url_parse ---> from urllib.parse import urlparse
+ Save the file with Ctrl+O, Enter, Ctrl+X
- Run setup_check.py with:
	- $ python3 setup_check.py
+ If process is already running, kill it with:
	- $ kill "PID Number" (To find PID number, use command $ ps)
- If missing any other modules/packages, try:
	- $ pip install "package-name"

### What does the JP_Anonymizer.py do?: 
- Anonymizes all sensitive information of all .dcm files IN given directory (including sub-directories) with ID provided by LORIS. 
- It also update the local database called LoggingDB with each new anonymization attempts. The database stores records about patients before and after anonymization, as well as their location during the process and some other IDs for safe keeping. Further documentation can be found in Jhil_Scripts_Documentation.odt

# How to anonymize Dicom Files using JP_Anonymizer.py:
- Run JP_Anonymizer.py with:
	- $ python3 JP_Anonymizer.py
- Follow instructions in terminal

- Optionally: You can launch the script by provided arguments like this:
	- $ python3 JP_Anonymizer.py [folder_path] (Without brackets)
- You can also skip the confirmation question like this:
	- $ echo "yes" | python3 JP_Anonymizer.py [folder_path] (Use with caution, as anonymization is permanent) 
