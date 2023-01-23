`pydrought3` is a package containing python 3 modules for drought data management

# Quick Start

## Supported Python Versions

Python == 3.6, tested on Python 3.7.2

## Mac/Linux


Setup a virtual environment for the project, if you don't have one
```
python3 -m venv <your-env>
source <your-env>/bin/activate
```

On the activated environment, ensure pip setuptools and wheel are up-to-date
```
python -m ensurepip --default-pip
python -m pip install --upgrade pip setuptools wheel
```

Install on your virtual environment
```
pip install git+https://webgate.ec.europa.eu/CITnet/stash/scm/drought/pydrought_pack.git
```

## Windows

TODO

# Example Usage

```
from pydrought3 import <module_name> as time
```

```
>>> from pydrought3 import time_mgt as time
>>> time.Dekad(2019,12,30)
```
