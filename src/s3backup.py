#!/usr/bin/env python3

import logging
import argparse
from common.Mysql import Mysql
from common.S3Uploader import S3Uploader


argv_parser = argparse.ArgumentParser(prog='s3backup.sh', description='calls mysqldump and uploads results to S3')

argv_parser.add_argument("-o", "--out", dest="path_to_backup",
                       help="write backup to PATH", metavar="PATH")

argv_parser.add_argument("-a", "--action", dest="action",
                       help="backup|backup_unsafe. backup_unsafe means that your backup will not be uploaded to s3",
                       default="backup")

group = argv_parser.add_mutually_exclusive_group()

group.add_argument("-A", "--all-databases", dest="all_databases", action="store_true", 
                   help="backup all databases")

group.add_argument("-d", "--database", dest="database", help="database to backup")

argv_parser.add_argument("-b", "--bucket", dest="s3_bucket",
                       help="AWS S3 bucket name")

options = argv_parser.parse_args()


if options.action not in ["backup", "backup_unsafe"]:
    argv_parser.error("Unknown action. Available actions: backup|backup_unsafe")

if options.all_databases is not None:
    options.database = "--all-databases"

if options.database is None:
    argv_parser.error("Database is required option")

if options.action == 'backup' and options.s3_bucket is None:
    argv_parser.error("You should define s3 bucket name to upload backup")

path_to_backup = ''

try:
    path_to_backup = Mysql().backup(options.database, options.path_to_backup)
except Exception as backup_error:
    print("Error while backup process: %s" % (backup_error))
    exit()

print('Backup successfully created at %s' % path_to_backup)

if options.action == 'backup':
    try:
        S3Uploader.upload(path_to_backup, bucket=options.s3_bucket)
        print("Backup has been successfully uploaded to amazon s3 bucket")
    except Exception as upload_error:
        print("Error while uploading backup to S3: %s" % (upload_error))

