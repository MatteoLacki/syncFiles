# Rationale
Move files from one place to another (e.g. windows network folder).
Then, compare the files for sizes and check sums and log everything.


# Installation

```{bash}
    pip install syncFiles
```

# Usage:

```{bash}
	python3 syncFiles C:\your\path\pattern\for\files\f*.raw E:\your\target\folder --min_age_hours 24
```

For help, run:
```{bash}
	python3 syncFiles -h
```

# Logging
All copy tasks are logged, by default in C:\Logs\sync.log

