import os.path
import subprocess
from files_helper import FilesHelper


class Mysql:

    mysqldump_args = "-u%s -p%s %s --single-transaction --quick | gzip > %s"

    def __init__(self):
        self.mysql_config = {}
        self.__parse_my_cnf()

    def __parse_my_cnf(self):
        home_dir = os.path.expanduser("~")
        mycnf = open("%s/.my.cnf" % home_dir)

        while True:
            mycnf_line = mycnf.readline()

            if not mycnf_line:
                break

            parsed_line = mycnf_line.split('=')

            if len(parsed_line) != 2:
                continue

            self.mysql_config[parsed_line[0]] = parsed_line[1].strip(' \t\n\r')

    def __get_mysqldump_configs(self, database_name, backup_path):
        return self.mysqldump_args % (
            self.mysql_config['user'],
            self.mysql_config['password'],
            database_name,
            backup_path
        )

    def backup(self, database_name, path_to_backup=None):
        if path_to_backup is None:
            path_to_backup = FilesHelper.generate_default_sql_backup_path(database_name)

        FilesHelper.check_path_exists(path_to_backup, create_if_not_exists=True)

        mysqldump_args = self.__get_mysqldump_configs(database_name, path_to_backup)
        subprocess.call("mysqldump " + mysqldump_args, shell=True)

        FilesHelper.check_mysql_backup_file(path_to_backup)

        return path_to_backup
