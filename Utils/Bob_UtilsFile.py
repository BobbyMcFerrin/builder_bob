############################################################
# Bob UtilsFile
#
#
#
############################################################

# Python Imports

import os, shutil, shlex, pickle
from pathlib import Path

# Infrastructure Imports

from Utils.Bob_UtilsData import UtilsData
from Utils.Bob_UtilsError import UtilsError

##################### Bob UtilsFile Object ###############

class Bob_UtilsFile_Object:

    """
    Inits
    """

    ##################### Inits #####################

    def __init__(self):
        """
        Inits
        """

    ################# File Exists ##################

    def is_file_exists(self, file_name, raise_error=True):
        """
        File Exists
        :param file_name:
        :return:
        """
        if isinstance(file_name, str) is False:
            UtilsError.raise_error('Wrong value for file_name: {}'.format(file_name))
        result = os.path.exists(file_name)
        if raise_error is False:
            return result
        else:
            if result is False:
                UtilsError.error_file_not_found(file_name)
            return True

    ################# File Exists ##################

    def is_directory_exists(self, directory_name,
                            raise_error=True,
                            create_if_not_exists=False):
        """
        Directory Exists
        :param file_name:
        :return:
        """
        result = os.path.isdir(directory_name)
        if raise_error is False:
            if result is False and create_if_not_exists is True:
                try:
                    os.makedirs(directory_name, exist_ok=True)
                    result = True
                except Exception:
                    UtilsError.quit_with_error('Could not create: {}'
                                               .format(directory_name))
            return result
        else:
            if result is False:
                UtilsError.error_directory_not_found(directory_name)
            return True

    ################# Read File Stripped Lines ###########

    def read_file_lines(self, file_name, strip=False,
                        ignore_comment=False,
                        ignore_empty_lines=False):
        """
        Reads File Stripped Lines
        :param file_name:
        :return:
        """
        lines = []
        with open(file_name, 'r', encoding='utf-8') as file_handler:
            for line in file_handler:
                if strip is True:
                    line = line.strip()
                if ignore_comment is True:
                    if line.startswith('#') is True:
                        continue
                if ignore_empty_lines is True:
                    if len(line) == 0:
                        continue
                lines.append(line)
        return lines

    ################# Read Basic Config ##################

    def read_basic_config(self, config_file):
        """
        Directory Exists
        :param file_name:
        :return:
        """
        # Reads A Basic Config File (KeyValue Based)
        # Todo: Consider applying here check if file exists
        config = {}
        lines = self.read_file_lines(config_file,
                                     strip=True, ignore_comment=True,
                                     ignore_empty_lines=True)
        for line in lines:
            if line.find('=') == -1:
                UtilsError.quit_with_error(
                    'Config line without "=" operator: {}'.format(line))
            split_1 = line.split("=")
            config[split_1[0].strip()] = UtilsData.eval_value(split_1[1].strip()
                                                              .replace("\042", ""))
        return config

    ################# Read Basic Config ##################

    def read_ini_config(self, config_file):
        """
        Directory Exists
        :param file_name:
        :return:
        """
        # Reads A Basic Config File (KeyValue Based)
        # Todo: Consider applying here check if file exists
        lines = self.read_file_lines(config_file,
                                     strip=True, ignore_comment=True,
                                     ignore_empty_lines=True)
        config = {}
        current_section = None
        for line in lines:
            if not line:
                continue
            if line.startswith('[') and line.endswith(']'):
                section_name = line[1:-1].strip()
                if section_name in config:
                    UtilsError.quit_with_error('Bad INI File: {} (section {} already exists)'
                                               .format(config_file, section_name))
                current_section = section_name
                config[current_section] = {}
            else:
                if current_section is None:
                    UtilsError.quit_with_error('Bad INI File: {}'.format(config_file))
                split_1 = line.split('=')
                this_key = split_1[0].strip()
                if this_key in config[current_section]:
                    UtilsError.quit_with_error('Configfile: key_name '
                                               'already defined for section: {}/{}'
                                               .format(current_section, this_key))
                config[current_section].setdefault(this_key,
                                                   UtilsData.eval_value(split_1[1]
                                                                        .strip()))
        return config

    ################# Write File Lines ###########

    def write_file_lines(self, file_name, data):
        """
        Writes File Lines
        :param file_name:
        :return:
        """
        with open(file_name, 'w') as file_handler:
            for line in data:
                file_handler.write(line.rstrip("\n") + '\n')

    #################### Write Text Lines To File ###############

    def write_textlines_to_file(self, file_name, lines):
        """
        Write TextLines To File
        :param file_name:
        :param lines:
        :return:
        """
        with open(file_name, 'w') as file_handler:
            for line in lines:
                file_handler.write(line + '\n')

    #################### Deletes File #############

    def delete_file(self, file_name, raise_error=True):
        """
        Deletes File
        :return:
        """
        try:
            os.remove(file_name)
        except FileNotFoundError:
            if raise_error is True:
                UtilsError.raise_error('Delete file: not exists: {}'
                                       .format(file_name))
            return False
        except PermissionError:
            if raise_error is True:
                UtilsError.raise_error('Delete file: permission error: {}'
                                       .format(file_name))
            return False
        except Exception as e:
            if raise_error is True:
                UtilsError.raise_error('Delete file: general error: {} -> {}'
                                       .format(file_name, e.__str__()))
                return False
        return True

    ########## Delete Directory Contents  ########

    def delete_directory_contents(self, directory_name, raise_error=True):
        """
        Deletes Directory Contents
        :return:
        """
        # Todo: This is not directory recursive
        for file_name in os.listdir(directory_name):
            full_name = os.path.join(directory_name, file_name)
            self.delete_file(full_name, raise_error=raise_error)

    #################### Copy File ###############

    def copy_file(self, source, dest):
        """
        Write TextLines To File
        :param file_name:
        :param lines:
        :return:
        """
        # Todo: Better formulate Error
        if os.path.isdir(dest) is True:
            # Supporting if target is directory
            base_file_name = os.path.basename(source)
            target_file_name = dest + os.sep + base_file_name
        else:
            target_file_name = dest
        try:
            shutil.copy(source, target_file_name)
        except Exception as e:
            UtilsError.raise_error(e.__str__())
        return True

    #################### Travereses Directory ###############

    def traverse_directory(self, directory, ext=None,
                           ignore_files=None):
        """
        Traverses Directory
        :param file_name:
        :param lines:
        :return:
        """
        if ext:
            ext = '.' + ext.lstrip('.')
        result = []
        for root, _, files in os.walk(directory):
            for file_name in files:
                cond = True
                if ext is not None:
                    if not file_name.endswith(ext):
                        cond = False
                if cond is True and ignore_files is not None:
                    if file_name in ignore_files:
                        cond = False
                if cond:
                    result.append([os.path.join(root, file_name),
                                  file_name])
        return result

    ################ Save Pickle ################

    def save_pickle(self, file_name, data):
        """
        Saves Pickle
        """
        with open(file_name, 'wb') as file_handler:
            pickle.dump(data, file_handler, 2)

    ################ Load Pickle ################

    def load_pickle(self, file_name, not_found_return_empty=False):
        """
        Load Pickle
        """
        try:
            with open(file_name, 'rb') as file_handler:
                return pickle.load(file_handler)
        except Exception as e:
            if e.__str__().find('No such file or directory') != -1:
                if not_found_return_empty is True:
                    return {}
            UtilsError.quit_with_error('Could not load pickle file: {} : {}'
                                       .format(file_name, e.__str__()))

#################### Main Block #################

UtilsFile = Bob_UtilsFile_Object()
