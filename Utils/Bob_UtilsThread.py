############################################################
# Bob UtilsThread
#
#
#
############################################################

# Python Imports

import os, logging, subprocess, time
from threading import Thread

# Infrastructure Imports

from Utils.Bob_UtilsError import UtilsError

############### Bob UtilsThread Object ####################

class Bob_UtilsThread_Object:

    """
    Bob UtilsThread Object
    """

    ##################### Inits #####################

    def __init__(self):
        """
        Inits
        """

    ################# Prepare Data ##################

    def prepare_data(self, data, num_of_threads):
        """
        Prepare Data
        """
        self.__thread_groups = {}
        self.__total = 0
        this_thread = -1
        for i in range(0, len(data)):
            this_thread += 1
            self.__total += 1
            self.__thread_groups.setdefault(this_thread, [])
            self.__thread_groups[this_thread].append({
                'payload': data[i],
                'result': [None, -1]})

            if this_thread >= num_of_threads:
                this_thread = -1


    ################# Thread Func ########################

    def _thread_func(self, callback, index):
        """
        Thread Func
        """
        for entry in self.__thread_groups[index]:
            callback(entry)
        return True

    ################# Fire Threads And Run Until Complete ############

    def fire_threads_and_run_until_complete(self, callback):
        """
        Fire Threads and Run until Complete
        """
        for this_group in self.__thread_groups:
            thread = Thread(target=self._thread_func, args=(callback, this_group))
            thread.daemon = True
            thread.start()
            time.sleep(0.1)
        is_done = False
        while not is_done is True:
            is_done = True
            num_done = 0
            for this_group in self.__thread_groups:
                for entry in self.__thread_groups[this_group]:
                    if entry['result'][1] == -1:
                        is_done = False
                    else:
                        num_done += 1
            if not is_done:
                logging.debug('Threading Done: {} / {}'.format(num_done, self.__total))
                time.sleep(3)
        logging.debug('Threading Done.')
        this_data = []
        for this_group in self.__thread_groups:
            for entry in self.__thread_groups[this_group]:
                this_data.append(entry['result'][0])
        return this_data




