import os.path
import gzip
import time
import sys


class FilesHelper:
    def __init__(self):
        pass

    @staticmethod
    def check_path_exists(path, create_if_not_exists=False):
        path_array = path.strip('/').split('/')
        current_parent_dir = ''
        path_array.pop()
        while len(path_array) > 0:
            current_parent_dir += '/' + path_array.pop(0)
            if not os.path.isdir(current_parent_dir):
                if create_if_not_exists:
                    os.mkdir(current_parent_dir)
                else:
                    return False

    @staticmethod
    def check_mysql_backup_file(path_to_backup):
        if not os.path.isfile(path_to_backup):
            raise Exception('Error while creating backup. File %s doesnt created' % path_to_backup)

        backup_file = gzip.open(path_to_backup)

        backup_part = backup_file.read(10240)

        if backup_part.find('CREATE TABLE') == -1 or backup_part.find('INSERT INTO') == -1:
            raise Exception('Backup file is broken')

    @staticmethod
    def generate_default_sql_backup_path(database_name):
        current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        return "%s/backup/%s_%s.sql.gz" % (
            current_dir,
            database_name,
            time.strftime('%Y_%m_%d_%H_%M_%S')
        )
