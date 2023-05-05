"""
constants, functions and object for file-system operations
"""
#!/usr/bin/python

# import official python packages
import json
import os
from os.path import isfile, join
import sys
import logging
import shutil

# import custom python packages

log = logging.getLogger('main-logger')


def move_content(src_folder_name, dst_path):
    """
    copy files from source directory of to destination directory
    delete source directory afterwards

    similar function to copy_or_move_files_and_folder but without user-request when overwriting
    and only support for directories
    """
    # build path to old folder on the same level as wahooMapsCreator
    par_dir = os.path.abspath(os.path.join(os.path.join(
        os.path.dirname(__file__), os.pardir), os.pardir))
    source_dir = os.path.join(par_dir, src_folder_name)

    if os.path.exists(source_dir):
        # copy & delete directory
        for item in os.listdir(source_dir):
            src = os.path.join(source_dir, item)
            dst = os.path.join(dst_path, item)
            # next, if destination directory exists
            if os.path.isdir(dst):
                continue

            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        shutil.rmtree(source_dir)


def create_empty_directories(parent_dir, tiles_from_json, border_countries):
    """
    create empty directories for each tile and each country
    """
    for tile in tiles_from_json:
        outdir = os.path.join(parent_dir,
                              f'{tile["x"]}', f'{tile["y"]}')
        os.makedirs(outdir, exist_ok=True)

    for country in border_countries:
        outdir = os.path.join(parent_dir, country)
        os.makedirs(outdir, exist_ok=True)


def read_json_file_country_config(json_file_path):
    """
    read the country config (of last run) from the given json file
    """

    log.debug('-' * 80)
    log.debug('# Read country config json file')

    country_config = read_json_file_generic(json_file_path)
    if country_config == '':
        log.error('! Json file could not be opened.')
        sys.exit()

    log.debug(
        '+ Use country config file %s', json_file_path)
    log.debug('+ Read country config json file: OK')

    return country_config


def read_json_file_generic(json_file_path):
    """
    reads content of given .json file
    """
    try:
        with open(json_file_path, encoding="utf-8") as json_file:
            json_content = json.load(json_file)
            json_file.close()

        return json_content

    except FileNotFoundError:
        return {}


def write_json_file_generic(json_file_path, json_content):
    """
    writes content to .json file
    """
    # Serializing json
    json_content = json.dumps(json_content, indent=4)

    # Writing to file
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json_file.write(json_content)
        json_file.close()


def get_files_in_folder(folder):
    """
    return filenames of given folder without path as list
    """
    onlyfiles = [f for f in os.listdir(folder) if isfile(join(folder, f))]

    return onlyfiles


def delete_o5m_pbf_files_in_folder(folder):
    """
    delete .o5m and .pbf files of given folder
    """
    onlyfiles = [f for f in os.listdir(folder) if isfile(join(folder, f))]

    for file in onlyfiles:
        if file.endswith('.o5m') or file.endswith('.pbf'):
            try:
                os.remove(os.path.join(folder, file))
            except OSError:
                pass


def copy_or_move_files_and_folder(from_path, to_path, delete_from_dir=False):
    """
    copy content from source directory to destination directory
    optionally delete source directory afterwards

    similar function to move_content but with user-request when overwriting and support for files
    """
    # check if from path/file exists at all
    if os.path.exists(from_path):

        # given path is a directory
        if os.path.isdir(from_path):
            # first create the to-directory if not already there
            os.makedirs(to_path, exist_ok=True)

            for item in os.listdir(from_path):
                from_item = os.path.join(from_path, item)
                to_item = os.path.join(to_path, item)

                # copy directory
                if os.path.isdir(from_item):
                    copy_directory_w_user_input(from_item, to_item)

                # copy file
                else:
                    copy_file_w_user_input(from_item, to_item)

        # given path is a file
        else:
            copy_file_w_user_input(from_path, to_path)

        # directory
        if delete_from_dir:
            shutil.rmtree(from_path)


def copy_directory_w_user_input(from_item, to_item):
    """
    copy content from source directory to destination directory
    """
    if not os.path.isdir(to_item):
        shutil.copytree(from_item, to_item)
    else:
        val = input(f"{to_item} exists already. Overwrite? (y/n):")
        if val == 'y':
            shutil.copytree(from_item, to_item)
            log.info('! %s overwritten', to_item)
        else:
            log.debug('! %s not copied, exists already.', to_item)


def copy_file_w_user_input(from_item, to_item):
    """
    copy source file to destination file
    """
    if not os.path.isfile(to_item):
        shutil.copy2(from_item, to_item)
    else:
        val = input(f"{to_item} exists already. Overwrite? (y/n):")
        if val == 'y':
            shutil.copy2(from_item, to_item)
            log.info('! %s overwritten', to_item)
        else:
            log.debug('! %s not copied, exists already.', to_item)
