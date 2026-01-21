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


## What the tool does
- Iterates over run directories inside `--input`
- Processes each FASTQ file (sample) independently
- Computes per-sample metrics:
  - `num_reads`
  - `avg_read_length`
- Determines run status:
  - SUCCESS (all samples ok)
  - FAILED (all samples failed)
  - PARTIAL (mix of success and failure)

## Outputs
- `output/status_overview.json`:
  - run_id, num_samples, run_status, failed_samples
- `output/status_detailed.json`:
  - per-run list of samples with metrics or error message

## Error handling
- Sample-level failures do not stop run processing
- Errors are logged with run_id + sample_id + reason
- Run status reflects sample outcomes (SUCCESS/FAILED/PARTIAL)

## Monitoring (conceptual)
In production, we would monitor:
- Number of runs processed per hour/day
- Percentage of runs in FAILED/PARTIAL
- Error rate per error type (e.g., corrupted FASTQ, missing files)
- Processing duration per run/sample (latency)
- Throughput: samples processed per minute

Error escalation approach:
- Alert when FAILED/PARTIAL rate exceeds a threshold
- Alert when a run stays in a non-terminal state too long
- Notify operators via Email/Slack/PagerDuty
- Optional automatic retry for transient IO errors

Suggested tools:
- Metrics: Prometheus + Grafana dashboards/alerts
- Logs: ELK/EFK stack (Elasticsearch/OpenSearch + Logstash/Fluentd + Kibana)
- Tracing (optional): OpenTelemetry



