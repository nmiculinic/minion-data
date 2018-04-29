### Requirements

This aims to have minimal requirements, due to putting everything in docker containers. Still some are obligatory:

* docker
* make
* parallel
* wget

### Usage:

Most common usage is:

```
make <dataset name>-prepare_dataset
```

and it will do everything automatically. The Makefile is generated from `gen.go` so it's worth checking it out.

### Folder structure:

* **bin:** Various binary utilites to make this possible. Mostly since ":" char and makefile doesn't play nice, and it's essential for docker
* **minion_data** Root package folder for further data processing. Should be run `__main__.py__` or even better as module `python -m minion_data`
* **protos** Protobuff file descriptors

Each data source contains (or will contain) following files/folders:

* **raw:**  Raw fast5 read in tar format
* **checksum.raw.sha512:** checksum of all files in raw/
* **extracted:**  Extracted raw's tars
* **flattened:**  Extracted fast5's are flattened to single directory structure (symlink)
* **sample**: 10 randomly chosen fast5s, hardlinked
* **work_flattened:**  Random subsample of flatten `$WORKING_SAMPLE_SIZE` big. Almost all further processing works on this directory, not the whole dataset
* **chiron_out:** Chiron basecalled of all work_flattened files
* **basecalled.fastq:** Chiron basecalled of all work_flattened files in single fastq
* **aligement.sam:** Graphmap aligned basecalled.fastq to the reference
* **ref.fasta:** Reference genome
* **dataset:** Prepared dataset. It's gziped protobuf defined in `protos/dataset.proto` called `DataPoint`

Helper files:
* **ref.fasta.gmidx:** Graphmap's index

Example one is `r9.4-sample`, others are names `<chemistry>-<specie>-<source>`


