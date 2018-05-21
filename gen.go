package main

import (
	"fmt"
	"os"
	"text/template"
	"log"
)

/*

tt_EXTRA := -C tt -e BASE_URL="" -e REF_URL=""
r9.4-ecoli-loman_EXTRA := -C r9.4-ecoli-loman -e BASE_URL="http://s3.climb.ac.uk/nanopore" -e REF_URL="https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on"
r9.4-ecoli-simpson_EXTRA := -C r9.4-ecoli-simpson -e BASE_URL="INVALID!!!" -e REF_URL="https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on"
r9.4-human-chr21_EXTRA:= -C r9.4-human-chr21 -e BASE_URL="http://s3.amazonaws.com/nanopore-human-wgs" -e REF_URL="https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=568815577&extrafeat=976&conwithfeat=on&hide-sequence=on"

r9.4-leggett_EXTRA:= -C "r9.4-arabidopsis_thaliana-leggett" -e BASE_URL="" -e REF_URL=""


r9.4-sample_EXTRA := -C r9.4-sample -e BASE_URL="" -e REF_URL='https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on'

.PHONY: sample-tt clean-tt

sample-%:
	@$(MAKE) --no-print-directory $($*_EXTRA) -L sample -f ../single.Makefile
#	@$(MAKE) --no-print-directory $($*_EXTRA) -L ref.fasta -f ../single.Makefile
clean-%:
	@$(MAKE) --no-print-directory $($*_EXTRA) clean -f ../single.Makefile
check-%:
	@$(MAKE) --no-print-directory $($*_EXTRA) check-raw -f ../single.Makefile
	# @$(MAKE) --no-print-directory $($*_EXTRA) check-extracted -f ../single.Makefile
create-check-%:
	@$(MAKE) --no-print-directory $($*_EXTRA) --always-make checksum.raw.sha512 -f ../single.Makefile
	# @$(MAKE) --no-print-directory $($*_EXTRA) --always-make checksum.extracted.sha512 -f ../single.Makefile

*/

const tmpl = `
{{- $extra := printf "-C %s -e BASE_URL='%s' REF_URL='%s'" .Folder .BaseURL .RefURL -}}
{{ .Name }}-make-sample:
{{ print "\t" -}} @$(MAKE) --no-print-directory {{ $extra }} -L sample -f ../single.Makefile
.PHONY: {{ .Name }}-make-sample

{{ .Name }}-download_ref:
{{ print "\t" -}} @$(MAKE) --no-print-directory {{ $extra }} -L sample -f ../single.Makefile
.PHONY: {{ .Name }}-download_ref

{{ .Name }}-clean:
{{ print "\t" -}}@$(MAKE) --no-print-directory {{ $extra }} clean -f ../single.Makefile
.PHONY: {{ .Name }}-clean

{{ .Name }}-check:
{{ print "\t" -}}@$(MAKE) --no-print-directory {{ $extra }} check-raw -f ../single.Makefile
.PHONY: {{ .Name }}-check

{{ .Name }}-create-check:
{{ print "\t" -}}@$(MAKE) --no-print-directory {{ $extra }} --always-make checksum.raw.sha512 -f ../single.Makefile
.PHONY: {{ .Name }}-create-check

{{ .Name }}-chiron_basecall:
{{ print "\t" -}} @$(MAKE) --no-print-directory {{ $extra }} -L chiron_basecall -f ../single.Makefile
.PHONY: {{ .Name }}-chiron_basecall

{{ .Name }}-align:
{{ print "\t" -}} @$(MAKE) --no-print-directory {{ $extra }} -L alignment.sam -f ../single.Makefile
.PHONY: {{ .Name }}-align

{{ .Name }}-prepare_dataset:
{{ print "\t" -}} @$(MAKE) --no-print-directory {{ $extra }} -L prepare_dataset -f ../single.Makefile
.PHONY: {{ .Name }}-prepare_dataset
`

type Item struct {
	Name    string // Alias for running
	BaseURL string // BaseURL for downloading raw files
	RefURL  string // URL for downloading ref.fasta, that is reference genome
	Folder  string // Folder where all data should be saved/processed
}

const EColiRef = "https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on"

func main() {
	fmt.Println(`
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
rwick_basecaller/01_raw_fast5/INF042_raw_fast5.tar:
	@mkdir -p rwick_basecaller/01_raw_fast5
	wget https://ndownloader.figshare.com/files/9199063 -O $@

rwick_basecaller/.done: rwick_basecaller/01_raw_fast5/barcode01_2.fastq.gz rwick_basecaller/01_raw_fast5/barcode01_1.fastq.gz rwick_basecaller/01_raw_fast5/barcode01.fasta.gz rwick_basecaller/01_raw_fast5/INF042_raw_fast5.tar
	@mkdir -p rwick_basecaller/02_basecalled_reads
	tar -xf rwick_basecaller/01_raw_fast5/INF042_raw_fast5.tar --directory rwick_basecaller/01_raw_fast5
	@touch $@

rwick: rwick_basecaller/.done
`)
	t := template.Must(template.New("x").Parse(tmpl))
	for _, f := range []Item{
		{
			Name:    "sample",
			Folder:  "r9.4-sample",
			RefURL:  EColiRef,
			BaseURL: "MISSING!",
		},
		{
			Name:    "ecoli-loman",
			Folder:  "r9.4-ecoli-loman",
			RefURL:  EColiRef,
			BaseURL: "http://s3.climb.ac.uk/nanopore",
		},
		{
			Name:    "ecoli-simpson",
			Folder:  "r9.4-ecoli-simpson",
			RefURL:  EColiRef,
			BaseURL: "MISSING",
		},
		{
			Name:    "arabidopsis_thaliana-leggett",
			Folder:  "r9.4-arabidopsis_thaliana-leggett",
			RefURL:  "Unknown",
			BaseURL: "MISSING",
		},
	} {
		if f.Name != "" {
			if err := t.Execute(os.Stdout, f); err != nil {
				log.Fatal(err)
			}
		}
		// for aliased datasets
		if f.Name != f.Folder {
			f.Name = f.Folder
			if err := t.Execute(os.Stdout, f); err != nil {
				log.Fatal(err)
			}
		}
	}
}
