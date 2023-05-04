#!/bin/bash

python utils/create_zip_files.py
python deploy_lambda.py
