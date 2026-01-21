"""
This module aggregates sample-level results into run-level reports
and writes structured JSON output files.

Outputs produced by the pipeline:
- status_overview.json  (one entry per run)
- status_detailed.json  (full sample-level details per run)
"""

import json
from processor.run_scanner import find_fastq_files
from processor.sample_processor import process_sample

def write_json(data, output_path):              # Write a Python object as formatted JSON to a file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

"""
Determine the final run status based on sample results.

    Rules:
    - SUCCESS: all samples succeeded
    - FAILED: all samples failed OR there are zero samples
    - PARTIAL: Mixture of FAILED and SUCCESS Samples
    
    """
def evaluate_run_status(sample_results):
    total = len(sample_results)
    failed = 0
    for r in sample_results:
        if r["status"] == "FAILED":
            failed += 1

    if total == 0:
        return "FAILED"
    if failed == 0:
        return "SUCCESS"
    if failed == total:
        return "FAILED"
    return "PARTIAL"


"""
  Process all runs and build both detailed and overview reports.

    Parameters:
    run_dirs : list[Path]
        List of run directories found in the input folder.

    Returns:
    detailed : list[dict]
        Per-run detailed results including all sample results.
    overview : list[dict]
        Per-run summary with number of samples, run status, and failed count.
    """
def build_detailed_and_overview(run_dirs):
    detailed = []
    overview = []

    for run_dir in run_dirs:
        run_id = run_dir.name
        fastq_files = find_fastq_files(run_dir)

        sample_results = []
        for fq in fastq_files:
            sample_results.append(process_sample(run_id, fq))

        run_status = evaluate_run_status(sample_results)
        failed_samples = sum(1 for r in sample_results if r["status"] == "FAILED")

        detailed.append({
            "run_id": run_id,
            "samples": sample_results
        })

        overview.append({
            "run_id": run_id,
            "num_samples": len(sample_results),
            "run_status": run_status,
            "failed_samples": failed_samples
        })

    return detailed, overview
