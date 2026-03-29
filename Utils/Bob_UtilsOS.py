############################################################
# Bob UtilsOS
#
#
#
############################################################

# Python Imports

import os, logging, subprocess, time

# Infrastructure Imports

from Utils.Bob_UtilsError import UtilsError

##################### Bob OS Run Result ################

class Bob_OSRun_Result:

    """
    Bob OS Run Result
    """

    ###################### Inits #################

    def __init__(self, command, stdout, stderr, exit_code):
        """
        Inits
        """
        self._command = command
        self._stdout = stdout
        self._stderr = stderr
        self._exitcode = exit_code

    ################### Exit Upon Error ##########

    def exit_upon_error(self):
        """
        Exit Upon Error
        :return:
        """
        if self._exitcode != 0:
            UtilsError.quit_with_error('Command: {}\nFailed With Status Code: {}\n'
                                       'Standard Output:\n{}\nStandard Error:\n{}\n'.format(
                self.command, self.exitcode, self.stdout, self.stderr))

    ################### Properties ###############

    ### STD Out

    @property
    def stdout(self):
        """
        Stdout
        :return:
        """
        return [line.strip() for line in self._stdout.split("\n")]

    ### STD Err

    @property
    def stderr(self):
        """
        Stdout
        :return:
        """
        return [line.strip() for line in self._stderr.split("\n")]

    ### Exit Code

    @property
    def exitcode(self):
        """
        Stdout
        :return:
        """
        return self._exitcode

    ### Command

    @property
    def command(self):
        """
        Stdout
        :return:
        """
        return self._command

################ Bob UtilsOS Object ####################

class Bob_UtilsOS_Object:

    """
    Inits
    """

    KILL_PROCESS_SHELL = """ps aux | grep -i "<replace_id>" | awk '{ print("kill -9 "$2); }' | sh"""

    ##################### Inits #####################

    def __init__(self):
        """
        Inits
        """

    ################# Run Command And Wait ##########

    def run_command_and_wait(self, command, run_from=None,
                             raise_error=True):
        """
        Runs Command And Wait
        :return:
        """
        output = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                cwd=run_from,
                                text=True, shell=True)
        result = Bob_OSRun_Result(command, output.stdout,
                                     output.stderr, output.returncode)
        if raise_error is True and result.exitcode != 0:
            result.exit_upon_error()
        return result

############################ Main File #############################

UtilsOS = Bob_UtilsOS_Object()
