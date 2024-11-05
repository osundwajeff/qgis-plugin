#!/usr/bin/env bash

qgis_setup.sh

# FIX default installation because the sources must be in "qgis-plugin" parent folder
rm -rf  /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/qgis-plugin
ln -sf /tests_directory /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/qgis-plugin
ln -sf /tests_directory /usr/share/qgis/python/plugins/qgis-plugin

pip3 install -r /tests_directory/requirements.txt
pip3 install -r /tests_directory/requirements_testing.txt