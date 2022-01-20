ZONE="europe-west3-b"
VMNAME="test-machine-from-machine-image"
IMAGE_NAME="image-machine-from-script"


# gcloud beta compute instances create $VMNAME \
#   --zone=$ZONE \
#   --source-machine-image=$IMAGE_NAME


gcloud compute instances create machine-from-standard-image \
    --image=chmurki-image-machine-from-script \
    --machine-type=e2-micro \
    --zone=$ZONE \
