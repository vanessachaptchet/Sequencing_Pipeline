from pathlib import Path

def validate_input_dir(input_dir):
    if not input_dir.exists() or not input_dir.is_dir():
        raise ValueError(f"Input directory not found or not a directory: {input_dir}")

def find_run_dirs(input_dir):
    runs = []
    for p in input_dir.iterdir():
        if p.is_dir():
            name = p.name
            # ignore hidden folders and common non-run folders
            if name.startswith("."):
                continue
            if name in ["output", "logs", "__pycache__", "processor", "mvz_task", "input"]:
                continue
            runs.append(p)
    return runs

###
def find_fastq_files(run_dir):
    fastq_files = []
    for p in run_dir.rglob("*"):
        if p.is_file():
            name = p.name.lower()
            if name.endswith(".fastq") or name.endswith(".fq") or name.endswith(".fastq.gz") or name.endswith(".fq.gz"):
                fastq_files.append(p)
    return fastq_files
