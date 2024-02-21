# opentrons-emulation development setup

This document describes how to set up a development environment for the opentrons-emulation project.

## Frontend Setup

The opentrons-emulation project uses [asdf](https://asdf-vm.com/) to manage our versions of [node.js](https://nodejs.org/en) and [Rust](https://www.rust-lang.org/). 

To set up your development environment, follow these steps:

1. [Install asdf]([text](https://asdf-vm.com/guide/getting-started.html))
2. Run `make setup-asdf` to install node.js and Rust
3. Close your terminal and open a new one 
4. Run `make setup-fronted` to setup the frontend project

## Run Development Server

1. Run `make dev-frontend`
