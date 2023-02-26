# Project Structure

The rPi-controller system is broken up into 4 major components:

- Frontend Web Application (GUI) `./display`
- Backend API Server `./server`
- Redis Parameter Store `./database`
- Logic and I/O Controller `./controller`

The diagram below briefly outlines the systems and how they connect to one another. More detailed information about each
system can be found in the corresponding sections that follow.

```
┌────────────────────────────────────────────────────────┐
│ Physical Display                                       │
└────────────────────────────────────────────────────────┘
  ↓ Browser (Chromium)
╔════════════════════════════════════════════════════════╗
║ Frontend Web Application (GUI)                         ║
║  - uses JavaScript VueJS framework                     ║
║ ┌───────────────────────────────────────────────────┐  ║
║ │ Vuex Store                                        │  ║
║ └───────────────────────────────────────────────────┘  ║
║ ┌───────────────────────────────────────────────────┐  ║
║ │ Axios + Endpoints                                 │  ║
║ └───────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════╝
  ↕ Websocket (HTTP)
╔════════════════════════════════════════════════════════╗
║ Backend API Server                                     ║
║  - uses python FASTAPI library                         ║
║ ┌───────────────────────────────────────────────────┐  ║
║ │ Client Manager Thread                             │  ║
║ └───────────────────────────────────────────────────┘  ║
║ ┌───────────────────────────────────────────────────┐  ║
║ │ Routes & Endpoint fucntions                       │  ║
║ └───────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════╝
  ↕ DataStore
╔════════════════════════════════════════════════════════╗
║ Redis Parameter Store                                  ║
║  - uses pre-built Docker image for Redis               ║
║ ┌───────────────────────────────────────────────────┐  ║
║ │ Python Interface class (DataStore)                │  ║
║ └───────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════╝
  ↕ DataStore
╔════════════════════════════════════════════════════════╗
║ Logic and I/O Controller                               ║
║  - uses python Threads to control I/O                  ║
║ ┌───────────────────────────────────────────────────┐  ║
║ │ State Machine                                     │  ║
║ └───────────────────────────────────────────────────┘  ║
║ ┌───────────────────────────────────────────────────┐  ║
║ │ Sensor Reading                                    │  ║
║ └───────────────────────────────────────────────────┘  ║
║ ┌───────────────────────────────────────────────────┐  ║
║ │ Setting Outputs                                   │  ║
║ └───────────────────────────────────────────────────┘  ║
╚════════════════════════════════════════════════════════╝
```


## Frontend Web Application

### VueJS

The frontend web application is our web-based GUI allowing the user to view information about the tractor and interact
with its operation. This web-app is built using the VueJS framework. The GUI part of the web app consists of a number
of HTML views (pages) and components. Each VueJS view/component (extension .vue) has associated CSS (for styling) and
JavaScript code that adds variables and functionality to the page. Each view/components thus has 3 sections and will
generally have the following structure:

```vue
<template>
  <div>
    <!-- This is where the html elements go... -->
  </div>
</template>

<script>
import "imports from other .js files go here"

export default {
  name: "name of view/component",
  components: {
    // imported component declarations
  },
  props: {
    // variables passed in from a parent view/component
  },
  data() {
    return {
      // view/component specific variables
    }
  },
  mounted: {
    // code to run when the view/component is mounted. Other lifecycle hooks include:
    //  - beforeCreated
    //  - created
    //  - beforeMounted
    //  - mounted
    //  - beforeUpdate
    //  - updated
  },
  methods: {
    // list of JavaScript methods which can be called by event handlers
  },
  computed: {
    // computed properties are variables defined as a function, allowing for complex logic or reactive data
  }
}
</script>

<style>
.property {
  /* CSS styling for elements, tags, ids, etc... */
}
</style>
```

As you can see the bulk of the magic is the underlying JavaScript that makes the web pages "do stuff".

In order to actually 'create' the VueJS app, the [main.js](../display/src/main.js) file creates an instance of a VueJS
application and mounts the applications at the file [App.vue](../display/src/App.vue) (our entry point).

The [Router](../display/src/router/index.js) sets up a list of various views/components that can be accessed by various
paths (ie. http://site/your-path-here). Then, by inserting the <router-view> html element into our app (provided by the
VueJS framework), we are able to have views/components that change depending on our current path (ie. think different
pages on a website).

The [Vuex Store](../display/src/store/index.js) provides central access to locally stored variables. It consists of
individual _modules_ that each have _state_ (variables), _getters_, _mutations_, and _actions_ (functions). This store
can be imported into our views/components and thus allow multiple views/components access to the same variables. For
our project, the Vuex store is more or less a copy of the Redis database that gets stored locally (in the browser) to
quick and easy access. These values are constantly updated by backend (via websocket) and occasionally by the user.

We also have various other [Services](../display/src/services) that let us write functions once and then import them
into multiple views/components.

For more information on VueJs, see its [documentation](https://vuejs.org/guide/introduction.html).

### Node.js and NPM

Node.js is the underlying JavaScript runtime environment that we use to actually run VueJS. The **N**ode **P**ackage
**M**anager (or just NPM) allows us to manage JavaScript packages/libraries (and versions) that we use in our project.
The configuration of NPM for the project is stored in the [package.json](../display/package.json) file.


## Backend Web Server

The backend web server facilitates communication between the frontend web-application and the controller logic and I/O.

Using the python library FASTAPI, it hosts a API server on port 8577. This server contains a number of endpoints that
called be called by the frontend (via a http websocket) and services these requests asynchronously. The various
functions of these endpoints vary, more detailed information can be found [here](../server/ServerInfo.md).

Additionally, the backend server has a separate thread that runs the _ClientManager_ python class. This class handles
the various websocket connections made to the server (at the moment just one) and keeps track of the 'meta-data'
information about the server. Also, this manager continuously updates the frontend with the current information stored
in Redis.

For additional information regarding FASTAPI, check out its [documentation](https://fastapi.tiangolo.com/).

## Redis Database

First, let me just clarify that Redis is not an actual "database" like mySQL or PostgreSQL. Rather, it is a key-value
store. If you're familiar with python, it's like a giant 'dictionary' datastructure. It stores 'parameters' and their
associated 'values', and if desired persists them to disk (ie. stores them so that they can be reloaded next time the
application starts up).

For our project, we have 2 types of parameters: _live_ and _stored_. Live parameters are not persisted to disk, and
thus on start-up take a default value. Stored parameters are persisted to disk, therefore when the system starts up
they will be read from memory and have the same value as when teh system was last shut down.

To deploy our Redis "database", we use a pre-made Docker container that sets everything up for us. In order to actually
read and set values in Redis, we use a python wrapper class [DataStore](../database/data_store.py). Each application
that wants to access Redis creates their own instance of the DataStore class, which then provides them with functions
to _get_ and _set_ values in Redis.

For more information see the Redis [documentation](https://redis.io/docs/).


## Logic Controller & I/O

...


## Additional Information

### Docker

This project is deployed using Docker "containers". Docker acts like a 'Virtual Machine', running a specific piece of
code in an isolated, self-contained environment. That said, unlike a lot of other Virtual Machines, it takes advantage
of the underlying OS to provide a minimal amount of overhead (perfect for a system like the Raspberry Pi).

Each of these self-contained processes are called "containers". Containers are build from an "image" (the code and
configuration files that describe its functionality). The contents of a container (files, code, etc...) are known as
it's "volume(s)". Each container also has a "network", the connections (ports) within the container (between processes).
To learn more about docker, check out its [documentation](https://docs.docker.com/get-started/).

Each of the 4 major components (display, server, database, and controller) are each run in a separate Docker container.
The configuration for these containers can be found in the [docker-compose.yml](../docker-compose.yml) file. These
files aren't written in any particular language, but follow a specific structure (see the
[documentation](https://docs.docker.com/compose/) for further details). Additionally, for the containers we set up
ourselves there are separate files that specify the instructions each container should execute, these can be found at:

- [DockerfileDisplay](../DockerfileDisplay)
- [DockerfileServer](../DockerfileServer)
- [DockerfileController](../DockerfileController)
