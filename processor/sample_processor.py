"""
This module processes individual FASTQ samples.

Each sample is handled independently:
- SUCCESS: metrics are computed correctly
- FAILED: an error occurred (e.g. corrupted FASTQ)

Errors on sample level do not stop the entire run.

"""
import logging
from processor.fastq_utils import compute_fastq_metrics

def process_sample(run_id, fastq_path):
    sample_id = fastq_path.name
    try:
        metrics = compute_fastq_metrics(fastq_path)
        logging.info(f"Sample OK | run={run_id} | sample={sample_id} | reads={metrics['num_reads']}")
        return {"sample_id": sample_id, "status": "SUCCESS", "metrics": metrics}
    except Exception as e:
        logging.exception(f"Sample FAILED | run={run_id} | sample={sample_id} | reason={e}")
        return {"sample_id": sample_id, "status": "FAILED", "error": str(e)}
