# RMNIM

Reconstrução de morfologia neuronal a partir de imagens de microscopia - PIB12628-2023 - Processamento de imagens médicas na nuvem

## Descrição

Este projeto tem como objetivo a reconstrução da morfologia neuronal a partir de imagens de microscopia. Utilizamos técnicas de processamento de imagens médicas na nuvem para realizar essa tarefa.

## Requisitos

Recomendamos o uso do [Miniforge3](https://github.com/conda-forge/miniforge) para gerenciar os pacotes e ambientes virtuais. Você pode utilizar o `mamba` ou `conda` para instalar os pacotes necessários.

### Instalação do Miniforge3

Siga as instruções no repositório [Miniforge3](https://github.com/conda-forge/miniforge) para instalar o Miniforge3 em seu sistema.

### Criação do Ambiente Virtual

Você pode criar um novo ambiente virtual ou utilizar o ambiente `base` que já é criado durante a instalação do Miniforge3.

### Instalação dos Pacotes

Para instalar os pacotes básicos necessários para rodar o código, execute o seguinte comando:

```sh
mamba install -c conda-forge opencv scikit-image scipy numpy pandas jupyterlab
```
ou
```sh
conda install -c conda-forge opencv scikit-image scipy numpy pandas jupyterlab
```
## Execução
### Comandos do Makefile

O `Makefile` contém alguns comandos úteis para executar e limpar o projeto:

- `runmetric`: Executa a métrica `DiademMetric`.
- `clean`: Remove arquivos de cache e checkpoints.
- `runpypy`: Executa o script Python usando `PyPy`.
- `runpy`: Executa o script Python usando `Python`.
- `all`: Executa o script Python e a métrica `DiademMetric`, salvando os resultados.

Exemplo de uso:

```sh
make runmetric
make clean
make runpy
make all
```
## Info
### Sobre o Package `ip`

O package `ip` contém diversos módulos para processamento de imagens, incluindo:

- `binary.py`: Funções para criação de imagens binárias.
- `enhancement.py`: Funções para aprimoramento de imagens.
- `graph.py` e `graph_nx.py`: Implementações de grafos para análise de imagens.
- `ios.py`: Funções para entrada e saída de imagens.
- `swc.py`: Manipulação de arquivos `SWC`.
- `utils.py`: Funções utilitárias diversas.

Neuronal morphology reconstruction from microscopy images - PIB12628-2023 - Medical image processing in the cloud

## Description

This project aims to reconstruct neuronal morphology from microscopy images. We use cloud-based medical image processing techniques to achieve this task.

## Requirements

We recommend using [Miniforge3](https://github.com/conda-forge/miniforge) to manage packages and virtual environments. You can use `mamba` or `conda` to install the necessary packages.

### Miniforge3 Installation

Follow the instructions on the [Miniforge3](https://github.com/conda-forge/miniforge) repository to install Miniforge3 on your system.

### Creating the Virtual Environment

You can create a new virtual environment or use the `base` environment that is created during the Miniforge3 installation.

### Installing Packages

To install the basic packages needed to run the code, execute the following command:

```sh
mamba install -c conda-forge opencv scikit-image scipy numpy pandas jupyterlab
```
or
```sh
conda install -c conda-forge opencv scikit-image scipy numpy pandas jupyterlab
```
## Running
### Makefile Commands

The `Makefile` contains some useful commands to run and clean the project:

- `runmetric`: Runs the `DiademMetric` metric.
- `clean`: Removes cache and checkpoint files.
- `runpypy`: Runs the Python script using `PyPy`.
- `runpy`: Runs the Python script using `Python`.
- `all`: Runs the Python script and the `DiademMetric` metric, saving the results.

Usage example:

```sh
make runmetric
make clean
make runpy
make all
```
## Info
### About the `ip` Package

The `ip` package contains various modules for image processing, including:

- `binary.py`: Functions for creating binary images.
- `enhancement.py`: Functions for image enhancement.
- `graph.py` and `graph_nx.py`: Graph implementations for image analysis.
- `ios.py`: Functions for image input and output.
- `swc.py`: SWC file manipulation.
- `utils.py`: Various utility functions.
