############################################################
# Bob Utils Error
#
#
#
############################################################

# Python Imports

import sys

# Infrastructure Imports

######### Bob Exception Object #################

class BobException(Exception):

    """
    Bob Infra Exception
    """

    # Todo: Will Be Extended In Near Future

    ################# Inits ###############

    def __init__(self, *args):
        """
        Inits
        """
        Exception.__init__(self, *args)

##################### Bob UtilsError Object ###############

class Bob_UtilsError_Object:

    """
    Inits
    """

    ##################### Inits #####################

    def __init__(self):
        """
        Inits
        """

    ################### Quits With Error ###################

    def quit_with_error(self, error_text, error_msg=2):
        """
        Quits With Error
        :return:
        """
        print("ERROR: {}".format(error_text))
        print("Quitting ..")
        sys.exit(error_msg)

    ################### Error File Not Found ###################

    def error_file_not_found(self, file_name):
        """
        Quits With Error
        :return:
        """
        self.quit_with_error("File Not Found: {}".format(file_name))

    ################### Error Directory Not Found ###################

    def error_directory_not_found(self, directory_name):
        """
        Quits With Error
        :return:
        """
        self.quit_with_error("Directory Not Found: {}".format(directory_name))

    ################### Raise Error ###################

    def raise_error(self, error_text):
        """
        Quits With Error
        :return:
        """
        raise BobException(error_text)

#################### Main Block #################

UtilsError = Bob_UtilsError_Object()
