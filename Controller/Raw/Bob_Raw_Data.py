#############################
# Bob Raw Data
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
from Controller.Raw.Bob_AI_Parser import Bob_AI_Parser_Object

#################### Bob Raw Data #####################

class Bob_Raw_Data:

    """
    Bob Raw Data
    """

    #### Inits ####

    def __init__(self, page_range, this_file=None):
        """
        Inits
        """
        logging.debug('Initializing Bob Raw Data ..')
        self.__this_file = this_file
        self.__page_range = page_range
        if self.__page_range is not None:
            logging.debug('Using Custom Page Range: {}'
                          .format(self.__page_range))
            self.__page_range = [self.__page_range[0],
                                 self.__page_range[1]]

    #### Discovery ####

    def discovery(self):
        """
        Discovery
        """
        logging.debug('Conducts Document Discovery From -> {}'
                      .format(GlobalVars.prop_incoming_documents))
        files = UtilsFile.traverse_directory(GlobalVars.prop_incoming_documents,
                                             ext='.pdf')
        for entry in files:
            if self.__this_file is not None:
                if entry[1].find(self.__this_file) == -1:
                    continue
            logging.debug('Working On: {}'.format(entry[1]))
            parser = Bob_AI_Parser_Object(entry[0], self.__page_range)
            result = parser.conduct_ai_parsing()
            UtilsFile.save_pickle(GlobalVars.prop_file_documents_raw_cache + entry[1].replace(".pdf", ".dat"),
                                  result)

