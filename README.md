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

## Usage

## Dckrcnf.json
Example:
```
{
    "name": "phabricator",

    "image": {
        "name": "theascone/docker_phabricator",
        "version": "latest"
    },

    "hostname": "phabricator.weiltoast.de",

    "environment": [
        {
            "name": "MYSQL_USER",
              "value": "phabricator"
        },
        {
            "name": "MYSQL_PASS",
            "value": "xyz"
        }
    ],
    "volumes": [
        {
            "host_path": "var_log",
            "container_path": "/var/log",
            "mode": "rw"
        },
        {
            "host_path": "/var/run/docker.sock",
            "container_path": "/tmp/docker.sock",
            "mode": "ro"
        }
    ],
    "ports": [
        {
            "container_port": 22,
            "host_port": 22
        },
        {
            "container_port": 22280,
            "host_port": 22280
        }
    ],
    "links": [
        {
            "name": "mysql_phabricator",
            "alias": "mysql"
        }
    ]
}

```


