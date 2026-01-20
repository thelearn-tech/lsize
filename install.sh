#!/bin/bash

_VERSION='0.1'

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

if [ ! -d $BIN_DIR ]; 
then
  echo -e "$default $0:$green Created $BIN_DIR..."
fi


echo -e "$default $0:$green Copying lsize to $BIN_DIR"

if cp lsize.py $BIN_DIR/lsize;
then
  echo -e "$default $0:$green Copying succesfull..."
else 
  echo -e "$default $0:$red Copy failed! Exiting.."
  exit 1
fi

if chmod +x $BIN_DIR/lsize;
then
  echo -e "$default $0:$green Made $BIN_DIR/lsize executable"
else 
  echo -e "$default $0:$red chmod +x failed! Exiting.."
  exit 1
fi


EXPORT_LINE='export PATH="$HOME/.local/bin:$PATH"'

# 1. Add to current shell if missing
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
  PATH="$BIN_DIR:$PATH"
fi

# 2. Decide which startup file to modify
if shopt -q login_shell; then
  TARGET="$HOME/.profile"
else
  TARGET="$HOME/.bashrc"
fi

# 3. Append only if file exists and line is not already present
if [[ -f "$TARGET" ]]; then
  grep -Fxq "$EXPORT_LINE" "$TARGET" || {
    printf '\n# Added by lsize\n%s\n' "$EXPORT_LINE" >> "$TARGET"
  }
fi

source $TARGET

if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]];
then
  echo -e "$default $0:$green Succesfully added $BIN_DIR to PATH.."
else
  echo -e "$default $0:$yellow Couldn't add $BIN_DIR to PATH. \n Please try manually adding $BIN_DIR to PATH"
  exit 1
fi

echo -e "$cyan To get started type 'lsize -h'"

