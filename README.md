# dckrmgr
## Prerequisites
The easiest way ist through [pip3](https://pypi.python.org/pypi/pip) (Ubuntu: `apt-get install python3-pip`):
* [docker-py](https://github.com/docker/docker-py): `pip3 install docker-py`
* [jsonschema](https://pypi.python.org/pypi/jsonschema): `pip3 install jsonschema`

## Installation
```
git clone git@github.com:theascone/dckrmgr.git
mkdir -p /usr/local/src/dckr
mv dckrmgr/* /usr/local/src/dckr
ln -s /usr/local/src/dckr/dckrmgr /usr/local/bin/dckrmgr
```
