###################################
# Bob Init File
#
#
###################################

# Python Imports

import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Infrastructure Imports

from Utils.Bob_UtilsFile import UtilsFile
from Utils.Bob_UtilsError import UtilsError

# Configures Logging

import logging

# Logger : Minimum Logging For Python Libraries #

# Todo: Remove duplicated getLogger lines ...

# Let's Exclude everything!

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)
logging.getLogger('paramiko').setLevel(logging.CRITICAL)
logging.getLogger('openai').setLevel(logging.CRITICAL)
logging.getLogger('hpack').setLevel(logging.CRITICAL)
logging.getLogger('httpx').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.INFO)
logging.getLogger('pymongo').setLevel(logging.CRITICAL)
logging.getLogger('fitz').setLevel(logging.CRITICAL)
logging.getLogger('pdfplumber').setLevel(logging.CRITICAL)
logging.getLogger('pdfminer').setLevel(logging.CRITICAL)
logging.getLogger("openai").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("openai._base_client").setLevel(logging.WARNING)
logging.getLogger("httpcore.connection").setLevel(logging.WARNING)
logging.getLogger("httpcore.http11").setLevel(logging.WARNING)

# Logger : Configure Logging Printing

logging.basicConfig(format='%(asctime)s.%(msecs)d [%(module)s] '
                           '(%(levelname)s) %(message)s',
                    level=logging.DEBUG, datefmt='%Y-%m-%d %I:%M:%S')

#################### Bob Global Variables ##############

class BobGlobalVariables:

    """
    Bob Global Variables
    """

    ############### Inits ############

    def __init__(self):
        """
        Inits
        """
        if 'Bob' not in os.environ:
            raise Exception('Bob not defined inside os.environ')
        self.__user_home = str(Path.home()) + os.sep
        self.__tool_home = os.path.join(self.__user_home,
                                              'work', 'Data',
                                              'Bob') + os.sep
        self.__repo_home = os.environ['Bob']
        self.__incoming_documents = os.path.join(self.__repo_home, 'Documents') + os.sep
        self.__file_documents_raw_cache = os.path.join(self.__tool_home, 'Raw') + os.sep
        self.__file_documents_temp = os.path.join(self.__tool_home, 'Temp') + os.sep
        self.__file_documents_consolidated = os.path.join(self.__tool_home, 'Consolidated') + os.sep
        self.__file_documents_output = os.path.join(self.__tool_home, 'Output') + os.sep
        self.__prop_num_threads = 1

    ############### Properties #############

    @property
    def prop_file_documents_raw_cache(self):
        """
        Property File Documents Raw Cache
        """
        return self.__file_documents_raw_cache

    @property
    def prop_file_documents_temp(self):
        """
        Property File Documents Temp
        """
        return self.__file_documents_temp

    @property
    def prop_file_documents_consolidated(self):
        """
        Property File Documents Consolidated
        """
        return self.__file_documents_consolidated

    @property
    def prop_file_documents_output(self):
        """
        Property File Documents Output
        """
        return self.__file_documents_output

    @property
    def prop_incoming_documents(self):
        """
        Property Incoming Documents
        """
        return self.__incoming_documents

    @property
    def prop_num_threads(self):
        """
        Property Number of Threads
        """
        return self.__prop_num_threads

    @prop_num_threads.setter
    def prop_num_threads(self, value):
        """
        Property Number of Threads
        """
        self.__prop_num_threads = value = value

############### Main Block ###########3

GlobalVars = BobGlobalVariables()
