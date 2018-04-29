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
