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

[Resources managed by this component](#resources-managed-by-this-component)

[LICENSE](#license)

-----------------------

### Description

The User Management module is responsible for managing the user’s profile and the definition of the user’s device resources that will be shared in mF2C.
It is also responsible for checking that the mF2C applications act according to these sharing model and profile properties.

-----------------------

### Component architecture

This module is part of the Agent Controller component:

![Agent Controller](docresources/ac.png)

This module is composed of three components:
- Profiling
- Sharing Model
- User Management Assessment

-----------------------

### Installation Guide

This component is part of the mF2C Agent Controller and it requires all the other components to work properly.

#### 1. Requirements

1. [Docker](https://docs.docker.com/install/)

**Dockerfile** content:

```
FROM python:3.4-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 46000
CMD ["python", "app.py"]
```

To install as part of mF2C see **mF2C/mF2C** [repository](https://github.com/mF2C/mF2C)

To run the component without Docker, you will need the following:

1. Python 3.4

#### 2. Install

1. Clone / download repository

```bash
git clone https://github.com/mF2C/UserManagement.git
```

2. Go to UserManagement folder

```bash
cd UserManagement
```

3. Build application:

```bash
sudo docker build -t um-app .
```

4. Run application and expose port `46300`:

```bash
sudo docker run -p 46300:46300 um-app
```

<p style="color:red; font-weight: bold">NOTE: Read next section to see how to properly start the component.</p>

-----------------------

### Usage Guide

1. See the user guide that can be found in https://github.com/mF2C/Documentation/blob/master/documentation/user_guide/api.rst (TO BE DONE !!)

2. Environment variables that can be defined (in the [docker-compose](https://github.com/mF2C/mF2C) file) when launching the service:

  - Available environment variables:
    - CIMI_USER
    - CIMI_PASSWORD
    - CIMI_COOKIES_PATH

Example:

```bash
sudo docker run --env CIMI_URL=https://192.192.192.192 --env CIMI_USER="testuser" --env CIMI_PASSWORD="testuserpassword" -p 46300:46300 um-app
```

3. Methods exposed by the REST API 

- List of methods:
  - **/api/v2**
    - GET:    get rest api service status
  - **/api/v2/um/**
    - GET:    check initialization values
  - **/api/v2/um/user-profile/**
    - GET:    get "current" profile
    - POST:   create a new profile
  - **/api/v2/um/user-profile/<string:user_profile_id>**
    - GET:    get profile by profile ID
    - PUT:    updates profile
    - DELETE: deletes profile
  - **/api/v2/um/user-profile/user/<string:user_id>/device/<string:device_id>**
    - GET:    get user's profile by user ID and device ID
    - PUT:    updates profile
    - DELETE: deletes profile
  - **/api/v2/um/sharing-model**
    - GET:    get current sharing model
    - POST:   create new sharing model
  - **/api/v2/um/sharing-model/<string:sharing_model_id>**
    - GET:    get a sharing model
    - PUT:    updates a sharing model
    - DELETE: deletes a sharing model
  - **/api/v2/um/sharing-model/user/<string:user_id>/profile/<string:device_id>**
    - GET:    get user's sharing model
    - PUT:    updates sharing model
    - DELETE: deletes sharing model
  - **/api/v2/um/assesment**
    - GET:    gets the status of the current assessment in the device
    - PUT:    start / stop assessment


4. After installing the User Management module, the REST API services can be accessed at port 46300:

     - List of services (json): _https://192.192.192.192:46300/api/v2/um_

     - List of services (swagger ui): _https://192.192.192.192:46300/api/v2/um.html_

-----------------------

### Relation to other mF2C components

The User Management module is connected with the following mF2C components:

- Is called by the following modules / components:
    - Lifecycle Management: it needs information about the profiling and sharing model before 'launching' a service

- Makes calls to the following modules / components:
    - Lifecycle Management: it sends the Lifecycle warnings when mF2C uses more resources than defined by the user

-----------------------

### Resources managed by this component



**user_profile**

```json
{
  "user_id": "user/1230958abdef",
  "device_id": string,
  "service_consumer": boolean,
  "resource_contributor": boolean,
  "max_apps": integer
}
```

**sharing_model**

```json
{
  "user_id": {:href "user/1230958abdef"},
  "device_id": string,
  "GPS_allowed": boolean,
  "max_CPU_usage": integer,
  "max_memory_usage": integer,
  "max_storage_usage": integer,
  "max_bandwidth_usage": integer,
  "battery_limit": integer
}
```



-----------------------

### LICENSE

The User Management application is licensed under [Apache License, version 2](LICENSE.TXT).
