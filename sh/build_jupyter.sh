#!/usr/bin/env bash

set -ex

jupyter lab build
jupyter labextension install jupyter-leaflet@0.17.3 @jupyter-widgets/jupyterlab-manager