This application is a hybrid application hosted in AWS ECS on docker containers as micro-services.
The project is primarily a showcase portfolio application, leveraging docker, VueJS, GoLang, Mysql, Shell scripts, and AI Tensorflow models.

Pre-Reqs: docker and the following available ports (82, 8080, 5052 and 3306)  

Setup:
* cd into cloned repo
* `docker-compose up -d`
* Visit http://127.0.0.1:8080/
* Wait for the Vue,Go and Flask API to load in each container. 
  The Flask API will probably take the longest due to saving and compiling the AI tensorflow transer model, so
  be patient :). Later more models will be included along with an options drop-down for the user to choose which model they would like to use.

 