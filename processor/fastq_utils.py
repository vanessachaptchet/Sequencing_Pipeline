"""
This module contains helper functions to read FASTQ files
(plain text or gzipped) and compute basic sequencing metrics.

Implemented metrics:
- number of reads
- average read length
"""

import gzip
from pathlib import Path


def open_text(path: Path):
    """
    Open a FASTQ file as text.

    Supports:
    - .fastq / .fq (plain text)
    - .fastq.gz / .fq.gz (gzipped)

    Returns a file handle that can be used in a for-loop.
    """
    name = str(path).lower()
    if name.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, "r", encoding="utf-8")


def compute_fastq_metrics(fastq_path: Path) -> dict:
    """
    Compute basic metrics for a FASTQ file.

    FASTQ format:
    Each read consists of 4 lines:
      1) header
      2) sequence
      3) plus line
      4) quality

    We count reads and compute average read length using the sequence lines.
    """
    num_reads = 0
    total_len = 0
    line_index = 0

    f = open_text(fastq_path)
    try:
        for line in f:
            line = line.strip("\n")
            mod = line_index % 4

            # Sequence line = 2nd line of the 4-line FASTQ record
            if mod == 1:
                total_len += len(line)

            # Quality line = 4th line => completed one read
            if mod == 3:
                num_reads += 1

            line_index += 1

        # If file ends in the middle of a record, it's an invalid FASTQ
        if line_index % 4 != 0:
            raise ValueError("Invalid FASTQ: incomplete record (file ended mid-read)")

    finally:
        f.close()

    avg_len = (total_len / num_reads) if num_reads > 0 else 0.0
    return {"num_reads": num_reads, "avg_read_length": avg_len}
