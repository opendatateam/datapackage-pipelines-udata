WIP

## Install

```
$ git clone https://github.com/opendatateam/datapackage-pipelines-udata
$ cd datapackage-pipelines-udata
$ pip install -e .
```

## Usage

### Generators

#### Transform a remote dataset into a local datapackage

Start with pipeline generator `udata.source-spec.yaml`

```
name: organigramme
udata-instance: data.gouv.fr
data-kind: dataset
dataset: referentiel-de-lorganisation-administrative-de-letat
```

Run the pipeline

```
$ dpp run organigramme
```

Enjoy!

### Processors
