#!/usr/bin/env bash
set -o errexit

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  ar x google-chrome-stable_current_amd64.deb
  tar xvf data.tar.xz
fi

# Clean up any old sessions to save memory
rm -rf /tmp/.com.google.Chrome.*

cd /opt/render/project/src
pip install --upgrade pip
pip install -r requirements.txt
