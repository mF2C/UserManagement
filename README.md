# UserManagement
Agent Controller - User Management module

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

&copy; Atos Spain S.A. 2017

The User Management module is a component of the European Project mF2C.

-----------------------

[Description](#description)

[Component architecture](#component-architecture)

[Installation Guide](#installation-guide)

[Usage Guide](#usage-guide)

[Relation to other mF2C components](#relation-to-other-mf2c-components)

-----------------------

### Description

The User Management is responsible for managing the user’s profile and the definition of the user’s device resources that will be shared in mF2C.
It is also responsible for checking that the mF2C applications act according to these sharing model and profile properties.

-----------------------

### Component architecture

...

-----------------------

### Installation Guide

##### 1. Requirements

1. Docker
2. Docker-Compose
3. Python 2.7.9 - 2.7.14

#### Launch with Docker

- Build application:

```bash
sudo docker build -t um-app .
```

- Run application:

```bash
sudo docker run -p 5001:5000 um-app
```

#### Launch with Docker-Compose

...

#### Launch application and dataClay



###### 1. dataClay

1.1. Download [dataClay](https://github.com/mF2C/dataClay)

1.2. Initialize the dataClay services

```bash
cd orchestration
docker-compose rm  # to clean the previous containers, if exist
docker-compose up
```

###### 2. User Mgmt module

2.1. register

```bash
sudo bash register.sh
```

2.2. launch python virtualenv

```bash
virtualenv env
source env/bin/activate
```

(deactivate)

2.3. client.properties

```bash
HOST=192.168.252.42
TCPPORT=11034
```

2.4. launch application

(/usr/bin/python2.7)

```bash
python rest_api.py
```


-----------------------

### Usage Guide

...



-----------------------

### Relation to other mF2C components

...
