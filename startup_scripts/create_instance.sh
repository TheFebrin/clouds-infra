ZONE="europe-west3-b"
INSTANCE_NAME="machine-from-script"
IMAGE_NAME="image-$INSTANCE_NAME"

gcloud compute instances create $INSTANCE_NAME \
  --image-project=debian-cloud \
  --image-family=debian-10 \
  --zone=$ZONE \
  --machine-type=e2-micro \
  --metadata-from-file=startup-script=startup.config

# Create image from this instance
gcloud beta compute machine-images create $IMAGE_NAME \
  --source-instance=$INSTANCE_NAME \
  --source-instance-zone=$ZONE
