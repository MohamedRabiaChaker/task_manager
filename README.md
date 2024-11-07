# 🧪 Flask Task Manager

Welcome to this dummy project called Flask Task Manager This repository is part of a series of mini-projects I’ve built to showcase my skills as a software and data engineer. I enjoy building and experimenting with new tools and ideas, and this project is designed to highlight some of my abilities in Flask development.

## 🚀 Project Overview

This Flask app is a lightweight web application, designed with simplicity and scalability in mind. It’s perfect for anyone looking to understand the core concepts of a Flask application, from routing to handling forms, or maybe just for a quick dose of fun coding. 😊

Feel free to explore the code, spin it up locally, and see what makes it tick. 
## 📚 Documentation

Below are templates to guide you through documenting each section of this project. Feel free to expand and tailor these as needed to capture the project's unique elements.

### Blueprints

Modules the project is composed of, they offer better adherence so single principle since it allows us to define assets and routes for each piece of fuctionality on it's own.

- **main**: main module, still empty to date


### Features

List out and briefly describe each feature. For example:
- **User Registration**: Allows users to register using a simple form.
- **Database Integration**: Stores user data in a local SQLite database.

### API Endpoints

| Endpoint         | Method | Description             |
| ---------------- | ------ | ----------------------- |
| `/main/test`      | GET     | Testing initial project structure    |

### Development setup

during early development we are using a postgres docker container and running it with the following credentials: 

` docker run --name postgres-container -e POSTGRES_USER=myuser -e POSTGRES_PASSWORBD=mypassword -e POSTGRES_DB=mydb -p 5432:5432 -d postgres ` 
