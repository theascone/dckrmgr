# dckrmgr
### Prerequisites
The easiest way ist through [pip3](https://pypi.python.org/pypi/pip) (Ubuntu: `apt-get install python3-pip`):
* [docker-py](https://github.com/docker/docker-py): `pip3 install docker-py`
* [jsonschema](https://pypi.python.org/pypi/jsonschema): `pip3 install jsonschema`

### Installation
```
git clone git@github.com:theascone/dckrmgr.git
mkdir -p /usr/local/src/dckr
mv dckrmgr/* /usr/local/src/dckr
ln -s /usr/local/src/dckr/dckrmgr /usr/local/bin/dckrmgr
```

### Usage

#### Dckrcnf.json
**Example:**
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
**Equivalents to Docker CLI:**
<table>
    <tr>
        <td><b>Dckrcnf</b></td>
        <td><b>Docker CLI</b></td>
        <td><b>Comment</b></td>
    </tr>
    <tr>
        <td>name</td>
        <td>--name</td>
    </tr>
    <tr>
      <td>
      image(name, version)
      </td>
      <td>name:version</td>
    </tr>
    <tr>
      <td>hostname</td>
      <td>--hostname (-h)</td>
    </tr>
    <tr>
      <td>environment[(name, value)]</td>
      <td>--env (-e)</td>
      <td>Json Array</td>
    </tr>
    <tr>
      <td>volumes[(host_path, container_path, mode)]</td>
      <td>--volume (-v) host_path:container_path:mode</td>
      <td>host_path can be relative to location of dckrcnf.json</td>
      <td>Json Array</td>
    </tr>
    <tr>
      <td>ports[(container_port, host_port)]</td>
      <td>--publish (-p) host_port:container_port</td>
      <td>Json Array</td>
    </tr>
    <tr>
      <td>links[(name, alias)]</td>
      <td>--link name:alias</td>
      <td>Json Array</td>
    </tr>

</table>


### dckrmgr
```
dckrmgr [-h] [-D P_CWD_TOP] [-R] [-t] [-r] [-c] [-s]

optional arguments:
  -h, --help    show this help message and exit
  -D P_CWD_TOP  Set working directory
  -R            Use dckrsub.json files to recursively apply operations
  -t            Stop container
  -r            Remove container
  -c            Create container
  -s            Start container

```
