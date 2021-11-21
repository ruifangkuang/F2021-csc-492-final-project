# CSC492 Semester Long Project
Final project repository for CSC 492 group of Nick, Sabah, Brennan and Ruifang.

## Overview
This application is written in Flask, a web development framework written in Python. It uses virtual environments for package management.

A visualization of tasks and application architecture is available via this [Figma whiteboard](https://www.figma.com/file/lHswI2yQxbDxS8nV8eekAt/Engineering-Whiteboard?node-id=36%3A14).

### Setup 
To get access to the code, navigate to the directory on your local machine in which you want the code/repo to be stored, and run: ```$ git clone https://github.com/Brennan-Richards/csc-492-project.git```. You can then create branches, add files, push back to the repository, etc.

## Running
To run the application, first the virtual environment must be active. To activate the virtual environment, navigate to the code repository via a terminal on your local machine and run: ```$ . venv/bin/activate```. The Flask application can then be run on a local server for development by running: ```$ flask run```.

To enable hot reload, updating the webpage when changes are made to your local codebase, run ```$ export FLASK_ENV=development```.

## Requirements
Requirements are the packages needed to run the program.

To install the requirements, navigate to the code repository via a terminal on your local machine and run: ```$ pip install -r requirements.txt```.

If you download a new requirement, you must include it in the requirements.txt file by running ```$ pip freeze > requirements.txt```.

### Development

## Database
The database interface we are using is SQLAlchemy. Read the documentation [here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/).

## User Interface
Many of the CSS classes used are part of [Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/). Bootstrap is a CSS framework that provides a lot of the styling for the website out of the box so that we don't need to define it ourselves.
