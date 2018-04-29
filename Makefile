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
