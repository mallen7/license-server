aws rds create-db-instance \
    --db-instance-identifier license-db \
    --allocated-storage 20 \
    --db-instance-class db.t2.micro \
    --engine mariadb \
    --master-username licenseusr \
    --master-user-password x4XtNHDJfPF8WWnhDQDmAUpn \
    --backup-retention-period 7 \
    --no-publicly-accessible
