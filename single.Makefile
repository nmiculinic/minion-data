BASE_URL := "UNSET!!!"
REF_URL := "UNSET!!!"
WORKING_SAMPLE_SIZE=2000

## Raw files related stuff
raw/%:
	@echo "downloading missing raw files $@ to $$(pwd)/raw"
	@mkdir -p raw
	wget $(BASE_URL)/$* -P raw
checksum.raw.sha512:
	sha512sum raw/* > checksum.raw.sha512

raw/.done: $(shell cat checksum.raw.sha512 | cut -f3 -d ' ')
	@echo "Missing following raw files $+"
	@touch $@

download: raw/.done
	@:
check-raw: $(shell cat checksum.raw.sha512 | cut -f3 -d ' ')
	sha512sum -c checksum.raw.sha512



## Extract related stuff
# $(shell cat checksum.extracted.sha512 | cut -f3 -d ' '): extracted/.done
extracted/.done: raw/.done
	@echo "Extracting the raw tars to $$(pwd)/extracted"
	@mkdir -p extracted
	@find raw -type f -name "*.tar" | parallel -k tar -xf {} -C extracted
	@find raw -type f -name "*.tar.gz" | parallel -k tar -xf {} -C extracted
	@find raw -type f -name "*.tgz" | parallel -k tar -xzf {} -C extracted
	@echo "extracted all files from raw/ to extracted/"
	@touch $@

extract: extracted/.done
	@:
checksum.extracted.sha512:
	find extracted -type f | xargs -I {} sha512sum {} > checksum.extracted.sha512
check-extracted: extract
	sha512sum -c checksum.extracted.sha512

## Flatten all reads into single directory
flattened/.done: extracted/.done
	@mkdir -p flattened
	@echo "Flattening the extracted files to $$(pwd)/flattened"
	@find extracted -type f -not -path '*/\.*' -exec ln -sr {} -t flattened \;
	@echo "flattened all files"
	@touch $@

flatten: flattened/.done
	@:

work_flatten/.done: flattened/.done
	@echo "Sampling $(WORKING_SAMPLE_SIZE) flattened files to $$(pwd)/work_flatten"
	@rm -Rf work_flatten
	@mkdir work_flatten
	@find flattened \( -type f -or -type l \) -name '*.fast5' | shuf | head -n $(WORKING_SAMPLE_SIZE) | parallel -k ln -Lsr {} work_flatten
	@echo "sampled $(WORKING_SAMPLE_SIZE) files"
	@touch $@

work_flatten: work_flatten/.done
    @:

all-reads.txt: flattened/.done raw/.done
	@find flattened -mindepth 1 -not -path '*/\.*'  > all-reads.txt

sample: flattened/.done
	@echo "Sampling the flattened files to $$(pwd)/sample"
	@rm -Rf sample
	@mkdir sample
	@find extracted -type f -name '*.fast5' | shuf | head | parallel -k ln {} sample
	@echo "sampled 10 files"
clean:
	rm -Rf extracted flattened sample work_flatten
ref.fasta:
	@wget $(REF_URL) -O ref.fasta

.PHONY: extract download sample check-raw check-extracted tt

chiron_out/.done: work_flatten/.done
	../bin/chiron_basecall $$(pwd) work_flatten chiron_out
	@echo "Basecalled all files with chiron"
	@touch $@

basecalled.fastq: chiron_out/.done
	@cat chiron_out/result/*.fastq > basecalled.fastq

chiron_basecall: basecalled.fastq
	@:
.PHONY: chiron_basecall

alignment.sam: basecalled.fastq
	../bin/graphmap $$(pwd) basecalled.fastq $@

