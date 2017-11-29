"""
@author Bryan Hopkins pennbwh@gmail.com

This script packages up a simple python project into an AWS lambda-runnable zip.
There are better ways to do this.  This exists largely as a practical training exercise
and conceptual example.

"""

import zipfile
import os
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

modes = {
        zipfile.ZIP_DEFLATED: 'deflated',
        zipfile.ZIP_STORED:   'stored',
        }


deployfile_name = "gits3vault.zip"
# Windows value: virtualenv_dir = "./env//Lib/site-packages"
# virtualenv_dir = os.environ['VIRTUAL_ENV']
# virtualenv_source_dir = virtualenv_dir + "/lib/python2.7/site-packages"


# Walk the given virtual environment directory and find site-packages
def get_sitepackages(virtualenv_dir):
    for path, subdirs, files in os.walk(virtualenv_dir):
        for subdir in subdirs:
            if subdir[-1 * len("site-packages"):] == "site-packages":
                return path + "/" + subdir
    return "."


# Return true if the file has a .py extension
def is_python_file(filename):
    if filename is not None:
        return file[-3:] == ".py"
    return False

deployfile = zipfile.ZipFile(deployfile_name, mode="w")

try:
    all_directory_files = os.listdir(".")
    # write only the .py files
    for file in all_directory_files:
        if is_python_file(file):
            deployfile.write(file, compress_type=compression)

    virtualenv_source_dir = get_sitepackages(".")
    print("Walking directory %s for dependency files" % virtualenv_source_dir)
    for path, subdirs, files in os.walk(virtualenv_source_dir):
        for file in files:
            # if is_python_file(file):
            path_to_file = os.path.join(path, file)
            path_in_deployfile = path_to_file[len(virtualenv_source_dir)+1:]
            deployfile.write(path_to_file, path_in_deployfile, compress_type=compression)
            # deployfile.write(path_to_file, file)
finally:
    deployfile.close()

