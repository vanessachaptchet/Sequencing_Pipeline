import argparse
import logging
from pathlib import Path

from processor.run_scanner import validate_input_dir, find_run_dirs
from processor.output_writer import build_detailed_and_overview, write_json
from processor.logging_utils import setup_logging


def parse_args():
    parser = argparse.ArgumentParser(description="Sequencing run processing pipeline (prototype)")
    parser.add_argument("--input", required=True, help="Directory containing sequencing run folders")
    parser.add_argument("--outdir", required=True, help="Directory where results will be written")
    parser.add_argument("--log", required=True, help="Log file path")
    return parser.parse_args()


def main():
    args = parse_args()

    input_dir = Path(args.input)
    outdir = Path(args.outdir)
    log_path = Path(args.log)

    setup_logging(log_path)
    logging.info("Pipeline started")

    try:
        validate_input_dir(input_dir)

        run_dirs = find_run_dirs(input_dir)
        logging.info(f"Runs found: {len(run_dirs)}")

        detailed, overview = build_detailed_and_overview(run_dirs)

        overview_path = outdir / "status_overview.json"
        detailed_path = outdir / "status_detailed.json"

        write_json(overview, overview_path)
        write_json(detailed, detailed_path)

        logging.info(f"Overview written to: {overview_path}")
        logging.info(f"Detailed written to: {detailed_path}")

    except Exception as e:
        logging.exception(f"Pipeline failed: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
