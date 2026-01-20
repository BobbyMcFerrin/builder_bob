#############################
# Bob Raw Data
#
#
#
#############################

# Python Imports

import logging, base64, time
import fitz

from pprint import pprint

# Infrastructure Imports

from Utils import GlobalVars
from Utils.Bob_UtilsFile import UtilsFile
from Utils.Bob_UtilsOS import UtilsOS
from Utils.Bob_UtilsThread import Bob_UtilsThread_Object
from Controller.Logic.Bob_OpenAI import Bob_AI_Object

#################### Bob AI Parser Object #####################

class Bob_AI_Parser_Object:

    """
    Bob Raw Data
    """

    #### Inits ####

    def __init__(self, file_path, page_range):
        """
        Inits
        """
        UtilsFile.delete_directory_contents(GlobalVars.prop_file_documents_temp)
        logging.debug('Initializing Bob AI Parser ..')
        self.__page_range = page_range
        if self.__page_range is not None:
            logging.debug('Using Custom Page Range: {}'
                          .format(self.__page_range))
            self.__page_range = [self.__page_range[0],
                                 self.__page_range[1]]
        self.__file_path = file_path
        self._fitz = fitz.open(file_path)
        self._image_cmd = self._image_command = UtilsOS.run_command_and_wait('which pdftoppm').stdout[0]
        self._openai = Bob_AI_Object()

    #### Single Page Parser AI Action ####

    def _single_page_parser_action(self, data_entry):
        """
        Single Page Parser AI Action
        """

        page_number = data_entry['payload']['page_number']
        target_file = GlobalVars.prop_file_documents_temp + 'page'
        _this_command = '/usr/bin/pdftoppm -png -r 300 -f {} -l {} {} {}'.format(page_number, page_number,
                                                                                 self.__file_path, target_file)
        logging.debug('Generating Image For Page: {}'.format(page_number))
        UtilsOS.run_command_and_wait(_this_command)
        with open(target_file + '-{}.png'.format(str(page_number).zfill(3)),
                  'rb') as image_file:
            png_bytes = image_file.read()
        png_base64 = base64.b64encode(png_bytes).decode("utf-8")
        ai_result = self._openai.get_page_structure_and_text_from_base64_image(png_base64)
        data_entry['result'][0] = [ai_result, page_number]
        data_entry['result'][1] = 1
        return ai_result

    #### Conduct AI Parsing ####

    def conduct_ai_parsing(self):
        """
        Conduct AI Parsing
        """
        now = time.time()
        thread_run = Bob_UtilsThread_Object()
        data = []
        all_pages = []
        for page in self._fitz:
            page_number = page.number + 1
            if self.__page_range is not None:
                if (page_number < self.__page_range[0]
                        or page_number > self.__page_range[1]):
                    continue
            all_pages.append(page_number)
            data.append({'page_number': page_number})
        thread_run.prepare_data(data, GlobalVars.prop_num_threads)
        result = thread_run.fire_threads_and_run_until_complete(self._single_page_parser_action)
        final_data = []
        # Ordering For Maximum Safety!
        for page in all_pages:
            for entry in result:
                if entry[1] == page:
                    final_data.append(entry[0])
        logging.debug('Total Time: {}'.format(round((time.time() - now), 4)))
        return final_data