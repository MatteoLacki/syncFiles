# Rationale
Move files on windows.


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

# Nice things
All copy tasks are logged (by default in C:\Logs\sync.log).
After copying, files are compared for sizes and check sums.
