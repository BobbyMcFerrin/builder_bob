############################################################
# Bob UtilsData
#
#
#
############################################################

# Python Imports

import os, re, hashlib, re
import random
import inspect
import importlib.util
from datetime import datetime, timedelta

# Infrastructure Imports

##################### Bob UtilsData Object ###############

class Bob_UtilsData_Object:

    """
    Inits
    """

    ##################### Inits #####################

    def __init__(self):
        """
        Inits
        """

    ################### Eval Value ###################

    def eval_value(self, value):
        """
        User Home
        :return:
        """
        try:
            v = int(value)
        except Exception:
            try:
                v = float(value)
            except Exception:
                _value = str(value)
                if _value.strip().lower() == 'true':
                    v = True
                elif _value.strip().lower() == 'false':
                    v = False
                else:
                    v = _value
                return v
        if v is None:
            raise Exception('Unexpected.')
        return v

    ############### Convert PDF Date String To Epoch ############

    def convert_pdf_date_string_to_epoch(self, date_string):
        """
        Convert PDF Date String To Epoch
        """
        clean = date_string[2:]  # Remove "D:"
        dt_str = clean[:14]  # "20220406132416"
        tz_str = clean[14:].replace("'", "")  # "+0300"

        dt = datetime.strptime(dt_str + tz_str, "%Y%m%d%H%M%S%z")
        return int(dt.timestamp())

    ############### Get Count Of Dots And Numbers ################

    def get_count_of_dots_and_numbers(self, value):
        """
        Get Count Of Dots And Numbers
        """
        number_sequences_count = len(re.findall(r'\d+', value))
        number_of_dots = value.count(".")
        return number_of_dots, number_sequences_count

    ############## Extract Dotted Numbers #######################

    def extract_dotted_numbers(self, value):
        """
        Extract dotted number sequences like 1.1, 1.1., 3.2.1, etc.
        """
        return re.findall(r'\d+(?:\.\d+)+\.?', value)

    ############## Is Number ###################################

    def is_number(self, value):
        """
        Is INumber
        """
        try:
            _ = float(value)
            return True
        except Exception:
            return False

    ############ Extract Section Number ############

    def extract_section_number(self, text):
        """

        """
        text = text.strip()

        # Pattern for section numbers: digits with optional dots (e.g., 1, 1.6, 7., .1, 1.2.3)
        section_pattern = r'\.?\d+(?:\.\d+)*\.?'

        # Find at start
        start_match = re.match(rf'^({section_pattern})\s*', text)
        # Find at end
        end_match = re.search(rf'\s*({section_pattern})$', text)

        section_num = None
        cleaned = text

        if start_match:
            section_num = start_match.group(1).strip('.')
            cleaned = text[start_match.end():]

        if end_match:
            end_num = end_match.group(1).strip('.')
            # Use end number if no start, or if they match (duplicate)
            if section_num is None:
                section_num = end_num
            cleaned = cleaned[:end_match.start() - (len(text) - len(cleaned))] if start_match else text[
                :end_match.start()]

        # Clean up any remaining whitespace
        cleaned = cleaned.strip()

        return cleaned, section_num


#################### Main Block #################

UtilsData = Bob_UtilsData_Object()
