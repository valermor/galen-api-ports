#!/bin/sh

# Generate _thrift Java files inside the target folder (see pom.xml outputDirectory)
echo "mvn clean thrift:compile"
mvn clean thrift:compile
echo "rm -rf ./src/main/java/galen/api/server/thrift"
rm -rf ./src/main/java/galen/api/server/thrift
echo "mv ./target/generated-sources/thrift/galen/api/server/* ./src/main/java/galen/api/server/"
mv ./target/generated-sources/thrift/galen/api/server/* ./src/main/java/galen/api/server/

# package server into jar
echo "mvn clean package"
mvn clean package

# move server jar into bin folder
echo "rm -rf bin"
rm -rf bin
echo "bin"
mkdir bin

echo "mv -f ./target/galen-api-thrift-1.0-SNAPSHOT-jar-with-dependencies.jar ./bin/galen-api-server.jar"
mv -f ./target/galen-api-thrift-1.0-SNAPSHOT-jar-with-dependencies.jar ./bin/galen-api-server.jar