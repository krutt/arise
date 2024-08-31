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

```sh
$ pip install arise
❯ ...
❯ Installing collected packages: arise
❯ Successfully installed arise-0.1.6
```

</details>

And build required images with `build` command. The following shows you how to build a `Testnet4`
Bitcoin-Core node as well as [electrs](https://github.com/aekasitt/electrs),
[mempool](https://github.com/mempool/mempool) and [mutiny-web](https://github.com/MutinyWallet/mutiny-web)

```sh
arise build --testnet4 --electrs --mempool --mutiny-web
```

<details>
<summary>Sample output when running build command</summary>

```sh
$ arise build --testnet4 --electrs --mempool --mutiny-web
❯
❯ ---> c7c857e7f240
❯  Step 13/13 : ENTRYPOINT ["/usr/app/electrs"]
❯
❯ ---> [Warning] The requested image's platform (linux/amd64) does not match the detected host
❯ ---> Running in 6b6bb5257753
❯ Removing intermediate container 6b6bb5257753
❯ ---> 7c067a938f79
❯ Successfully built 7c067a938f79
❯ Successfully tagged arise-electrs:latest
❯
❯ Build specified images:                    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❯ Built <Image 'arise-testnet4'> successfully
❯ Built <Image 'arise-electrs'> successfully
❯ Built <Image 'arise-mempool'> successfully
❯ Built <Image 'arise-mutiny-web'> successfully
```

</details>

The initial build may take some time as it is downloading source codes from different repositories
and interfacing with `Docker Daemon` to build according to flagged requirements. Once the build process
completes, you can begin deploying local network with peripherals as such:

```sh
arise deploy --testnet4 --with-electrs --with-mempool --with-mutiny-web
```

<details>
<summary>Sample output when running deploy command</summary>

```sh
$ arise deploy --signet --with-electrs --with-mempool --with-mutiny-web
❯ Deploy arise-signet                        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
❯ Deploy middleware services                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
❯ Deploy peripheral services                 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:16
```

</details>

You will have docker containers running in the backend, ready to be interfaced by your local
environment applications you are developing.

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

