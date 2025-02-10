PICKER = picker
PYTHON = python3
GTKWAVE = gtkwave
BROWSER = google-chrome

RPT_DIR = report
$(shell mkdir -p ./$(RPT_DIR))

# Generate DUT
TOP_ENTRY = ./rtl/adder.v
TL = python
WAVEFORM = -w adder.fst

gen_dut:
	$(PICKER) export ${TOP_ENTRY} --lang ${TL} -c ${WAVEFORM}

.PHONY: wave rpt test
FILE =
FILE_PATH = ./$(RPT_DIR)/fst/adder_$(FILE).fst

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
