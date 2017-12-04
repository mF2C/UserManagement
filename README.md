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

-----------------------

### Usage Guide

...



-----------------------

### Relation to other mF2C components

...
