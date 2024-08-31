# Arise

[![Bitcoin-only](https://img.shields.io/badge/bitcoin-only-FF9900?logo=bitcoin)](https://twentyone.world)
[![Docker](https://img.shields.io/badge/docker-2496ED?&logo=docker&logoColor=white)](https://hub.docker.com)
[![Top](https://img.shields.io/github/languages/top/krutt/arise)](https://github.com/krutt/arise)
[![Languages](https://img.shields.io/github/languages/count/krutt/arise)](https://github.com/krutt/arise)
[![Size](https://img.shields.io/github/repo-size/krutt/arise)](https://github.com/krutt/arise)
[![Last commit](https://img.shields.io/github/last-commit/krutt/arise/master)](https://github.com/krutt/arise)

[![Arise Banner](static/arise-banner.svg)](https://github.com/krutt/arise/blob/master/static/arise-banner.svg)

## Prerequisites

* python (3.8+)
* pip
* docker

## Contributions

To be determined

### Known issues

You may run into this setback when first running this project. This is a
[docker-py](https://github.com/docker/docker-py/issues/3059) issue widely known as of October 2022.

```python
docker.errors.DockerException:
  Error while fetching server API version: (
    'Connection aborted.', FileNotFoundError(
      2, 'No such file or directory'
    )
  )
```

See the following issue for Mac OSX troubleshooting.
[docker from_env and pull is broken on mac](https://github.com/docker/docker-py/issues/3059#issuecomment-1294369344)
Recommended fix is to run the following command:

```sh
sudo ln -s "$HOME/.docker/run/docker.sock" /var/run/docker.sock
```

## License

This project is licensed under the terms of the MIT license.


