########################################################################################################################
#
# Canadian Neonatal Brain Platform:
#   CNN/CNFUN to REDCap Data Update Script
#
# Author:
#   Applied Clinical Research Unit (URCA) - CHU Sainte-Justine Research Center
#
# History:
#   -> Summer 2018 - Initial Creation
#   -> Fall 2018 - Code completion and cleanup
#   -> Winter 2019 - Code completion and cleanup
#   -> TBD - Final version
#
# Note:
#   Developed for Python 3.6.7
#
########################################################################################################################


# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------------------------------------------------

from tkinter import *

# ----------------------------------------------------------------------------------------------------------------------
#  Custom Modules
# ----------------------------------------------------------------------------------------------------------------------
from LocalDB.API import load_hospital_record_numbers
from redcap.prepare_patient import prepare_patient_tables
from redcap.prepare_reference import prepare_reference_tables
from redcap.initialization import initialize_data_import_configuration_matrix
from redcap.query import load_redcap_metadata, send_data_to_redcap
import logging

# Note: You may tell the script to use the values of the development or production constants simply by commenting out
#       one of the two lines below.
# import production as environment


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# ----------------------------------------------------------------------------------------------------------------------
#  Functions
# ----------------------------------------------------------------------------------------------------------------------


def update_redcap_data():
    """
    This method is the main method of this script. It calls all methods necessary to transfer CNN and CNFUN data
    to REDCap.
    :return: None
    """

    window.config(cursor="wait")

    # Insert blank line.
    label = Label(window, text='')
    label.pack()

    # Load data import configuration matrix.
    label = Label(window, text='Loading Data Import Configuration...')
    label.pack()
    initialize_data_import_configuration_matrix()
    label = Label(window, text='Done.')
    label.pack()

    # Get all information about REDCap table names and fields.
    label = Label(window, text='Loading REDCap Metadata...')
    label.pack()
    load_redcap_metadata()
    label = Label(window, text='Done.')
    label.pack()

    # Get all hospital record numbers.
    label = Label(window, text='Loading Hospital Record Numbers...')
    label.pack()
    load_hospital_record_numbers()
    label = Label(window, text='Done.')
    label.pack()

    # Update Reference Tables.
    label = Label(window, text='Preparing Reference Data Transfer...')
    label.pack()
    prepare_reference_tables()
    label = Label(window, text='Done.')
    label.pack()

    # Update Patient Tables.
    label = Label(window, text='Preparing Patient Data Transfer...')
    label.pack()
    prepare_patient_tables()
    label = Label(window, text='Done.')
    label.pack()

    # Send data to REDCap.
    label = Label(window, text='Sending ALL data to REDCap...')
    label.pack()
    send_data_to_redcap()
    label = Label(window, text='Done.')
    label.pack()

    # Insert blank line.
    label = Label(window, text='')
    label.pack()

    # Indicate that the script is completed.
    label = Label(window, text='Command completed.')
    label.pack()

    window.config(cursor="")

    return


if __name__ == "__main__":

    # ----------------------------------------------------------------------------------------------------------------------
    #  UI Code
    # ----------------------------------------------------------------------------------------------------------------------

    # Initialize the tcl/tk interpreter and create the root window.
    window = Tk()

    # Adjust size of window.
    window.geometry("1024x768")

    # Add a title label to the root window.
    label = Label(window, text="CNN/CNFUN to REDCap - Data Update")
    label.pack()

    # Add all buttons to the root window.
    button = Button(window, text="Update REDCap Data", command=update_redcap_data, height=1, width=25)
    button.pack()

    # Set window title.
    window.title("CNN/CNFUN to REDCap - Data Update")

    # Display window.
    window.mainloop()

    update_redcap_data()