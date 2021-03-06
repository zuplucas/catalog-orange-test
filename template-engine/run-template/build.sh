#!/bin/sh

BINARY_NAME=run.sh
BINARY_NAME_WINDOWS=run.bat
BIN_FOLDER=bin

#python-build:
	mkdir -p $BIN_FOLDER
	cp -r src/* $BIN_FOLDER

#sh_unix:
	{
	echo "#!/bin/bash"
	echo "python3 \$(dirname \"\$0\")/main.py"
	} >> $BIN_FOLDER/$BINARY_NAME
	chmod +x $BIN_FOLDER/$BINARY_NAME

#bat_windows:
	{
	echo "@ECHO OFF"
	echo "python main.py"
	} >> $BIN_FOLDER/$BINARY_NAME_WINDOWS

#docker:
	cp Dockerfile set_umask.sh $BIN_FOLDER
