[![Build Status](https://travis-ci.com/artorious/speedy_chakula_app.svg?branch=ft-fetch-all-orders-160231913)](https://travis-ci.com/artorious/speedy_chakula_app)  [![Coverage Status](https://coveralls.io/repos/github/artorious/speedy_chakula_app/badge.svg?branch=ft-fetch-all-orders-160231913)](https://coveralls.io/github/artorious/speedy_chakula_app?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# speedy_chakula_app
A fast-Food-Fast is a food delivery service app for a restaurant

## Features
* Retrieve and display all food orders 
* Place a new food order
* Retrieve a single food order
* Update food order status



#### Usage
##### Set Install, setup and configure the development enviroment.

1. Install [python3](https://www.python.org/download/releases/3.6.4/)
2. [Pipenv & Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
3. On a  terminal (Linux), Install and set up git `sudo apt install git` 
4. Clone the repository `git clone https://github.com/artorious/speedy_chakula_app.git`
5. Run `cd speedy_chakula_app/`
6. Run `git checkout ch-cleanup-api-v1-160340543`
7. In a virutal environment, run `pipenv shell` to install requirements

##### Starting the application
To run the application and set the envionment variable, 
run `FLASK_APP=run.py ; flask run`

##### Running tests
Run `coverage run -m pytest -v app/tests/test* ; coverage report app/tests/test_*  app/*.py `

On [Postman](https://www.getpostman.com/collections/dbfd44a4306fe46d66a4) 
