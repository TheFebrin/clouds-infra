ZONE="europe-west3-c"
# TEMPLATE="chmurki-template-from-config"
TEMPLATE="chmurki-template-from-image-ip"
# SIZE=3
SIZE=1
GROUP_NAME="backup-group-ip"

gcloud compute instance-groups managed create $GROUP_NAME \
    --base-instance-name backup-group-machine-from-image \
    --size $SIZE \
    --template $TEMPLATE \
    --zone=$ZONE \
    # --target-pool chmurki-pool

gcloud compute instance-groups managed set-autoscaling $GROUP_NAME \
  --zone=europe-west3-c \
  --max-num-replicas=3
