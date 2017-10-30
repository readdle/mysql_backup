# MySQL backup and S3 upload script

# How to use

- install python3-venv (if needed)
- run install.sh (to download python modules)
- S3: use IAM roles or create standard AWS credentials files (~/.aws/credentials)
```
[default]
aws_access_key_id=foo
aws_secret_access_key=bar
```

- add database credentials to ~/.my.cnf
- add to cron: /bin/sh /path/to/script/s3backup.sh --action=backup --all-databases --bucket=s3_bucket_name

# Requires:

- Python 3

# Additional

```sh
s3backup.sh --help
```

