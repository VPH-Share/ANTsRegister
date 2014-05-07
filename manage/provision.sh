#!/bin/bash
set -o nounset
set -o errexit
shopt -s expand_aliases
#######################################
# Source helper utilities
source manage/utils.sh
log "Updating OS packages"
pkgupdate
log "Setting GB locale"
setlocales
#######################################
log  "Installing ANTsRegister commandline application"
sudo mkdir -p $REPO_DIR/vendors
curl -L -o $REPO_DIR/vendors/ANTs-1.9.v4-Linux.tar.gz http://downloads.sourceforge.net/project/advants/ANTS/ANTS_Latest/ANTs-1.9.v4-Linux.tar.gz
sudo tar xzf $REPO_DIR/vendors/ANTs-1.9.v4-Linux.tar.gz -C vendors
#######################################
log "Installing SOAPlib Commandline Wrapper dependencies"
pkginstall python-pip
pkginstall python-dev python-lxml
sudo pip install -r $REPO_DIR/manage/requirements.txt
#######################################
log "Configure SOAPLib to autostart"
sudo cat $REPO_DIR/manage/initd.antsregister > /etc/init.d/antsregister
sudo chmod +x /etc/init.d/antsregister
sudo update-rc.d antsregister defaults
#######################################
log "Starting application"
sudo service antsregister start
#######################################
log "Cleaning up..."
pkgclean
pkgautoremove
history -c
#######################################
