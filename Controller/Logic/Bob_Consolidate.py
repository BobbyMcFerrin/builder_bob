#############################
# Bob Logic
#
#
#
#############################

# Python Imports

import logging
from pprint import pprint

# Infrastructure Imports

from Utils import GlobalVars
from Utils.Bob_UtilsFile import UtilsFile
from Utils.Bob_UtilsData import UtilsData
from Utils.Bob_UtilsThread import Bob_UtilsThread_Object
from Controller.Logic.Bob_OpenAI import Bob_AI_Object

#################### Bob Consolidate #####################

class Bob_Consolidate_Object:

    """
    Bob Logic Object
    """

    #### Inits ####

    def __init__(self, file_name=None):
        """
        Inits
        """
        logging.debug('Initializing Bob Consolidation Object ..')
        self._openai = Bob_AI_Object()
        self.__file_name = file_name

    #### Aggregate To Final Data ####

    def _aggregate_sections(self, data, name):
        """
        Aggregate To Final Data
        """
        for entry in data['blocks']:
            sec_num = entry['section_number'].strip()
            if sec_num == '':
                continue

            # Special Fixes !!
            # Education Doc !
            if name == 'education':
                if sec_num.startswith('5.2.4.18.') is True:
                    sec_num = sec_num.replace('5.2', '52')
                if sec_num.startswith('5.2.4.19.') is True:
                    sec_num = sec_num.replace('5.2', '52')
                if sec_num == '2.3.2.2.1':
                    sec_num = '42.11.3.4'
            if name == 'community':
                if sec_num.startswith('2.0.') is True:
                    sec_num = sec_num.replace('2.0.', '20.')
                if sec_num.startswith('2.3.5.5.1') is True:
                    sec_num = sec_num.replace('2.3.5.5.1', '23.5.5.1')
                if sec_num.startswith('2.9.7.') is True:
                    sec_num = sec_num.replace('2.9.7.', '29.7.')
                if sec_num.startswith('3.2.6.') is True:
                    sec_num = sec_num.replace('3.2.6.', '32.6.')
                if sec_num.startswith('4.3.4.2.') is True:
                    sec_num = sec_num.replace('4.3.4.2.', '43.4.2.')
                if sec_num.startswith('4.3.5.10.') is True:
                    sec_num = sec_num.replace('4.3.5.10.', '43.5.10.')
                if sec_num.startswith('7.1.4.4.') is True:
                    sec_num = sec_num.replace('7.1.4.4.', '71.4.4.')
            split_dots = sec_num.split(".")
            #### Major HeadLine / HeadLine A
            if len(split_dots) == 1:
                if UtilsData.is_number(split_dots[0]) is False:
                    self._m_headline = [sec_num, entry['text'].strip()]
                else:
                    self._h_1 = [sec_num, entry['text'].strip()]
            #### HeadLine B
            if len(split_dots) == 2:
                if split_dots[1].strip() == '':
                    _this = entry['text'].strip()
                    if _this.find('\n') == -1:
                        self._h_1 = [sec_num, entry['text'].strip()]
                else:
                    self._h_2 = [sec_num, entry['text'].strip()]
            if len(split_dots) >= 3:
                self._agg_data.setdefault(sec_num,
                    {'headlines': [self._m_headline, self._h_1, self._h_2],
                     'guideline': [sec_num, entry['text'].strip()]})


    ####################### Prepare Data For Classification ####################

    def _prepare_data_for_classification(self):
        """
        Prepare Data For Classification
        """
        for sec_num in self._agg_data:
            entry = self._agg_data[sec_num]
            guideline_num = entry['guideline'][0]
            guideline_text = entry['guideline'][1]
            #if sec_num.count('.') >= 4 and sec_num.find("\n") == -1:
            #    print([sec_num], guideline_text)
            major_head_line_num = entry['headlines'][0][0]
            major_head_line_text = entry['headlines'][0][1]
            head_line_a_num = entry['headlines'][1][0]
            head_line_a_text = entry['headlines'][1][1]
            if entry['headlines'][2] is  None:
                head_line_b_num = 'x.'
                head_line_b_text = 'NotAvailable'
            else:
                head_line_b_num = entry['headlines'][2][0]
                head_line_b_text = entry['headlines'][2][1]
            self._final_data.append(
                {'guideline_text': guideline_text,
                 'guideline_num': guideline_num,
                 'major_head_line_num': major_head_line_num,
                 'major_head_line_text': major_head_line_text,
                 'head_line_a_num': head_line_a_num,
                 'head_line_a_text': head_line_a_text,
                 'head_line_b_num': head_line_b_num,
                 'head_line_b_text': head_line_b_text,
                 'classification': None})

    ######### Single Action Classification #######

    def _single_action_classification(self, data_entry):
        """
        Single Action Classification
        """

        major_head_line_text = data_entry['payload']['major_head_line_text']
        head_line_a_text = data_entry['payload']['head_line_a_text']
        head_line_b_text = data_entry['payload']['head_line_b_text']
        guideline_text = data_entry['payload']['guideline_text']
        guideline_num = data_entry['payload']['guideline_num']

        if guideline_num.count('.') == 3:
            for _this_entry in self._final_data:
                _this_num = _this_entry['guideline_num']
                if _this_num.count('.') == 2:
                    if guideline_num.startswith(_this_num):
                        head_line_b_text += ' - ' + _this_entry['guideline_text']
                        break

        result = self._openai.classify_guideline(major_head_line_text,
                                                 head_line_a_text,
                                                 head_line_b_text,
                                                 guideline_text, self.__name)

        data_entry['payload']['classification'] = result
        data_entry['result'][1] = 1

    ######### Perform Classification #############

    def _perform_classification(self):
        """
        Perform Classification
        """
        thread_run = Bob_UtilsThread_Object()
        thread_run.prepare_data(self._final_data, GlobalVars.prop_num_threads)
        thread_run.fire_threads_and_run_until_complete(self._single_action_classification)

    #### Consolidate ####

    def consolidate(self):
        """
        Consolidates
        """
        logging.debug('Conducts Document Consolidation .. {}'
                      .format(GlobalVars.prop_incoming_documents))
        files = UtilsFile.traverse_directory(GlobalVars.prop_file_documents_raw_cache,
                                             ext='.dat')
        for entry in files:
            self._agg_data = {}
            self._final_data = []
            self._m_headline = None
            self._h_1 = None
            self._h_2 = None
            logging.debug('Working On: {}'.format(entry[0]))
            name = entry[1].replace(".dat", "")
            if self.__file_name is not None:
                if entry[1].find(self.__file_name) == -1:
                    continue
            self.__name = name
            data = UtilsFile.load_pickle(entry[0])
            for this_data_entry in data:
                self._aggregate_sections(this_data_entry, name)
            self._prepare_data_for_classification()
            self._perform_classification()
            UtilsFile.save_pickle(GlobalVars.prop_file_documents_consolidated + entry[1],
                                  self._final_data)



