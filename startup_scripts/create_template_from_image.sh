gcloud compute instance-templates create chmurki-template-from-image-ip \
    --image=chmurki-image-machine-from-script \
    --machine-type=e2-micro \
    --address=34.141.42.255 \
