[![Build Status](https://travis-ci.com/artorious/speedy_chakula_app.svg?branch=ch-improve-config-settings-160485668)](https://travis-ci.com/artorious/speedy_chakula_app) 
[![Coverage Status](https://coveralls.io/repos/github/artorious/speedy_chakula_app/badge.svg?branch=ch-improve-config-settings-160485668)](https://coveralls.io/github/artorious/speedy_chakula_app?branch=ch-improve-config-settings-160485668) 
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# speedy_chakula_app
A fast-Food-Fast is a food delivery service app for a restaurant

## Features
* Retrieve and display all food orders 
* Place a new food order
* Retrieve a single food order
* Update food order status

[API Documentation](https://documenter.getpostman.com/view/3796196/RWaPskzj)


#### Usage
##### Set Install, setup and configure the development enviroment.

1. Install [python3](https://www.python.org/download/releases/3.6.4/)
2. [Pipenv & Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
3. On a  terminal (Linux), Install and set up git `sudo apt install git` 
4. Clone the repository `git clone https://github.com/artorious/speedy_chakula_app.git`
5. Run `cd speedy_chakula_app/`
6. Run `git checkout ch-API-Documentation-160534024`
7. In a virutal environment, run `pipenv shell` to install requirements

##### Starting the application
To run the application and set the envionment variable, 
run `FLASK_APP=run.py ; flask run`

##### Running tests
Run `coverage run -m pytest -v app/tests/v1/test* ; coverage report app/tests/v1/test_*  app/api/v1/*.py `

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/dbfd44a4306fe46d66a4)