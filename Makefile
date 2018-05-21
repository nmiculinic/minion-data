
.FORCE:
proto: .FORCE
	python -m grpc_tools.protoc -I $$(pwd)/protos --mypy_out=./minion_data --python_out=./minion_data $$(pwd)/protos/*

USERNAME=""
TAG="latest"

ifeq ($(strip $(USERNAME)), "")
	BASE_TAG=""
else
	BASE_TAG=$(USERNAME)/
endif

docker-build:
	docker build -t $(BASE_TAG)minion_data:$(TAG)  .

.PHONY: docker-build

docker-push: docker-build
	docker push $(BASE_TAG)minion_data:$(TAG)
.PHONY: docker-push

# Reference hybrid assembly
rwick_basecaller/01_raw_fast5/barcode01.fasta.gz:
	@mkdir -p rwick_basecaller/01_raw_fast5
	wget https://ndownloader.figshare.com/files/8810704 -O $@

# Illumina reads
rwick_basecaller/01_raw_fast5/barcode01_1.fastq.gz:
	@mkdir -p rwick_basecaller/01_raw_fast5
	wget https://ndownloader.figshare.com/files/8811145 -O $@

rwick_basecaller/01_raw_fast5/barcode01_2.fastq.gz:
	@mkdir -p rwick_basecaller/01_raw_fast5
	wget https://ndownloader.figshare.com/files/8811148 -O $@

# Raw fast5 files

rwick_basecaller/.done: rwick_basecaller/01_raw_fast5/barcode01_2.fastq.gz rwick_basecaller/01_raw_fast5/barcode01_1.fastq.gz rwick_basecaller/01_raw_fast5/barcode01.fasta.gz
	@mkdir -p rwick_basecaller/02_basecalled_reads
	@touch $@

rwick: rwick_basecaller/.done

sample-make-sample:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: sample-make-sample

sample-download_ref:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: sample-download_ref

sample-clean:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' clean -f ../single.Makefile
.PHONY: sample-clean

sample-check:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' check-raw -f ../single.Makefile
.PHONY: sample-check

sample-create-check:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' --always-make checksum.raw.sha512 -f ../single.Makefile
.PHONY: sample-create-check

sample-chiron_basecall:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L chiron_basecall -f ../single.Makefile
.PHONY: sample-chiron_basecall

sample-align:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L alignment.sam -f ../single.Makefile
.PHONY: sample-align

sample-prepare_dataset:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L prepare_dataset -f ../single.Makefile
.PHONY: sample-prepare_dataset
r9.4-sample-make-sample:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: r9.4-sample-make-sample

r9.4-sample-download_ref:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: r9.4-sample-download_ref

r9.4-sample-clean:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' clean -f ../single.Makefile
.PHONY: r9.4-sample-clean

r9.4-sample-check:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' check-raw -f ../single.Makefile
.PHONY: r9.4-sample-check

r9.4-sample-create-check:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' --always-make checksum.raw.sha512 -f ../single.Makefile
.PHONY: r9.4-sample-create-check

r9.4-sample-chiron_basecall:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L chiron_basecall -f ../single.Makefile
.PHONY: r9.4-sample-chiron_basecall

r9.4-sample-align:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L alignment.sam -f ../single.Makefile
.PHONY: r9.4-sample-align

r9.4-sample-prepare_dataset:
	@$(MAKE) --no-print-directory -C r9.4-sample -e BASE_URL='MISSING!' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L prepare_dataset -f ../single.Makefile
.PHONY: r9.4-sample-prepare_dataset
ecoli-loman-make-sample:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: ecoli-loman-make-sample

ecoli-loman-download_ref:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: ecoli-loman-download_ref

ecoli-loman-clean:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' clean -f ../single.Makefile
.PHONY: ecoli-loman-clean

ecoli-loman-check:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' check-raw -f ../single.Makefile
.PHONY: ecoli-loman-check

ecoli-loman-create-check:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' --always-make checksum.raw.sha512 -f ../single.Makefile
.PHONY: ecoli-loman-create-check

ecoli-loman-chiron_basecall:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L chiron_basecall -f ../single.Makefile
.PHONY: ecoli-loman-chiron_basecall

ecoli-loman-align:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L alignment.sam -f ../single.Makefile
.PHONY: ecoli-loman-align

ecoli-loman-prepare_dataset:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L prepare_dataset -f ../single.Makefile
.PHONY: ecoli-loman-prepare_dataset
r9.4-ecoli-loman-make-sample:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: r9.4-ecoli-loman-make-sample

r9.4-ecoli-loman-download_ref:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: r9.4-ecoli-loman-download_ref

r9.4-ecoli-loman-clean:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' clean -f ../single.Makefile
.PHONY: r9.4-ecoli-loman-clean

r9.4-ecoli-loman-check:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' check-raw -f ../single.Makefile
.PHONY: r9.4-ecoli-loman-check

r9.4-ecoli-loman-create-check:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' --always-make checksum.raw.sha512 -f ../single.Makefile
.PHONY: r9.4-ecoli-loman-create-check

r9.4-ecoli-loman-chiron_basecall:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L chiron_basecall -f ../single.Makefile
.PHONY: r9.4-ecoli-loman-chiron_basecall

r9.4-ecoli-loman-align:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L alignment.sam -f ../single.Makefile
.PHONY: r9.4-ecoli-loman-align

r9.4-ecoli-loman-prepare_dataset:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-loman -e BASE_URL='http://s3.climb.ac.uk/nanopore' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L prepare_dataset -f ../single.Makefile
.PHONY: r9.4-ecoli-loman-prepare_dataset
ecoli-simpson-make-sample:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: ecoli-simpson-make-sample

ecoli-simpson-download_ref:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: ecoli-simpson-download_ref

ecoli-simpson-clean:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' clean -f ../single.Makefile
.PHONY: ecoli-simpson-clean

ecoli-simpson-check:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' check-raw -f ../single.Makefile
.PHONY: ecoli-simpson-check

ecoli-simpson-create-check:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' --always-make checksum.raw.sha512 -f ../single.Makefile
.PHONY: ecoli-simpson-create-check

ecoli-simpson-chiron_basecall:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L chiron_basecall -f ../single.Makefile
.PHONY: ecoli-simpson-chiron_basecall

ecoli-simpson-align:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L alignment.sam -f ../single.Makefile
.PHONY: ecoli-simpson-align

ecoli-simpson-prepare_dataset:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L prepare_dataset -f ../single.Makefile
.PHONY: ecoli-simpson-prepare_dataset
r9.4-ecoli-simpson-make-sample:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: r9.4-ecoli-simpson-make-sample

r9.4-ecoli-simpson-download_ref:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L sample -f ../single.Makefile
.PHONY: r9.4-ecoli-simpson-download_ref

r9.4-ecoli-simpson-clean:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' clean -f ../single.Makefile
.PHONY: r9.4-ecoli-simpson-clean

r9.4-ecoli-simpson-check:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' check-raw -f ../single.Makefile
.PHONY: r9.4-ecoli-simpson-check

r9.4-ecoli-simpson-create-check:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' --always-make checksum.raw.sha512 -f ../single.Makefile
.PHONY: r9.4-ecoli-simpson-create-check

r9.4-ecoli-simpson-chiron_basecall:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L chiron_basecall -f ../single.Makefile
.PHONY: r9.4-ecoli-simpson-chiron_basecall

r9.4-ecoli-simpson-align:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L alignment.sam -f ../single.Makefile
.PHONY: r9.4-ecoli-simpson-align

r9.4-ecoli-simpson-prepare_dataset:
	@$(MAKE) --no-print-directory -C r9.4-ecoli-simpson -e BASE_URL='MISSING' REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -L prepare_dataset -f ../single.Makefile
.PHONY: r9.4-ecoli-simpson-prepare_dataset
arabidopsis_thaliana-leggett-make-sample:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L sample -f ../single.Makefile
.PHONY: arabidopsis_thaliana-leggett-make-sample

arabidopsis_thaliana-leggett-download_ref:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L sample -f ../single.Makefile
.PHONY: arabidopsis_thaliana-leggett-download_ref

arabidopsis_thaliana-leggett-clean:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' clean -f ../single.Makefile
.PHONY: arabidopsis_thaliana-leggett-clean

arabidopsis_thaliana-leggett-check:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' check-raw -f ../single.Makefile
.PHONY: arabidopsis_thaliana-leggett-check

arabidopsis_thaliana-leggett-create-check:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' --always-make checksum.raw.sha512 -f ../single.Makefile
.PHONY: arabidopsis_thaliana-leggett-create-check

arabidopsis_thaliana-leggett-chiron_basecall:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L chiron_basecall -f ../single.Makefile
.PHONY: arabidopsis_thaliana-leggett-chiron_basecall

arabidopsis_thaliana-leggett-align:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L alignment.sam -f ../single.Makefile
.PHONY: arabidopsis_thaliana-leggett-align

arabidopsis_thaliana-leggett-prepare_dataset:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L prepare_dataset -f ../single.Makefile
.PHONY: arabidopsis_thaliana-leggett-prepare_dataset
r9.4-arabidopsis_thaliana-leggett-make-sample:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L sample -f ../single.Makefile
.PHONY: r9.4-arabidopsis_thaliana-leggett-make-sample

r9.4-arabidopsis_thaliana-leggett-download_ref:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L sample -f ../single.Makefile
.PHONY: r9.4-arabidopsis_thaliana-leggett-download_ref

r9.4-arabidopsis_thaliana-leggett-clean:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' clean -f ../single.Makefile
.PHONY: r9.4-arabidopsis_thaliana-leggett-clean

r9.4-arabidopsis_thaliana-leggett-check:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' check-raw -f ../single.Makefile
.PHONY: r9.4-arabidopsis_thaliana-leggett-check

r9.4-arabidopsis_thaliana-leggett-create-check:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' --always-make checksum.raw.sha512 -f ../single.Makefile
.PHONY: r9.4-arabidopsis_thaliana-leggett-create-check

r9.4-arabidopsis_thaliana-leggett-chiron_basecall:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L chiron_basecall -f ../single.Makefile
.PHONY: r9.4-arabidopsis_thaliana-leggett-chiron_basecall

r9.4-arabidopsis_thaliana-leggett-align:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L alignment.sam -f ../single.Makefile
.PHONY: r9.4-arabidopsis_thaliana-leggett-align

r9.4-arabidopsis_thaliana-leggett-prepare_dataset:
	@$(MAKE) --no-print-directory -C r9.4-arabidopsis_thaliana-leggett -e BASE_URL='MISSING' REF_URL='Unknown' -L prepare_dataset -f ../single.Makefile
.PHONY: r9.4-arabidopsis_thaliana-leggett-prepare_dataset
