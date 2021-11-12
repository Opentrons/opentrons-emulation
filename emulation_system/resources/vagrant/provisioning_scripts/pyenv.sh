#!/usr/bin/env bash

sudo -u vagrant sed -Ei -e '/^([^#]|$)/ {a \
export PYENV_ROOT="$HOME/.pyenv"
a \
export PATH="$PYENV_ROOT/bin:$PATH"
a \
' -e ':a' -e '$!{n;ba};}' /home/vagrant/.profile
echo 'eval "$(pyenv init --path)"' >> /home/vagrant/.profile

echo 'eval "$(pyenv init -)"' >> /home/vagrant/.bashrc
curl https://pyenv.run | sudo -u vagrant bash
exec bash

# Install Python 3.7
pyenv -v install 3.7.12