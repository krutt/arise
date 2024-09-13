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

## Getting started

You can use `arise` simply by installing via `pip` on your Terminal.

```sh
pip install arise
```
<details>
<summary>Sample output when running install command</summary>

![Sample Pip Install](https://github.com/krutt/arise/blob/master/static/pip-install.gif)

</details>

And build required images with `build` command. The following shows you how to build a `Testnet4`
Bitcoin-Core node as well as [electrs](https://github.com/aekasitt/electrs),
[mempool](https://github.com/mempool/mempool) and [mutiny-web](https://github.com/MutinyWallet/mutiny-web)

```sh
arise build --testnet4 --electrs --mempool --mutiny-web
```

<details>
<summary>Sample output when running build command</summary>

![Sample Arise Build](https://github.com/krutt/arise/blob/master/static/arise-build.gif)

</details>

The initial build may take some time as it is downloading source codes from different repositories
and interfacing with `Docker Daemon` to build according to flagged requirements. Once the build process
completes, you can begin deploying local network with peripherals as such:

```sh
arise deploy --testnet4 --with-electrs --with-mempool --with-mutiny-web
```

<details>
<summary>Sample output when running deploy command</summary>

![Sample Arise Deploy](https://github.com/krutt/arise/blob/master/static/arise-deploy.gif)

</details>

You will have docker containers running in the backend, ready to be interfaced by your local
environment applications you are developing.

## Dashboard

Arise not only facilitates the deployment of intermingling [Bitcoin](https://twentyone.world) services
but allows you to view Node's Blockchain Information, Mempool Information, Peripheral Details and etc.

In order to view relevant metrics, launch the dashboard using the following command.

```sh
arise dashboard
```

<details>
<summary>Sample output when running dashboard command</summary>

![Sample Arise Dashboard](https://github.com/krutt/arise/blob/master/static/arise-dashboard.gif)

</details>

## Contributions

To be determined

## Attributions

1. [Dutch Golden Age Prints and Paintings](https://picryl.com/media/soldaat-die-zijn-roer-met-beide-handen-rechtop-voor-zich-vasthoudt-nr-20-ca-1c5eb2) - Rijksmuseum, Public Domain Marked.
2. [ปฐวี - Patavi](https://www.f0nt.com/release/sov-patavi) font by [uvSOV - Worawut Thanawatanawanich](fb.com/worawut.thanawatanawanich)
3. [Florent Galon](https://flo.rent) for flame animation used as Tusk's HellFire.
4. [Avinash Vytla](https://github.com/SnippetsDevelop) for breaking down Florent's process on [YouTube](https://youtu.be/RP_x_F7m1UI)

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

