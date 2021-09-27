from dataclasses import dataclass
from pathlib import Path

from templateframework.storage.history_folder import HistoryFolder


@dataclass
class Metadata:
    target_path: Path
    inputs: dict
    history_folder: HistoryFolder
    history_local_filename: str
    filters: dict
    sample_folder: str
    sample: bool
