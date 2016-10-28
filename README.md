# birdy

Simple API engine which aims to create some REST API in order to interrogate BIRD's daemon.

Birdy is under development.

## Installation
1.  Check out the code.
2.  Create a virtualenv in order to keep the birdy's env as cleas as possible.
3.  Install the requirements.
4.  Rename the `example.birdy.cfg` to `birdy.cfg` and edit it as you need.

        $ virtualenv env
        $ source env/bin/activate
        $ pip install -r requirements.txt
        $ mv example.birdy.cfg birdy.cfg
        $ python server.py

Please notice that if you need to develop some new feature you can keep true the DEBUG flag (in `birdy.cfg`) to let the program feeds itself with some fake data. I think, if you're sane, you don't have a running bird instance on your laptop.

## Issue
Please let me know if you find bugs in the Github's issue traker.
