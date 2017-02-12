BASEPATH=schedule/nicar-2017-schedule
.PHONY: schedule 

schedule: scripts/scrape.py
	./scripts/scrape.py > $(BASEPATH).json
	in2csv $(BASEPATH).json > $(BASEPATH).csv
