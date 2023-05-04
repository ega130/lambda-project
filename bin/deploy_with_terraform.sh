#!/bin/bash

python utils/create_zip_files.py
cd terraform
terraform init
terraform apply -auto-approve
cd ..
