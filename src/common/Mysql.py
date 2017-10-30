import os.path
import subprocess
from .files_helper import FilesHelper


class Mysql:

    mysqldump_args = "%s --single-transaction --quick | gzip > %s"

    def __init__(self):
        self.mysql_config = {}

    def __get_mysqldump_configs(self, database_name, backup_path):
        return self.mysqldump_args % (
            database_name,
            backup_path
        )

    def backup(self, database_name, path_to_backup=None):

        database_file = database_name
        if (database_name == "--all-databases"):
            database_file = "all-databases"
        
        if path_to_backup is None:
            path_to_backup = FilesHelper.generate_default_sql_backup_path(database_file)

        FilesHelper.check_path_exists(path_to_backup, create_if_not_exists=True)

        mysqldump_args = self.__get_mysqldump_configs(database_name, path_to_backup)
        subprocess.run("mysqldump " + mysqldump_args, shell=True)

        FilesHelper.check_mysql_backup_file(path_to_backup)

        return path_to_backup
