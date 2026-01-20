#############################
# Bob Arg Utils
#
#
#
#############################

# Python Imports

import argparse

# Arg Utils

class Bob_Args_Object:

    """
    Bob Args Object
    """

    #### Inits ####

    def __init__(self, headline):
        """
        Inits
        """
        self.__prog_args = None
        self._argparse = argparse.ArgumentParser(description=headline)

    #### Adds Argument ####

    def add_argument(self, argument_name, required=False,
                     help='', flag=False):
        """
        Adds an arguement via argparse
        :param required:
        :param help:
        :return:
        """
        # Todo: Refactor
        if flag is False:
            self._argparse.add_argument('--{}'.format(argument_name),
                                        required=required, help=help)
        else:
            self._argparse.add_argument('--{}'.format(argument_name),
                                        required=required, help=help, action='store_true')

    #### Parse Args ####

    def parse_args(self):
        """
        Parse Args
        """
        self.__prog_args = vars(self._argparse.parse_args())

    #### Parse Comma Args ####

    def parse_comma_args(self):
        """
        Parses Commas Args
        """
        self.parse_args()

    #### Properties ####

    @property
    def prop_args(self):
        """
        Property: Args
        """
        return self.__prog_args
