make-sample:
	find extracted -type f | head | xargs -I {} -n1 cp {} extracted_sample
ref:
	wget 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?tool=portal&save=file&log$=seqview&db=nuccore&report=fasta&id=1356591284&extrafeat=976&conwithfeat=on&hide-sequence=on' -O ref.fasta
