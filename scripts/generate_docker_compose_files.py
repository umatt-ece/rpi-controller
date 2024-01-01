"""
This script is designed to generate a number of Docker-Compose files for running on various systems. The general content
is identical, with environment variables and file paths allowing them to run on the intended Operating System.

NOTE: It is important that this script be run from the `root` directory of this project (`.../rpi-controller`) in order
for the file paths to be generated correctly.

ARGUMENTS: Optionally, a command line argument may be provided to specify which platform to generate for. If not
provided, or the provided string does not match any platforms, all platforms will be generated.

Files Generated:
 * `docker/docker-compose-rpi.yml`
 * `docker/docker-compose-linux.yml`
 * `docker/docker-compose-windows.yml`

Author: Kameron Ronald
Date:   2023-12-30
"""
import sys
import os
from datetime import datetime


TAB_SIZE = 8
CWD = os.getcwd()

config = {
    "Raspberry Pi": {
        "filename": "docker-compose-rpi.yml",
    },
    "Linux": {
        "filename": "docker-compose-linux.yml",
    },
    "Windows": {
        "filename": "docker-compose-windows.yml",
    },
}

preferred_platform = sys.argv[1]

for platform, details in config.items():
    if preferred_platform == platform or preferred_platform not in config.keys():

        # Generate multi-line file content string
        file_contents = f'''
        # This file has been automatically generated by `scripts/generate_docker_compose_files.py`. Note that is you modify
        # this file, it will be overwritten when the script is next run. For permanent changes, please modify the script.
        #
        # Platform:  {platform}
        # Generated: {datetime.now().strftime("%Y-%m-%d at %I:%M %p (%Z)")}
        
        version: "3.7"
        services:
        
          database:
            image: redis
            ports:
              - "6379:6379"
            restart: always
        
          controller:
            build:
              dockerfile: Dockerfile
              context: .
            ports:
              - "8577:8577"
            environment:
              REDIS_HOST: "database"
              REDIS_PORT: "6379"
              LOCAL: "{"false" if platform == "Raspberry Pi" else "true"}"
            volumes:
              - "{CWD}/common:/controller/common"            # Module 'common'
              - "{CWD}/database:/controller/database"        # Module 'database'
              - "{CWD}/hardware:/controller/hardware"        # Module 'hardware'
              - "{CWD}/logic:/controller/logic"              # Module 'logic'
              - "{CWD}/server:/controller/server"            # Module 'server'
              - "{CWD}/log:/controller/log"                  # Mapped in log folder
              - "{CWD}/__init__.py:/controller/__init__.py"  # rpi-controller __init__.py
              - "{CWD}/main.py:/controller/main.py"          # rpi-controller main.py
            depends_on:
              - database
            restart: always
        '''

        # Split-up file contents by line (and remove first empty line)
        file_contents = file_contents.splitlines()[1:]

        if platform == "Raspberry Pi":
            file_contents.insert(21, f'{" " * TAB_SIZE}    privileged: true')

        with open(f"{details['filename']}", "w") as file:
            for line in file_contents:
                # Write line contents to file (and remove leading indent)
                file.write(f"{line[TAB_SIZE:]}\n")
            file.close()
