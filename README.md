# snaker

[![Python badge](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub tag](https://img.shields.io/github/tag/erishforG/snaker.svg)](https://github.com/erishforG/snaker/tree/0.0.3)
[![Build Status](https://travis-ci.org/erishforG/snaker.svg?branch=master)](https://travis-ci.org/erishforG/snaker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/erishforG/snaker/blob/master/LICENSE)

![snaker_image](https://github.com/erishforG/snaker/blob/master/server_image.jpeg)

Snaker is a Python based simple url shortener the Django framework.

## Compatibility

* Python 2.7, 3.4, 3.5 and 3.6 (recommended)
* Django 1.8 LTS, 1.9, 1.10, 1.11 LTS, 2.0 (recommended)
* MySQL (recommended), Oracle Database and SQLite and etc.

## Usage

1) download the package or fork the package or git clone https://github.com/erishforG/snaker.git

2) python3 pip install -r requirements.txt

3) vi ~/snaker/snaker/settings.py to change each values (*specific information will be bellow)

4) python3 manage.py migrate

5) python3 manage.py createsuperuser

6) python3 manage.py run server

7) visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Documentation
### how does snaker work

1) When you register 'LONG URL', snaker will match with 'HASH' code created by itself or oneself who uses snaker. 

2) Using base url with hashcode to enter the page, snaker will check the request.

3) snaker will get the information of the user who enter the page and records the data.

4) And then snaker will redirect the page that the user wants.

### parameters
#### base information
BASE_URL = base site url

BASE_TITLE = base site title

BASE_DESCRIPTION = base site description

BASE_IMAGE = base site image

#### redirect information
1) REDIRECT_IMAGE = redirect page base image

2) REDIRECT_THUMBNAIL = redirect page thumbnail logo below REDIRECT_IMAGE

3) REDIRECT_TIME = redirect delay time

#### utm setting
1) UTM - a simple code that you can attach to a custom URL behind the original code in order to track a source, medium, and campaign name

### database
choose your database and set your name, host, id, pw and etc.

## contribute
### contributers

@erishforG 
@musalys
@wangseung
@codingbowoo

### how to contribute

welcome :) pull requests for bug fixes, new features, and improvements to snaker. Contributors to the main snaker repository must accept MIT License Agreement before any changes can be merged.

## License

MIT
