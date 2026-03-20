#!/bin/bash

_VERSION='0.2'

BIN_DIR="$HOME/.local/bin"

green="\e[1;32m"
lightgreen="\e[0m\e[32m"
red="\e[1;31m"
lred="\e[0m\e[31m"
cyan="\e[1;36m"
yellow="\e[1;33m"
orange="\e[1;38;5;214m"
blue="\e[1;34m"
default="\e[0m"

if [ -f $BIN_DIR/lsize ]
then
  echo -e "$blue $(lsize -v) already exist..$default"
  read -p " Do you want to update [y/n] : " update
  if [[ $update == 'y' ]]
  then 
    cp lsize.py $BIN_DIR/lsize
    chmod +x $BIN_DIR/lsize
    echo -e "$cyan Update Finished : $($BIN_DIR/lsize -v) $default"
  fi
  exit
fi


# check if the ~/.local/bin exists else create the dir
if [ ! -d "$BIN_DIR" ]
then
  sleep 2
  if mkdir -p ~/.local/bin;
  then
    echo -e "$default $0:$green Created $BIN_DIR...$default"
  else
    echo -e "$default $0:$red Failed to create $BIN_DIR...$default"
  fi
fi



echo -en "$default $0:$green Copying lsize to $BIN_DIR.........."

sleep 2

if cp lsize.py $BIN_DIR/lsize;
then
  echo -e "${green}Succesfull"
else 
  echo -e "$default $0:$red Copy Failed! Exiting.."
  exit 1
fi

sleep 2

if chmod +x $BIN_DIR/lsize;
then
  echo -e "$default $0:$green Made $BIN_DIR/lsize executable"
else 
  echo -e "$default $0:$red chmod +x failed! Exiting.."
  exit 1
fi


EXPORT_LINE='export PATH="$HOME/.local/bin:$PATH"'

# 1. Add to current shell if missing
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]
then
  PATH="$BIN_DIR:$PATH"
fi

# 2. Decide which startup file to modify
if shopt -q login_shell;
then
  SOURCE_FILE="$HOME/.profile"
else
  SOURCE_FILE="$HOME/.bashrc"
fi

# 3. Append only if file exists and line is not already present
if [[ -f "$SOURCE_FILE" ]]
then
  grep -Fxq "$EXPORT_LINE" "$SOURCE_FILE" || {
    printf '\n# Added by lsize\n%s\n' "$EXPORT_LINE" >> "$SOURCE_FILE"
  }
fi

source $SOURCE_FILE

sleep 2

if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]];
then
  echo -e "$default $0:$green Succesfully added $BIN_DIR to PATH.."
else
  echo -e "$default $0:$yellow Couldn't add $BIN_DIR to PATH. \n Please try manually adding $BIN_DIR to PATH"
  exit 1
fi

sleep 2

echo -e "$cyan To get started type 'lsize -h' $default"

