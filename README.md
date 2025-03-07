# Arise

[![Bitcoin-only](https://img.shields.io/badge/bitcoin-only-FF9900.svg?logo=bitcoin)](https://twentyone.world)
[![Docker](https://img.shields.io/badge/docker-2496ED?&logo=docker&logoColor=white)](https://hub.docker.com)
[![Documentation](https://img.shields.io/badge/pdoc-555?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwBAMAAAClLOS0AAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAkUExURUdwTJHtkZDtkI/vj2rOYFXBQn3deZDukDuzAHDTaFrES4HhfmcEZqoAAAAHdFJOUwCAv0Df788Wv3t3AAACCElEQVQ4y42UsXKcMBCGuVC4Pc6FJuPGRzLDnK/xnAsKP0IeIU+QLhyFEHoAVlJlNxJHlwbBVY4LyeeXs4BLCnQzCTOAZj+0K+3/iyD4zwvhIIiiey/+iVRB8LnJPJBq6QA8eeBRuI8R8UFKTYbc7QGqQRIAOa++KKAD6LW4nQMFwgIB7gMlLaPQz8GVMlhxjD2AoKVcSeKl2jCAyq2K/5yBsiINRqSx+QwUcmhgFNmXOWivzO2CZsWTlyrl2U69qPmMjUi0pBqreY0bvi8BGGHzVaVKJnWHi2o5bwlhOI4JGF9yzeuTPua+5qoHEHvfDAvF398qPz70vboRl4DV8vESCC3HqSfsAAotkNf0sY1HhnR+AZTQruzrBXAHLLe/h9HDtIRwFa+v3XvL4bX8NXpvrLTDb31tImdezvO7dgipAYTOmhyYXAYptOvNuPVR99Ry24BieJlqEX8bdzhUWlBo3JQTMExZ//X7BNplmCgN4t3FFdecnUHJcHLi6ogfEurCujdlMwK38AMItd/FETp0TD2vi6nvW3AHYkje1VmcKJ6humyn46hB1ebkqPwhsYkJs8+jmLYp2Z5AgwkfnlRLPR7BsBTYUH3M7pEVRAMcT2dXbbWLM6d/SEFi6pKayVU75z2Oh3FKoKt7Lv/IkRw6M4mJXKrerP8aII6vz8MVxvsv//gNfQBIOvQNeKr0GQAAAABJRU5ErkJggg==)](https://krutt.github.io/arise)
[![Languages](https://img.shields.io/github/languages/count/krutt/arise)](https://github.com/krutt/arise)
[![Last commit](https://img.shields.io/github/last-commit/krutt/arise/master)](https://github.com/krutt/arise)
[![Size](https://img.shields.io/github/repo-size/krutt/arise)](https://github.com/krutt/arise)
[![Top](https://img.shields.io/github/languages/top/krutt/arise)](https://github.com/krutt/arise)

[![Arise Banner](static/arise-banner.svg)](https://github.com/krutt/arise/blob/master/static/arise-banner.svg)

## Getting started

You can use `arise` simply by installing via `pip` on your Terminal.

```sh
pip install arise
```
<details>
  <summary> Sample output when running install command </summary>

![Sample Pip Install](https://github.com/krutt/arise/blob/master/static/pip-install.gif)

</details>

And build required images with `build` command. The following shows you how to build a `Testnet`
Bitcoin-Core node as well as [electrs](https://github.com/aekasitt/electrs),
[mempool](https://github.com/mempool/mempool) and [mutiny-web](https://github.com/MutinyWallet/mutiny-web)

```sh
arise build --testnet --electrs --mempool --mutiny-web
```

<details>
  <summary> Sample output when running build command </summary>

![Sample Arise Build](https://github.com/krutt/arise/blob/master/static/arise-build.gif)

</details>

The initial build may take some time as it is downloading source codes from different repositories
and interfacing with `Docker Daemon` to build according to flagged requirements. Once the build process
completes, you can begin deploying local network with peripherals as such:

```sh
arise deploy --testnet --with-electrs --with-mempool --with-mutiny-web
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
  <summary> Sample output when running dashboard command </summary>

![Sample Arise Dashboard](https://github.com/krutt/arise/blob/master/static/arise-dashboard.gif)
</details>

## Contributions

### Prerequisites

* [python](https://www.python.org) version 3.9 and above
* [uv](https://docs.astral.sh/uv)
* [docker](https://www.docker.com)

### Set up local environment

The following guide walks through setting up your local working environment using `pyenv`
as Python version manager and `uv` as Python package manager. If you do not have `pyenv`
installed, run the following command.

<details>
  <summary> Install using Homebrew (Darwin) </summary>
  
  ```sh
  brew install pyenv --head
  ```
</details>

<details>
  <summary> Install using standalone installer (Darwin and Linux) </summary>
  
  ```sh
  curl https://pyenv.run | bash
  ```
</details>

If you do not have `uv` installed, run the following command.

<details>
  <summary> Install using Homebrew (Darwin) </summary>

  ```sh
  brew install uv
  ```
</details>

<details>
  <summary> Install using standalone installer (Darwin and Linux) </summary>

  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
</details>


Once you have `pyenv` Python version manager installed, you can
install any version of Python above version 3.9 for this project.
The following commands help you set up and activate a Python virtual
environment where `uv` can download project dependencies from the `PyPI`
open-sourced registry defined under `pyproject.toml` file.

<details>
  <summary> Set up environment and synchronize project dependencies </summary>

  ```sh
  pyenv shell 3.11.9
  uv venv  --python-preference system
  source .venv/bin/activate
  uv sync --dev
  ```
</details>

Now you have the entire project set-up and ready to be tinkered with. Try out the
standard `arise` command which brings up a help menu.

<details>
  <summary> Launch Arise Help </summary>

  ```sh
  $ arise
  >  Usage: arise [OPTIONS] COMMAND [ARGS]...
  > 
  >   arise
  > 
  > Options:
  >   --help  Show this message and exit.
  > 
  > Commands:
  >   auth       Persist authentications in desired run-control file.
  >   build      Build peripheral images for the desired cluster.
  >   clean      Remove all active "arise-*" containers, drop network.
  >   dashboard  Dashboard for checking current state of images deployed.
  >   deploy     Deploy cluster.
  >   pull       Pull core and peripheral images from GitHub container registry
  ```
</details>

## Change-logs

* **0.1.0** Cloned useful and useless things from [aesir](https://github.com/krutt/aesir)
* **0.1.1** Remove visual janks from progress bars
* **0.1.2** Establish new yaml formats and typings
* **0.1.3** Attempt to make `-testnet4` flag work on bitcoin daemon
* **0.1.4** Experiment with c compilers for faster build-times
* **0.1.5** Add peripheral images `arise-elctrs`, `arise-mempoopl` and `arise-mutiny-wallet`
* **0.1.6** Pretend launching electrs on `testnet4` is easy by using custom `electrs` repository
* **0.1.7** Separate middleware deployment and add delay for `mariadb` setup time
* **0.1.8** Experiment with cookie authentications between peripheral images
* **0.1.9** Enable intranet between containers and authenticate using cookie
* **0.2.0** Attribute animation tutoral and typeface in README markdown
* **0.2.1** Drop `testnet4` hacky implementation and custom `electrs` repository; Not worth it.
* **0.2.2** Attribute public domain art, persist authentications, drop `poetry` and use `uv`
* **0.2.3** Use GitHub workflows to setup GitHub Pages application for documentation

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
