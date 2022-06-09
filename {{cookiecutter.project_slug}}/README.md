# Prerequisites

1. Must be on a \*nix system that has `curl` and `make`, such as linux, macOS, or
   Windows Subsystem for Linux (WSL)
2. The `poetry` command, which can be installed via `make poetry`


# Installation

Use the poetry environment for all commands; either via `poetry run` or 
the dedicated shell:

```
$ poetry shell
$ make install
```

Or, for a developer install,

```
$ make install-dev
```

Then, to run the DAG:

```
$ make tables
```
