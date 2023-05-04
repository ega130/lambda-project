#!/bin/bash

python utils/create_zip_files.py
terraform apply -auto-approve
