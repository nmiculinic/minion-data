Description of possible files within each directory:

* **raw:**  Raw fast5 read in tar format
* **checksum.raw.sha512:** checksum of all files in raw/
* **extracted:**  Extracted raw's tars
* **flattened:**  Extracted fast5's are flattened to single directory structure (symlink)
* **sample**: 10 randomly chosen fast5s, hardlinked
* **work_flattened:**  Random subsample of flatten $WORKING_SAMPLE_SIZE big. Almost all further processing works on this directory, not the whole dataset
* **chiron_out:** Chiron basecalled of all work_flattened files
* **basecalled.fastq:** Chiron basecalled of all work_flattened files in single fastq
* **aligement.sam:** Graphmap aligned basecalled.fastq to the reference
* **ref.fasta:** Reference genome

Helper files:
* **ref.fasta.gmidx:** Graphmap's index


