#!/bin/sh

project_name=galen-api-ports

function cd_parent_to_project_folder()
{
  while [[ $PWD != '/' && ${PWD##*/} != ${project_name} ]]; do cd ..; done
}

cd_parent_to_project_folder

cd ./bin

java -jar galen-api-server.jar -r $@