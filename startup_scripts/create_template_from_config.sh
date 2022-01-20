gcloud compute instance-templates create chmurki-template-from-config \
  --metadata-from-file=startup-script=startup.config
