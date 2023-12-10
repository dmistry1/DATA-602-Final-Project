# Data Science 602 Project
#### Authors: Brad Scott, Deep Mistry

This project shows the number of active fires in Maui and predict if weather conditions are likely to produce active fires. This utilizes satellite data from NASA Fire Information for Resource Management System (FIRM) and weather data from National Oceanic and Atmospheric Administration (NOAA). 

## Local Setup
### Prerequisites 
- node version: `21.1.0`
- `python3`
- `Docker Desktop`
This project is developed using React + Flask

#### Starting backend server

In the project folder

`cd server`

Build the Flask server

`sudo docker build --tag backend:python .`

Starting the flask server

`sudo docker run --rm -p 8080:8080 -e PORT=8080 backend:python`

After your Flask server is running,
`cd ..`

`cd maui-wildfire`

`npm install`

`npm run start`

This will start up a local instace of the project.
