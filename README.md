# Raspberry Pi Controller (UMATT)

| [__version: 24.0.1__](https://github.com/umatt-ece/rpi-controller/blob/main/CHANGELOG.md) | [GitHub](https://github.com/umatt-ece/rpi-controller) |

> This repository contains backend code for operating the tractor, designed to run on a Raspberry Pi microcontroller (or some equivalent Linux-based microcontroller). It features a web-based, Vue app interface (see the [display-frontend](https://github.com/umatt-ece/display-frontend) repository for more info).

### Table of Contents
[Overview]()  
[Development]()  


## Overview

The controller code follows the structure shown below:

![Project Structure]()

- frontend web application GUI (display)
- backend api server (server)
- redis parameter store (database)
- logic and sensor/output control (controller)

For additional information, see [project structure](./documents/ProjectStructure.md) documentation.

## Development

Please use **development** branch (or feel free to make your own off of it). Any changes to **main** should be done via *pull request*.

See development [documentation](./documents/README.md) for more details.

## Contributors

> __Svan B.__  
> _Team Lead 2023_
> 

> __Kameron R.__  
> _Software Lead 2023_  
> ronaldk1@myumanitoba.ca
