###########################################
# Bob Tool
#
#
#
###########################################

# Python Imports

import __init__
import logging

# Infrastructure Imports

from Utils import GlobalVars
from Utils.Bob_UtilsArg import Bob_Args_Object
from Controller.Raw.Bob_Raw_Data import Bob_Raw_Data
from Controller.Logic.Bob_Consolidate import Bob_Consolidate_Object
from Controller.Logic.Bob_Output import Bob_Output_Object

# Arguments

ARG_CREATE_RAW = 'createraw'
ARG_CONSOLIDATE = 'consolidate'
ARG_OUTPUT = 'output'
ARG_PAGE_RANGE = 'pagerange'
ARG_THREADS = 'threads'
ARG_FILENAME = 'filename'

#################### Bob Tool Program ###################

class Bob_Tool_Program:

    """
    Bob Tool Program
    """

    ################## Inits ###############

    def __init__(self):
        """
        Inits
        """
        self._args = Bob_Args_Object('Bob Tool')
        self.__add_arugments()
        self._args.parse_args()
        self._prog_args = self._args.prop_args

    ############## Add Arguments ############

    def __add_arugments(self):
        """
        Add Arguments
        :return:
        """
        self._args.add_argument(ARG_CREATE_RAW, required=False,
                                flag=True, help='Creates raw data')
        self._args.add_argument(ARG_PAGE_RANGE, required=False,
                                flag=False, help='Indicates page range to work on')
        self._args.add_argument(ARG_CONSOLIDATE, required=False,
                                flag=True, help='Consolidates')
        self._args.add_argument(ARG_OUTPUT, required=False,
                                flag=True, help='Output')
        self._args.add_argument(ARG_THREADS, required=False,
                                flag=False, help='Number of threads')
        self._args.add_argument(ARG_FILENAME, required=False,
                                flag=False, help='Will work only on specific file')

    ############### Set General Variables #########

    def __set_general_variables(self):
        """
        Set General Variables
        """
        self.__page_range = None
        if self._prog_args[ARG_PAGE_RANGE] is not None:
            self.__page_range = [int(x) for x in
                                 self._prog_args[ARG_PAGE_RANGE].split(",")]
        if self._prog_args[ARG_THREADS] is not None:
            GlobalVars.prop_num_threads = int(self._prog_args[ARG_THREADS])
        self.__file_name = None
        if self._prog_args[ARG_FILENAME] is not None:
            self.__file_name = self._prog_args[ARG_FILENAME]

    ############ Conduct Create Raw ##########

    def _conduct_create_raw(self):
        """
        Conducts Discovery
        :return:
        """
        logging.debug('Conducting Create Raw Data ..')
        raw_data = Bob_Raw_Data(self.__page_range,
                                self.__file_name)
        raw_data.discovery()

    ############ Conduct Consolidate ##########

    def _conduct_consolidate(self):
        """
        Conducts Discovery
        :return:
        """
        logging.debug('Conducting Consolidate ..')
        consolidate = Bob_Consolidate_Object(self.__file_name)
        consolidate.consolidate()

    ############ Conduct Output ##########

    def _conduct_output(self):
        """
        Conducts Discovery
        :return:
        """
        logging.debug('Conducting Output ..')
        output = Bob_Output_Object(self.__file_name)
        output.main_loop()


    ################### Run #################

    def run(self):
        """
        Runs
        :return:
        """
        self.__set_general_variables()
        if self._prog_args[ARG_CREATE_RAW] is True:
            self._conduct_create_raw()
            return
        if self._prog_args[ARG_CONSOLIDATE] is True:
            self._conduct_consolidate()
            return
        if self._prog_args[ARG_OUTPUT] is True:
            self._conduct_output()
            return

########################## Main Block #########################

Bob_Tool = Bob_Tool_Program()
Bob_Tool.run()
