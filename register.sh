#!/bin/bash
TOOLPATH=tool/dClayTool.sh

echo
echo "***"
echo "*** Creating account \`bsc\`"
echo "***"
$TOOLPATH NewAccount bsc password


echo
echo "***"
echo "*** Creating a new DataContract called \`dstest\`"
echo "***"
$TOOLPATH NewDataContract bsc password dstest bsc

echo
echo "***"
echo "*** Registering all the data model_mf2c in ./model_mf2c"
echo "***"
$TOOLPATH NewModel bsc password model_mf2c ./model_mf2c python

echo
echo "***"
echo "*** Getting stubs and putting them in ./src/stubs"
echo "***"
rm -rf ./src/stubs
$TOOLPATH GetStubs bsc password model_mf2c ./src/stubs

echo
echo "***"
echo "*** Storing settings in ./cfgfiles/session.properties"
echo "***"
cat << EOF > ./cfgfiles/session.properties
Account=bsc
Password=password
StubsClasspath=$PWD/src/stubs
DataSets=dstest
DataSetForStore=dstest
DataClayClientConfig=$PWD/cfgfiles/client.properties
LocalBackend=DS1
EOF

