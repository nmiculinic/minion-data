raw/%:
	mkdir raw
	wget http://s3.climb.ac.uk/nanopore/$* -P raw
checksum.raw.sha512:
	sha512sum raw/* > checksum.raw.sha512

raw: $(shell cat checksum.raw.sha512 | cut -f3 -d ' ')
check-raw: $(shell cat checksum.raw.sha512 | cut -f3 -d ' ')
	sha512sum -c checksum.raw.sha512

$(shell cat checksum.extracted.sha512 | cut -f3 -d ' '): extract
checksum.extracted.sha512:
	sha512sum extracted/* > checksum.extracted.sha512

extract: raw
	find raw -type f -name "*.tar" | sort | parallel -k tar -xf {} --strip-components=1 -Cextracted
check-extracted: $(shell cat checksum.raw.sha512 | cut -f3 -d ' ')
	sha512sum -c checksum.extracted.sha512

sample: # extract
	rm -Rf sample
	mkdir sample
	find extracted -type f | shuf | head | parallel -k cp {} sample
ref.fasta:
	wget 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -O ref.fasta

.PHONY: download extract check-raw sample raw
