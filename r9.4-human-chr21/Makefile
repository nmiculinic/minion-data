raw/rel3-fast5-chr21.part0%.tar:
	wget http://s3.amazonaws.com/nanopore-human-wgs/rel3-fast5-chr21.part0$*.tar -P raw
part-%: raw/rel3-fast5-chr21.part0%.tar:
download: part-1 part-2 part-3
ref:
	wget 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=568815577&extrafeat=976&conwithfeat=on&hide-sequence=on' -O ref.fasta

.PHONY: download
