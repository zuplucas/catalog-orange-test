#!/bin/sh

runFormula() {
  echo "***********************************************************"
  echo "* Running with credentials                                 "
  echo "* USERID: $CREDENTIAL_AWS_CALLERUSERID "
  echo "* ARN: $CREDENTIAL_AWS_CALLERARN "
  echo "* ACCOUNT ID: $CREDENTIAL_AWS_CALLERACCOUNT "
  echo "* ACCOUNT NAME: $CREDENTIAL_AWS_ACCOUNTNAME "
  echo "***********************************************************"

  BUCKET=$NAME_BUCKET
  echo Inside /data ...
  cd /data
  echo Ziping files ....
  sudo zip -r $NAME_FILE.zip ./template
  echo Copying to s3 ...
  aws s3 cp "$NAME_FILE.zip" s3://$BUCKET
  echo Printing results...
  echo ::output url_download = "http://downloads.catalog.orangestack.com/?file=$NAME_FILE.zip"
}

