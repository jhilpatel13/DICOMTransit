from requests import post
from redcap import development as environment


def test_Post():

    # Two constants we'll use throughout
    TOKEN = environment.REDCAP_TOKEN_CNN_ADMISSION
    URL = "https://redcap.cnbp.ca/api/"

    payload = {"token": TOKEN, "format": "json", "content": "metadata"}

    response = post(URL, data=payload)
    print(response)


def test_PyCap():
    from PyCap.redcap import project

    # Two constants we'll use throughout
    TOKEN = environment.REDCAP_TOKEN_CNN_ADMISSION
    URL = "https://redcap.cnbp.ca/api/"
    project_admission = project.Project(URL, TOKEN)
    data = project_admission.export_records()
