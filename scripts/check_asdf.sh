#!/bin/bash

# Check if asdf is installed by searching for its command in the system's PATH
if command -v asdf >/dev/null 2>&1; then
    echo "asdf is installed."
else
    echo "asdf is not installed."
    echo "Please visit https://asdf-vm.com/guide/getting-started.html#_1-install-dependencies for installation instructions."
fi
