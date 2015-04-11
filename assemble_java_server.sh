#!/bin/sh

java_target_folder=./server/main/java/galen/api/server
target_java_thrift=${java_target_folder}/thrift
gen_thrift_files_folder=./target/generated-sources/thrift/galen/api/server
destination_server_folder=bin

echo "Generate thrift files"
mvn clean thrift:compile

if [ -d "${target_java_thrift}" ]; then
     rm -rf ${target_java_thrift}
fi

echo "Copy generated Java thrift files to Java target folder"
mv ${gen_thrift_files_folder}/* ${java_target_folder}

# package server into jar
echo "mvn clean package"
mvn clean package

# move server jar into bin folder
echo "Copy packaged server into bin folder"
if [ -d "${destination_server_folder}" ]; then
     rm -rf ${destination_server_folder}
fi
mkdir ${destination_server_folder}

echo "Server jar copied to /${destination_server_folder}/galen-api-server.jar"
mv -f ./target/galen-api-thrift-1.0-SNAPSHOT-jar-with-dependencies.jar ./bin/galen-api-server.jar

exit 0