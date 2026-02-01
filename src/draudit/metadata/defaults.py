from draudit.metadata.types import DatasetMetadata, MetadataField, TrustLevel


def build_default_metadata() -> DatasetMetadata:
    """
    Safe fallback metadata when user provides none.
    """
    missing = MetadataField(value=None, trust=TrustLevel.MISSING)

    return DatasetMetadata(
        target_column=missing,
        time_column=missing,
        problem_type=missing,
        label_description=missing,
        data_source=missing,
    )
