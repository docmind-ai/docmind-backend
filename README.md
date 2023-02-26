# docmind-backend

This project provides a serverless docmind backend as an API endpoint

Using [Zappa](https://github.com/Miserlou/Zappa), the Python files are uploaded into Amazon's S3 storage, while Amazon Lambda runs any called functions.

# installation

Install Python 3.8, then run the below

$> pipenv shell
$> pip install -r requirements.txt

# run in local

$> pipenv shell
$> flask run

# Deployment

You will need to add credentials using aws-cli to deploy and then run below

$> pipenv shell
$> zappa deploy # if no backend exists on AWS
$> zappa update # if a backend already exists on AWS

