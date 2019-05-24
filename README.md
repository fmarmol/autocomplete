[![CircleCI](https://circleci.com/gh/fmarmol/autocomplete.svg?style=svg)](https://circleci.com/gh/fmarmol/autocomplete)

## Requirements:
 - python >= 3.5
 - pytest
 - pytest-cov
 - pylint

## Installation:

We use [pipenv](https://docs.pipenv.org/en/latest/) to have a reproductible build and install dependencies in a virtualenv. Really important for production use.

```bash
python3 -m pip install --user pipenv
pipenv install
```

## Unitaries test + coverage:

```bash
pipenv run pytest --cov=. --cov-report=html --cov-report=term .
```

## Quality of code

```bash
pipenv run pylint autocomplete.py
```


## Usage

```bash
usage: autocomplete.py [-h] file prefix

positional arguments:
  file        text file of vocabulary with one word by line
  prefix      prefix wanted for autocompletion

optional arguments:
  -h, --help  show this help message and exit
```

**example** : `pipenv run python3 autocomplete.py ./examples/file.txt p`


## Questions

- **What would you change if the list of keywords was much larger (several millions) ?**
We can cut branches of the Trie and place them on other hosts. It needs some kind of database or datastructure to store these branches and served them by an RPC api for example.
The walk through the Trie would have some kind of sharding mechanism. The configuration of the shards can be store in a distributed key value database like Consul.

- **What would you change if the requirements were to match any portion of the
keywords (for example, given the string “pro”, the program could suggest the
keyword “reprobe”) ?**:
Given a pattern and assuming that the pattern have to be a prefix of one or more suffixes of a word, we can construct all suffixes for each node and walkthrough them to find a match.
