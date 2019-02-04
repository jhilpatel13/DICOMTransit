# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------------------------------------------------

import pyodbc
from redcap.enums import Database, Field, DataType
from redcap.constants import cnn_connection_string, cnfun_connection_string
from redcap.transaction import RedcapTransaction


# ----------------------------------------------------------------------------------------------------------------------
#  Local ODBC
# ----------------------------------------------------------------------------------------------------------------------

def get_database_column_names(table_info, transaction: RedcapTransaction):
    """
    Returns a list of fields contained within a database table.
    :param table_info: Table Information
    :param transaction: the transaction content to be updated.
    :return: List of fields
    """
    if table_info is None:
        return table_info

    # If this is the first time the column names are requested for this table
    if table_info[4].lower() not in transaction.database_column_names:
        # Get column names from database.

        conn = pyodbc.connect(get_connection_string(table_info[5]))
        odbc_cursor = conn.cursor()

        result = odbc_cursor.execute('SELECT * FROM [' + table_info[4].lower() + '] WHERE 1=0')
        database_columns = [tuple[0] for tuple in result.description]

        odbc_cursor.close()

        # Store a copy of column names for this table in local memory.
        transaction.database_column_names[table_info[4].lower()] = database_columns

    else:
        # Get column names from cache.
        database_columns = transaction.database_column_names[table_info[4].lower()]

    return database_columns


def get_data_rows_for_patient_table(table_info, transaction: RedcapTransaction):
    """
    Gets all rows of data for a specific patient table.
    :param table_info: Table Information
    :param transaction: the transaction content to be updated.
    :return: List of all the rows obtained from the query.
    """
    if table_info is None:
        return table_info
    if table_info[4] == '':
        return None

    primary_key_filter_name = str(get_primary_key_name(table_info[6]))
    primary_key_filter_value = str(transaction.get_primary_key_value(table_info[7]))
    primary_key_data_type = get_primary_key_data_type(table_info[7])

    if primary_key_filter_name == '' or primary_key_filter_value == '' or primary_key_filter_value == 'None':
        return None

    if primary_key_data_type == DataType.String.value:
        select_statement = ("SELECT * FROM [" +
                            table_info[4] +
                            "] WHERE [" +
                            primary_key_filter_name +
                            "] = " +
                            "'" +
                            primary_key_filter_value +
                            "'")
    elif primary_key_data_type == DataType.Integer.value:
        select_statement = ("SELECT * FROM [" +
                            table_info[4] +
                            "] WHERE [" +
                            primary_key_filter_name +
                            "] = " +
                            primary_key_filter_value)
    else:
        select_statement = ''

    if select_statement != '':

        conn = pyodbc.connect(get_connection_string(table_info[5]))
        odbc_cursor = conn.cursor()

        odbc_cursor.execute(select_statement)

        data = odbc_cursor.fetchall()

        odbc_cursor.close()
        conn.close

        return data

    else:
        return None


def get_data_rows_for_reference_table(table_info):
    """
    Gets all rows of data for a specific reference table.
    :param table_info: Table Information
    :return: List of all the rows obtained from the query.
    """
    if table_info is not None:
        if table_info[4] != '':

            select_statement = 'SELECT * FROM [' + table_info[4] + ']'

            conn = pyodbc.connect(get_connection_string(table_info[5]))
            odbc_cursor = conn.cursor()

            odbc_cursor.execute(select_statement)

            data = odbc_cursor.fetchall()

            odbc_cursor.close()
            conn.close

            return data

        else:
            return None
    else:
        return None


def get_connection_string(database):
    """
    Get Connection String
    :param database: Database Configuration Number
    :return: Connection String
    """
    if database == Database.CNN.value:
        return cnn_connection_string
    elif database == Database.CNFUN.value:
        return cnfun_connection_string
    else:
        return ''


def get_primary_key_name(primary_key):
    """
    Get Primary Key Name
    :param primary_key: Primary Key Configuration Number
    :return: Primary Key Name
    """
    if primary_key == Field.BabyId.value:
        return Field.BabyId.name
    elif primary_key == Field.CaseId.value:
        return Field.CaseId.name
    elif primary_key == Field.CNNPatientUI.value:
        return Field.CNNPatientUI.name
    elif primary_key == Field.HospitalRecordNumber.value:
        return Field.HospitalRecordNumber.name
    elif primary_key == Field.MotherId.value:
        return Field.MotherId.name
    elif primary_key == Field.PatientId.value:
        return Field.PatientId.name
    elif primary_key == Field.PatientUI.value:
        return Field.PatientUI.name
    elif primary_key == Field.MasterId.value:
        return Field.MasterId.name
    else:
        return Field.Unknown.name


def get_primary_key_data_type(primary_key):
    """
    Get Primary Key Data Type
    :param primary_key: Primary Key Configuration Number
    :return: Data Type Configuration Value
    """
    if primary_key == Field.BabyId.value:
        return DataType.Integer.value
    elif primary_key == Field.CaseId.value:
        return DataType.String.value
    elif primary_key == Field.CNNPatientUI.value:
        return DataType.String.value
    elif primary_key == Field.HospitalRecordNumber.value:
        return DataType.String.value
    elif primary_key == Field.MotherId.value:
        return DataType.Integer.value
    elif primary_key == Field.PatientId.value:
        return DataType.Integer.value
    elif primary_key == Field.PatientUI.value:
        return DataType.String.value
    elif primary_key == Field.MasterId.value:
        return DataType.Integer.value
    else:
        return DataType.Unknown.value