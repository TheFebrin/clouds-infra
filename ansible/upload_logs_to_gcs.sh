#!/bin/bash

# PATH="$PATH":/bin/gsutil/ 

echo "Cron started:  $(date +"%Y %m %d %I %M %p")"

# /usr/bin/gcloud
gsutil cp /var/log/nginx/access.log gs://http-servers-logs/"$HOSTNAME"_"$(date +"%Y_%m_%d_%I_%M_%p")".log

echo "Cron finished: $(date +"%Y %m %d %I %M %p")"