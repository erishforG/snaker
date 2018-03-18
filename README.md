# snaker

[![Build Status](https://travis-ci.org/erishforG/snaker.svg?branch=master)](https://travis-ci.org/erishforG/snaker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/erishforG/snaker/blob/master/LICENSE)

Snaker is a Python based simple url shortner the Django framework.

## Compatibility

* Python 2.7, 3.4, 3.5 and 3.6 (recommended)
* Django 1.8 LTS, 1.9, 1.10, 1.11 LTS, 2.0 (recommended)
* MySQL (recommended), Oracle Database and SQLite and etc.

## Usage

1) download the pacakge or fork the package or git clone https://github.com/erishforG/snaker.git

2) python3 pip install -r requeriments.txt

2) vi ~/snaker/snaker/settings.py to change each values (*specific information will be bellow)

3) python3 manage.py run server

4) visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Documentation

### base information
BASE_URL = base site url

BASE_TITLE = base site title

BASE_DESCRIPTION = base site description

BASE_IMAGE = base site image

###redirect information
1) REDIRECT_IMAGE = redirect page base image

2) REDIRECT_THUMBNAIL = redirect page thumbnail logo below REDIRECT_IMAGE

3) REDIRECT_TIME = redirect delay time

### utm setting
1) UTM - a simple code that you can attach to a custom URL behind the original code in order to track a source, medium, and campaign name

### database
choose your database and set your name, host, id, pw and etc.

## License

MIT
