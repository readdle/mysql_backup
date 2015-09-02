# MySQL backup and s3 upload script

# How to use

- yum install s3cmd
- configure ~/.s3cfg file
- add database credentials to ~/.my.cnf
- add to cron: python /path/to/script/s3backup.py --action=backup --database=database_name --bucket=s3_bucket_name

# Requires:

- Python 2.6

# Additional

```sh
python s3backup.py --help
```

