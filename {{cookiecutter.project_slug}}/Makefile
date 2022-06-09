# Parallel job execution - comment out this line to have all tasks run sequentially
MAKEFLAGS := --jobs=$(shell nproc)

# "functions"
to_command = python -m $(PROJECT) $(shell echo $(subst _,-,$(1)) | tr '[:upper:]' '[:lower:]')
from_import = $(shell python -c "import $(PROJECT); print($(PROJECT).$(1))")

# Directories to search
PROJECT := $(notdir $(subst -,_,$(CURDIR)))
TARGETDIR := target
SQLDIR := sql
DATADIR := data
AUTODIR := $(TARGETDIR)/auto
VPATH := $(SQLDIR):$(TARGETDIR):$(AUTODIR):$(DATADIR)

# Automatic targets from all SQL files
OBJS := $(wildcard $(SQLDIR)/*.sql)
TARGETS := $(patsubst $(SQLDIR)/%.sql,%.ctas,$(OBJS))

# Default target - construct all the analytics tables
tables: $(TARGETS)

$(TARGETS): config.yml $(PROJECT) | $(TARGETDIR) $(DATADIR)

$(TARGETDIR):
	mkdir -p $(TARGETDIR)
	mkdir -p $(AUTODIR)

$(DATADIR):
	mkdir -p $(DATADIR)

# ============================= Main DAG ====================================
# The main table and file dependency graph goes here, of the form:
#   target(s): one or more dependencies
#
# Database table, requires sql/<name>.sql to exist
#   <name>.ctas
#
# Flat files, requires the python function `<name>_csv` or `<name>_excel` in <project>/commands.py
#   <name>.csv/.xlsx
#
# Visualizations, requires the python function `<name>_chart` in <project>/commands.py
#   <name>.png/.svg/.html
#
#
# prerequisite.ctas:
# target.ctas: prereqisite.ctas

# ========================= Automatic Rules =================================
# Empty targets ending with ".ctas" indicate a completed CTAS execution
%.ctas: %.sql | $(TARGETDIR) $(DATADIR)
	python -m $(PROJECT) ctas $<
	@touch $(AUTODIR)/$@

pyfunc_%: $(PROJECT) | $(TARGETDIR)
	$(call to_command,$(patsubst pyfunc_%,%,$@))
	touch $(AUTODIR)/$@

%.jpg %.png %.html %.svg:
	$(call to_command,$*)-chart

%.xlsx:
	$(call to_command,$*)-excel

%.csv:
	$(call to_command,$*)-csv

# =========================== Misc. Content =================================
.PHONY: clean
clean:
	@[ ! -d $(TARGETDIR) ] || rm -r $(TARGETDIR)
	@[ ! -d $(DATADIR) ] || rm -r $(DATADIR)

.PHONY: poetry
poetry:
	@curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install
install: data poetry
	@~/.local/bin/poetry install --no-dev

.PHONY: install-dev
install-dev: data poetry
	@~/.local/bin/poetry install
	@pre-commit install
