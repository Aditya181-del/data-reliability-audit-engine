import json
import os
from typing import Dict

import yaml

from draudit.metadata.types import DatasetMetadata, MetadataField, TrustLevel


SUPPORTED_FORMATS = {".yaml", ".yml", ".json"}


def _parse_metadata_field(raw: Dict) -> MetadataField:
    """
    Parse a single metadata field dict into a MetadataField object.
    """

    if not isinstance(raw, dict):
        raise ValueError("Metadata field must be a dictionary")

    value = raw.get("value", None)
    trust_raw = raw.get("trust", "missing")

    try:
        trust = TrustLevel(trust_raw)
    except ValueError:
        raise ValueError(f"Invalid trust level: {trust_raw}")

    return MetadataField(value=value, trust=trust)


def load_metadata(metadata_path: str) -> DatasetMetadata:
    """
    Load dataset metadata from a YAML or JSON file.

    This function:
    - Loads metadata deterministically
    - Validates shape and trust levels
    - Does NOT validate semantic correctness
    """

    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    ext = os.path.splitext(metadata_path)[1].lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported metadata format: {ext}")

    with open(metadata_path, "r", encoding="utf-8") as f:
        if ext in {".yaml", ".yml"}:
            raw_metadata = yaml.safe_load(f)
        else:
            raw_metadata = json.load(f)

    raw_metadata = raw_metadata or {}

    return DatasetMetadata(
        target_column=_parse_metadata_field(raw_metadata.get("target_column", {})),
        time_column=_parse_metadata_field(raw_metadata.get("time_column", {})),
        problem_type=_parse_metadata_field(raw_metadata.get("problem_type", {})),
        label_description=_parse_metadata_field(
            raw_metadata.get("label_description", {})
        ),
        data_source=_parse_metadata_field(raw_metadata.get("data_source", {})),
    )
