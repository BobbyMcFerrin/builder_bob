#############################
# Bob Output
#
#
#
#############################

# Python Imports

import logging
from pprint import pprint

# Infrastructure Imports

from Utils import GlobalVars
from Utils.Bob_UtilsError import UtilsError
from Utils.Bob_UtilsFile import UtilsFile
from Utils.Bob_UtilsData import UtilsData
from Controller.Logic.Bob_Excel import Bob_Excel_Service

#################### Bob TelAviv Analyze Object #####################

class Bob_Output_Object:

    """
    Bob TelAviv Object
    """

    #### Inits ####

    def __init__(self, file_name=None):
        """
        Inits
        """
        logging.debug('Initializing Bob Output Object ..')
        self.__file_name = file_name

    ################### Output To Excel ##################

    def _output_to_xls(self, data, file_path):
        """
        Main Loop
        """
        logging.debug('Outputs ..')
        headers = ['ChapterName', 'HeadLine', 'HeadLine_Num', 'SubHeadLine', 'SubHeadLine_Num', 'GuideNum', 'GuideText', 'Discipline', 'Type', 'Space']
        output_data = []
        for entry in data:
            this_entry = []
            clean_entry_a, _ = UtilsData.extract_section_number(entry['head_line_a_text'])
            clean_entry_b, _ = UtilsData.extract_section_number(entry['head_line_b_text'])

            this_entry.append(entry['major_head_line_text'])
            this_entry.append(clean_entry_a)
            this_entry.append(entry['head_line_a_num'].strip(".") + ".")
            this_entry.append(clean_entry_b)
            this_entry.append(entry['head_line_b_num'])
            this_entry.append(entry['guideline_num'])
            this_entry.append(entry['guideline_text'])
            this_entry.append(', '.join(entry['classification']['disciplines']))
            this_entry.append(', '.join(entry['classification']['facility_types']))
            this_entry.append(', '.join(entry['classification']['facility_space_types']))
            output_data.append(this_entry)
        excel = Bob_Excel_Service()
        excel.create_workbook()
        excel.create_sheet("Test")
        excel.add_table(
            headers=headers,
            data=output_data,
            header_bg_color="4472C4"
        )
        excel.auto_fit_columns()
        excel.auto_fit_rows()
        excel.save(file_path)

    #### Main Loop ####

    def main_loop(self):
        """
        Main Loop
        """
        logging.debug('Conducts Output ..')
        files = UtilsFile.traverse_directory(GlobalVars.prop_file_documents_consolidated,
                                             ext='.dat')
        for entry in files:
            if self.__file_name is not None:
                if entry[1].find(self.__file_name) == -1:
                    continue
            data = UtilsFile.load_pickle(entry[0])
            target_path = GlobalVars.prop_file_documents_output + entry[1].replace(".dat", ".xlsx")
            self._output_to_xls(data, target_path)


