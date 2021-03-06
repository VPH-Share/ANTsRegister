#!/bin/bash
set -o nounset
set -o errexit
shopt -s expand_aliases
#######################################
# Source helper utilities
source manage/utils.sh
log "Updating OS packages"
pkgupdate
#######################################
log "Stopping application"
sudo service antsregister stop
#######################################
log "Deconfigure SOAPLib to autostart"
sudo update-rc.d antsregister disable
sudo rm /etc/init.d/antsregister
#######################################
log "Uninstalling SOAPlib Commandline Wrapper dependencies"
sudo pip uninstall -r $REPO_DIR/manage/requirements.txt
pkgremove python-dev python-lxml
pkgremove python-pip
#######################################
sudo rm -rf /webapp
