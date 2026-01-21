import gzip

def open_text(path):
    name = str(path).lower()
    if name.endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, "r", encoding="utf-8")

def compute_fastq_metrics(fastq_path):
    """
    FASTQ = 4 lines per read.
    We count reads and compute average read length from sequence lines.
    """
    num_reads = 0
    total_len = 0
    line_index = 0

    f = open_text(fastq_path)
    try:
        for line in f:
            line = line.strip("\n")
            mod = line_index % 4

            # sequence line is the 2nd line of each record (mod == 1)
            if mod == 1:
                total_len += len(line)

            # quality line is the 4th line (mod == 3) => we finished 1 record
            if mod == 3:
                num_reads += 1

            line_index += 1

        if line_index % 4 != 0:
            raise ValueError("Invalid FASTQ: incomplete record (file ended mid-read)")

    finally:
        f.close()

    avg_len = (total_len / num_reads) if num_reads > 0 else 0.0
    return {"num_reads": num_reads, "avg_read_length": avg_len}
