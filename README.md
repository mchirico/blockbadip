[![Build Status](https://travis-ci.org/mchirico/blockbadip.svg?branch=develop)](https://travis-ci.org/mchirico/blockbadip)

# blockbadip
Python - Block IPs based on /var/log/mail.log messages



## Setup

```bash
mkvirtualenv bip
workon bip

pip install -r requirements.txt

```



<img src="https://github.com/mchirico/mchirico.github.io/raw/a201450f47434ad8fee4f93dc824caa4ef5864d2/p/images/addvm.png" alt="drawing" width="750px;"/>
         </a>



## Testing

```bash

cd blockbadip

export PYTHONPATH="."
pytest -v tests/tests_block_bad_ip.py

```