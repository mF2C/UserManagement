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

The User Management module is responsible for managing the user’s profile and the definition of the user’s device resources that will be shared in mF2C.
It is also responsible for checking that the mF2C applications act according to these sharing model and profile properties.

-----------------------

### Component architecture

This module is part of the Agent Controller component:

![Agent Controller](resources/ac.png)

This module is composed of three components:
- Profiling
- Sharing Model
- User Management Assessment

-----------------------

### Installation Guide

#### 1. Requirements

1. Docker
2. Docker-Compose
3. Python
    - 2.7.9 - 2.7.14 (when working directly with Dataclay - Data Management module)
    - 3.* (when using CIMI)

#### 2. Launch application

###### 2.1. Launch with Docker

- Build application:

```bash
sudo docker build -t um-app .
```

- Run application:

```bash
sudo docker run -p 5001:8083 um-app
```

###### 2.2. Launch with Docker-Compose

_-not ready-_

###### 2.3. Launch application and dataClay

_-not ready-_


#### 3. Working with Dataclay - Data Management module

1. Download [Dataclay](https://github.com/mF2C/dataClay)

2. Initialize the Dataclay services

```bash
cd orchestration
docker-compose rm  # to clean the previous containers, if exist
docker-compose up
```

###### 3.1. User Mgmt module

1. register

```bash
sudo bash register.sh
```

2. launch python virtualenv

```bash
virtualenv env
source env/bin/activate
```

```bash
deactivate
```

3. Edit _client.properties_ file

```bash
HOST=192.168.252.42
TCPPORT=11034
```

4. launch application

(/usr/bin/python2.7)

```bash
python rest_api.py
```


-----------------------

### Usage Guide

REST API can be accessed at port 5001. For example:
_https://localhost:5001/api/v1/user-management_



-----------------------

### Relation to other mF2C components

_--_
