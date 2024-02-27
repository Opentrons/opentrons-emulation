# opentrons-emulation development setup

This document describes how to set up a development environment for the opentrons-emulation project.

## Frontend Setup

The opentrons-emulation project uses [asdf](https://asdf-vm.com/) to manage our versions of [node.js](https://nodejs.org/en)
To set up your development environment, follow these steps:

1. [Install asdf]([text](https://asdf-vm.com/guide/getting-started.html))
2. Run `make setup-dev-dependencies` to:
    - Configure and install node.js with asdf
    - Install pnpm globally
    - Download, build, bundle, and place mosquitto broker executable inside tauri project
    - Install all node.js dependencies

## Run Development Server
1. Run `make dev` to:
    - Install all rust dependencies
    - Start the Next.js server
    - Compile the tauri app
    - Start the tauri app in development mode
