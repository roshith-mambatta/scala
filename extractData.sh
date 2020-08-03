#!/bin/bash

CCM_HOME=/home/roshith/Desktop

extract_ot_run_details()
{
CCM_INSTANCE=$1
INSTANCE_LOG_EXTRACT_FILE=$2
groupCount=0
wrongSeqOrder=0
resultRow=""
while read line; do
if [[ "$line" == "document code::"* ]]; then
wrongSeqOrder=0
groupCount=0
resultRow="$CCM_INSTANCE;"
fi

if [ $wrongSeqOrder == 0 ] 
then
case $line in
   "document code::"*) 
   if [ $groupCount == 0 ]
   then
   resultRow+="$(echo $line|grep -oP "document code::* \K.*")"";"
   groupCount=1
   else
   wrongSeqOrder=1
   fi;;
   "No of pages ::"*) 
   if [ $groupCount == 1 ]
   then
   resultRow+="$(echo $line|grep -oP "No of pages ::* \K.*")"";"
   groupCount=2
   else
   wrongSeqOrder=1
   fi;;
   "Date ::"*) 
   if [ $groupCount == 2 ]
   then
   resultRow+="$(echo $line|grep -oP "Date ::* \K.*")"
   echo $resultRow>>/tmp/CCM_run_details.csv
   groupCount=0
   resultRow=""
   else
   wrongSeqOrder=1
   fi;;
   *) echo "";;
esac
fi
done < $INSTANCE_LOG_EXTRACT_FILE
}


echo "List CCM instances  ......<"
cd $CCM_HOME/CCM_services

for instance_name in $(ls -d */ | cut -f1 -d'/')
do
  echo $CCM_HOME/CCM_services/$instance_name
  if [ $instance_name == "EDITIQ" ]
  then
  cd $CCM_HOME/CCM_services/$instance_name/logs
  else
  cd $CCM_HOME/CCM_services/$instance_name/output
  fi
  egrep -h "No of pages|document code|Date ::" *.log>/tmp/extract.txt
  extract_ot_run_details $instance_name /tmp/extract.txt
done
echo "List CCM instances  ......<"

