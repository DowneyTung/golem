H5-Golem - Test Automation Framework
==================================================
[![Build Status](https://travis-ci.org/lucianopuccio/golem.svg?branch=master)](https://travis-ci.org/lucianopuccio/golem)
[![Documentation Status](https://readthedocs.org/projects/golem-framework/badge/?version=latest)](https://golem-framework.readthedocs.io/en/latest/?badge=latest)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Join the chat at https://gitter.im/golem-framework/golem](https://badges.gitter.im/golem-framework/golem.svg)](https://gitter.im/golem-framework/golem?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Intro
--------------------------------------

>Automate end to end tests in minutes, not hours.


H5-Golem is a complete test automation tool and framework for end-to-end testing, forked from [Github](https://github.com/lucianopuccio/golem), configured by Downey Tung in house for High5games. It creates powerful, robust and maintainable test suites, it's easy to learn even without a lot of programming knowledge. It is based on Selenium Webdriver, openCV, Tesseract and it can be extended using Python.

**It can:**
* Use the Page Object pattern
* Use Image recognition/template matching to automate application without DOM ([OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html#template-matching), [Tesseract](https://github.com/madmaze/pytesseract))
* Run tests in parallel.
* Write tests with multi data sets (data-driven)
* Test APIs
* Run tests remotely ([Zalenium](https://opensource.zalando.com/zalenium/) docker container or a cloud testing provider)
* It can be executed from Jenkins or any other CI tool


**It has:**
* A complete GUI module (a web application) to write and execute tests
* A reporting engine and a web reports module
* An interactive console


Pre-requisites
--------------------------------------

Basic knowledge of Selenium Webdriver is required. Check out [this docs](https://golem-framework.readthedocs.io/en/latest/installation.html) first.


Installation Instructions
--------------------------------------

>*Specifically for Running the H5G Test in Unix/Linux*


This framework works with python 3.4+ above.

The easiest way to build the project and run the the test is through [Docker](https://store.docker.com/search?offering=community&type=edition)

git clone the project and check out `H5G` branch

```
git clone git@github.com:DowneyTung/golem.git
cd golem
```

Since I forked the project, you ought to check out my branch for h5g project

```
git checkout H5G
```

if you decide to build the project and run the test using Docker

  - First, build the golem base-image

```
docker build -t downey/golem:1.0 .
```
   pull the selenium images from dockerHub
```
docker pull elgalu/selenium
```

  - Second, start the services by running
```
docker-compose up
```

  - Third, open your browser, preferably Chrome and navigate to
```
http://localhost:5000/
```

  - Fourth, login with username as *admin* and password as *admin*

  - Fifth, navigate to Suites, click on the rmg_smoke_test, click on Run Suite

  - Sixth, Open a new tab on the browser and navigate to the url below to watch the test running live
```
http://localhost:4444/grid/admin/live
```
  - Seventh, after the test finish running, navigate to the url below to view the test report
```
http://localhost:5000/report/project/RMG/
```
*Run Test Suite in Docker*

![grab_test_running_gif](https://github.com/DowneyTung/golem/blob/H5G/images/Golem_test_parallel.gif)

**If you want to build the project local without using docker**

I recommend to use pipenv to intialize a virtual python3 env

On MacOS, you can install Pipenv easily with [Homebrew](https://brew.sh/):

```
brew install pipenv
```

To initialize and spawn a python 3 virtual environment

```
pipenv shell --three
```

git clone the project and check out `H5G` branch

```
git clone git@github.com:DowneyTung/golem.git
cd golem
git checkout H5G
```

install the dependencies and setup

```
pip install requirements -r
```
```
python setup.py install
```


cd into the H5G directory and run the full smoke suite in parallel from command line
```
cd H5G
golem run RMG rmg_smoke_test
```

*Run Individual Test From Console*

```
golem run <project> <test>
```

Flags:

* -b | --browsers: a list of browsers, by default use defined in settings.json or Chrome
* -t | --threads: run in parallel, default 1 (not parallel)
* -e | --environments: a list of environments, default is none

Examples for running each individual test separately

```
golem run RMG load_app_change_bet_test -b chrome -e stage
golem run RMG load_app_click_on_spin_test -b chrome -e stage
golem run RMG load_app_dropdown_tab_test -b chrome -e stage
```

Examples for running each individual test separately through `Zalenium` locally

```
golem run RMG load_app_change_bet_test -b chrome-remote -e stage
golem run RMG load_app_click_on_spin_test -b chrome-remote -e stage
golem run RMG load_app_dropdown_tab_test -b chrome-remote -e stage
```

**Start the Web Module**
```
cd H5G (if you are not in the H5G directory)
golem gui
```

The Web Module can be accessed at http://localhost:5000/

By default, the following user is available: username: *admin* / password: *admin*

>*Specifically for Running the H5G Test in windows 10 above *

On windows machine, make sure you have [docker](https://store.docker.com/editions/community/docker-ce-desktop-windows) and [gitbash](https://git-scm.com/download/win) installed and configured properly to run the test.

The easiest way to start experiencing the automation framework is through building the test automation framework using docker.

git clone the porject and checkout development branch
```
git clone git@github.com:DowneyTung/golem.git
cd golem
git checkout H5G
```

Currently I only did test run of the test suites via docker

  - First, build the golem base-image

```
docker build -t downey/golem:1.0 .
```
   pull the selenium images from dockerHub
```
docker pull elgalu/selenium
```

  - Second, start the services by running
    In order to spin up the containers on win 10 above, you need to run the docker-compose-win.yml file

    Before we run the docker-compose-win.yml file:
     - make new directory in your c drive, `/c/Users/$your_user_name/temp/videos`

     - edit the docker-compose-win.yml file and replace `dtung` in line 9 to your $your_user_name

     - add `$Env:COMPOSE_CONVERT_WINDOWS_PATHS=1` to Powershell due to this [issue](https://stackoverflow.com/questions/51466393/cannot-set-traefik-via-labels-inside-docker-compose-yml)

    Run the docker-compose-win.yml file to spawn the docker containers:

```
docker-compose -f docker-compose-win.yml up
```

  - Third, open your browser, preferably Chrome and navigate to
```
http://localhost:5000/
```

  - Fourth, login with username as *admin* and password as *admin*

  - Fifth, navigate to Suites, click on the rmg_smoke_test, click on Run Suite

  - Sixth, Open a new tab on the browser and navigate to the url below to watch the test running live
```
http://localhost:4444/grid/admin/live
```
  - Seventh, after the test finish running, navigate to the url below to view the test report
```
http://localhost:5000/report/project/RMG/
```

Documentation
--------------------------------------

Read the full documentation of this framework here: [https://golem-framework.readthedocs.io/](https://golem-framework.readthedocs.io/)

License
--------------------------------------

[MIT](https://tldrlegal.com/license/mit-license)
