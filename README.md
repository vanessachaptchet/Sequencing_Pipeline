# Sequencing Run Processing Pipeline (Prototype)

This project implements a simplified, robust command-line tool to process sequencing runs and FASTQ samples.
It focuses on structure, error handling, and traceability (not performance).

## Requirements
- Python 3.x
- Linux-compatible
- Git

## Usage

### Step 1: Scan runs and write an overview (current)
```bash
python main.py --input input --outdir output

##
- `output/status_overview.json` (run-level overview; includes `num_samples` = number of FASTQ files per run)



