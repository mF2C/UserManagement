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
2. [mF2C](https://github.com/mF2C/mF2C)

Read [Usage Guide](#usage-guide) section to see how to properly start the component.

-----------------------

### Usage Guide

1. See the user guide that can be found in https://github.com/mF2C/Documentation/blob/master/documentation/user_guide/api.rst (TO BE DONE !!)

2. Environment variables that can be defined (in the [docker-compose](https://github.com/mF2C/mF2C) file) when launching the service:

- CIMI_USER
- CIMI_PASSWORD
- CIMI_COOKIES_PATH

Example:

```bash
sudo docker run --env CIMI_URL=https://192.192.192.192 --env CIMI_USER="testuser" --env CIMI_PASSWORD="testuserpassword"  --env CIMI_COOKIES_PATH="~./cookies" -p 46300:46300 um-app
```

3. After installing the User Management module, the REST API services can be accessed at port 46300:

     - List of services (json): _https://192.192.192.192:46300/api/v1/user-management_

     - List of services (swagger ui): _https://192.192.192.192:46300/api/v1/user-management.html_

-----------------------

### Relation to other mF2C components

The User Management module is connected with the following mF2C components:

- Is called by the following modules / components:
    - Lifecycle Management: it needs information about the profiling and sharing model before 'launching' a service

- Makes calls to the following modules / components:
    - Resource Manager:
    - Lifecycle Management: it sends the Lifecycle warnings when mF2C uses more resources than defined by the user

-----------------------

### Resources managed by this component



**user_profile**

```json
{
  "user_id": "user/1230958abdef",
  "device_id": string,
  "id": URI,
  "name": string,
  "description": "profiling ...",
  "id_key": string,
  "email": string,
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
  "id": URI,
  "name": string,
  "description": "sharing model ...",
  "GPS_allowed": boolean,
  "max_CPU_usage": integer,
  "max_memory_usage": integer,
  "max_storage_usage": integer,
  "max_bandwidth_usage": integer,
  "battery_limit": integer
}
```

To get information about battery level status:
https://github.com/mF2C/cimi/blob/atos2/server/src/com/sixsq/slipstream/ssclj/resources/spec/device_dynamic.cljc

```
(s/def :cimi.device-dynamic/device ::cimi-common/resource-link)


(s/def :cimi.device-dynamic/powerRemainingStatus ::cimi-core/nonblank-string)
(s/def :cimi.device-dynamic/powerRemainingStatusSeconds ::cimi-core/nonblank-string)
```

To get number of apps running in a device:
Lifecycle



-----------------------

### LICENSE

The User Management application is licensed under [Apache License, version 2](LICENSE.TXT).
