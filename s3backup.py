#!/usr/bin/env python

from optparse import OptionParser
from common.mysql import Mysql
from common.awss3 import S3Uploader

usage = "%prog [backup|backup_unsafe] database_name [options]"

argv_parser = OptionParser(usage=usage)

argv_parser.add_option("-o", "--out", dest="path_to_backup",
                       help="write backup to PATH", metavar="PATH")

argv_parser.add_option("-a", "--action", dest="action",
                       help="backup|backup_unsafe. backup_unsafe means that your backup will not be uploaded to s3",
                       default="backup")

argv_parser.add_option("-d", "--database", dest="database",
                       help="database to backup")

argv_parser.add_option("-b", "--bucket", dest="s3_bucket",
                       help="aws s3 bucket name")

argv_parser.expand_prog_name("backup|backup_unsafe <database_name>")

(options, args) = argv_parser.parse_args()

if options.action not in ["backup", "backup_unsafe"]:
    argv_parser.error("Unknown action. Available actions: backup|backup_unsafe")

if options.database is None:
    argv_parser.error("Database is required option")

if options.action == 'backup' and options.s3_bucket is None:
    argv_parser.error("You should define s3 bucket name to upload backup")

path_to_backup = ''

try:
    path_to_backup = Mysql().backup(options.database, options.path_to_backup)
except Exception as backup_error:
    print "Error while backup process!"
    print backup_error.args[0]
    exit()

print 'Backup successfully created at %s' % path_to_backup

if options.action == 'backup':
    try:
        S3Uploader.upload(path_to_backup, bucket=options.s3_bucket)
        print "Back has been successfully uploaded to amazon s3 bucket"
    except Exception as upload_error:
        print "Error while uploading backup to aws s3:"
        print upload_error.args[0]
