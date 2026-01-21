"""
This module configures logging for the pipeline.
It writes log messages to:
1) the console (so the user can see progress)
2) a log file (so errors and events are stored for later debugging)
"""

import logging
from pathlib import Path


def setup_logging(log_path: Path) -> None:
    """
    Configure logging for the pipeline.

    Parameters
    log_path : Path
        Path to the log file, e.g. logs/pipeline.log
    """
    # Create the log directory if it does not exist (e.g. "logs/")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
