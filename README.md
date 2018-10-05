[![Build Status](https://travis-ci.com/artorious/speedy_chakula_app.svg?branch=ch-improve-config-settings-160485668)](https://travis-ci.com/artorious/speedy_chakula_app) 
[![Coverage Status](https://coveralls.io/repos/github/artorious/speedy_chakula_app/badge.svg?branch=develop)](https://coveralls.io/github/artorious/speedy_chakula_app?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/a198b1caf23489ac1f6d/maintainability)](https://codeclimate.com/github/artorious/speedy_chakula_app/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# speedy_chakula_app
A fast-Food-Fast is a food delivery service app for a restaurant

## Features
* Retrieve and display all food orders 
* Place a new food order
* Retrieve a single food order
* Update food order status

### Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

##### Set Install, setup and configure the development enviroment.

1. Install and configure [python3](https://www.python.org/download/releases/3.6.4/)
2. Install and configure [Pipenv & VirtualEnvironmentWrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
3. On a  terminal (Linux), Install and set up git `sudo apt install git` 
4. Clone the repository `git clone https://github.com/artorious/speedy_chakula_app.git`
5. Run `cd speedy_chakula_app/`
6. Run `git checkout develop`
7. In a virutal environment, run `pipenv install --dev ; pipenv shell` to install requirements
##### Starting the application
To run the application and set the envionment variable, 

* run`flask run`

###### API Documentation and Endpoints

* [Version 1 API Documentation on postman](https://documenter.getpostman.com/view/3796196/RWaPskzj)
* [Version 2 API Documentation on postman](https://documenter.getpostman.com/view/3796196/RWgnWKjr)

Method | Endpoint | Functionality
--- | --- | ---
GET | /api/v1/orders | Fetches all existing food orders
GET | api/v1/orders/<orderid> | Fetches a specific food order
POST | api/v1/orders | Creates a new food order
PUT  | api/v1/orders/<orderid> | Updates the status of a food order
--- | ---| ---
POST | /api/v2/auth/signup | New User Registration
POST | api/v2/auth/login | User login
GET | api/v2/menu | Display menu of available food items
POST  | api/v2/users/orders | Place a food order

  
###### Running tests

On a terminal Run `coverage run -m pytest -v app/tests/v1/test* ; coverage report app/tests/v1/test_*  app/api/v1/*.py `

[![Run version 1 in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/dbfd44a4306fe46d66a4)
[![Run version 2 in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/f3b5dc9264f6b857b13c)
###### Deployment
Visit the deployed app on [Heroku](https://speedy-chakula-api-heroku.herokuapp.com/api/v1)
