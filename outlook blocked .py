import csv
import glob
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def get_input_file_name():
    """
        This function is used to get input file. Here I am using glob.glob() module to find all
        the pathnames matching a specified pattern.
    :return:
        'Input_log_file.csv'
    """
    try:
        return list(set(glob.glob('Input*')) - set(glob.glob('*Output*')))[0]
    except Exception as error:
        logger.error(error)
        return ''


def get_output_file_name(in_file_name):
    """
        This function is used to get output file name
    :return:
        'Input_log_file_Output_report.csv'
    """
    return f"{in_file_name.replace('.csv', '')}_Output_report.csv"


def output_file_data(in_file_name):
    """

    :param in_file_name:
    :return:
        [
            {'ID_1': '1', 'ID_2': '11', 'Name': 'ABC', 'Dept': 'A', 'Age': '22', 'Dept_Name': 'IT'},
            {'ID_1': '1', 'ID_2': '11', 'Name': 'XYZ', 'Dept': 'B', 'Age': '43', 'Dept_Name': 'Finance'},
            {'ID_1': '1', 'ID_2': '11', 'Name': 'DEF', 'Dept': 'C', 'Age': '23', 'Dept_Name': 'Marketing'},
            {'ID_1': '1', 'ID_2': '11', 'Name': 'WER', 'Dept': 'D', 'Age': '45', 'Dept_Name': 'HR'},
            {'ID_1': '1', 'ID_2': '22', 'Name': 'QWE', 'Dept': 'E', 'Age': '42', 'Dept_Name': 'Legal'},
            {'ID_1': '1', 'ID_2': '22', 'Name': 'ASD', 'Dept': 'R', 'Age': '11', 'Dept_Name': 'Operations'},
            {'ID_1': '1', 'ID_2': '22', 'Name': 'ZXC', 'Dept': 'F', 'Age': '33', 'Dept_Name': 'Network'},
            {'ID_1': '1', 'ID_2': '22', 'Name': 'WERT', 'Dept': 'G', 'Age': '88', 'Dept_Name': 'Admin'}
        ]
    """
    try:
        temp_list = []
        with open(in_file_name, 'r') as input_file:
            csv_file = csv.DictReader(input_file)
            for i in csv_file:
                id_1 = i['ID_1']
                id_2 = i['ID_2']
                input_file_dept = i['Dept']
                file_name = f'{id_1}_{id_2}_Masterfile.csv'
                # Search master file
                file_list = glob.glob(file_name)
                if file_list:
                    try:
                        with open(file_list[0], 'r') as search_file:
                            csv_search_file = csv.DictReader(search_file)
                            for j in csv_search_file:
                                output_file_dept = j['Dept']
                                output_file_dept_name = j['Dept_Name']
                                if input_file_dept == output_file_dept:
                                    i['Dept_Name'] = output_file_dept_name
                                    break
                                else:
                                    i['Dept_Name'] = ''
                    except Exception as error:
                        logger.error(error)
                else:
                    i['Dept_Name'] = ''
                    logger.error(f"{file_name} => This file not found using the combination of id1 and id2")
                    continue
                temp_list.append(i)
        print(temp_list)
        return temp_list
    except Exception as error:
        logger.error("Error occurred => ", str(error))


def write_output_file(out_data, out_file_name):
    """
        This function is used to write output file.
    :return:
    """
    fields = out_data[0].keys()
    with open(out_file_name, 'w') as output_file:
        csv_output_file = csv.DictWriter(output_file, fieldnames=fields)
        csv_output_file.writeheader()
        csv_output_file.writerows(output_data)


# Get Input File Name
input_file_name = get_input_file_name()

# If input file not found in path
if not input_file_name:
    logger.info("No Input File Found. Kindly Check Again")
else:
    # get final output data to be stored in file
    output_data = output_file_data(input_file_name)

    # get output file name
    output_file_name = get_output_file_name(input_file_name)

    # create new file with output file name and store output data in it
    write_output_file(output_data, output_file_name)

    # Operation done
    logger.info(f"Operation Done. Kindly check the output file with name => {output_file_name}")
