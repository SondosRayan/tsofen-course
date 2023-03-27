# Dockerizing my Project

## virtualenv

- [virtualenv](https://virtualenv.pypa.io/en/latest/) is a better version of [venv](https://docs.python.org/3/library/venv.html)
- Install **virtualenv** as explained [here](https://virtualenv.pypa.io/en/latest/installation.html), or:  
**sudo apt install python-virtualenv**
- Create a local virtual environment called myvenv here:  
**virtualenv myvenv**
- Activate the new virtual environment:  
**source myvenv/bin/activate**

## Install

- install the following:
**pip install boto3**
**pip install docx2pdf**
(this will install boto3 and docx2pdf on your local environment)
- You can now run the app by:  
**python view.py**  

## Dockerize the Project

- run **pip freeze > requirements.txt**  
(note that we could save this file in git - to really freeze out dependencies versions)
- Build a docker image in the current directory:  
**docker build . -t sondosrayan/myProject**
- Run the container (detached), exposing the port:  
**docker run -d sondosrayan/myProject**
- Push the image to the dockerHub
**docker push sondosrayan/myProject**
- if you want to pull the image just run this command:
**docker pull sondosrayan/myProject**