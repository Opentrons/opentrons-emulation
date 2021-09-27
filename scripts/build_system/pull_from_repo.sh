if [ "$#" -eq 3 ]; then
  REPO_NAME=$1
  BRANCH_NAME=$2
  STORAGE_DIR_NAME=$3
else
  echo "Must pass \"repo_name\", \"branch_name\", and \"storage_dir_name\""
  echo "Usage: ./pull_ot3_firmware.sh <repo_name> <branch_name> <storage_dir_name>"
  exit 1
fi

STORAGE_DIR=`(cd ../../ && pwd)`
FULL_PATH="$STORAGE_DIR/$STORAGE_DIR_NAME"

echo "Pulling branch \"$BRANCH_NAME\" from repo \"$REPO_NAME\" and storing to $FULL_PATH"
DOWNLOAD_PATH="https://github.com/Opentrons/$REPO_NAME/archive/$BRANCH_NAME.zip"

(
  cd $FULL_PATH && \
  rm -rf $REPO_NAME && \
  wget -q -O $REPO_NAME.zip "$DOWNLOAD_PATH" && \
  unzip -q $REPO_NAME.zip && \
  rm -f $REPO_NAME.zip && \
  mv $REPO_NAME* $REPO_NAME
)