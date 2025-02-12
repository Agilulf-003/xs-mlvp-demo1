PICKER = picker
PYTHON = python3
GTKWAVE = gtkwave
BROWSER = google-chrome

RPT_DIR = report
$(shell mkdir -p ./$(RPT_DIR))

# Generate DUT
TOP_ENTRY = ./rtl/dualPortStack.v
TL = python
WAVEFORM = -w dualPortStack.fst

gen_dut:
	$(PICKER) export ${TOP_ENTRY} --lang ${TL} -c ${WAVEFORM}

.PHONY: wave rpt test
FILE =
FILE_PATH = ./$(RPT_DIR)/fst/dualPortStack_$(FILE).fst

wave:
	$(GTKWAVE) -r .gtkwaverc $(FILE_PATH)
# Test
test:
	-@mkdir $(RPT_DIR)/cov_dat
	-@mkdir $(RPT_DIR)/fst
	-@mkdir $(RPT_DIR)/logs
	PYTHONPATH=. $(PYTHON) __init__.py

rpt:
	$(BROWSER) ./$(RPT_DIR)/rpt.html

clean:
	-rm -rf report
