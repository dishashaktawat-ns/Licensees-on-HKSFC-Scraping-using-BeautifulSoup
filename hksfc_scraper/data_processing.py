import pandas as pd

def normalize_and_check_schema(records, expected_fields=None):
    """Normalize JSON and detect schema drift"""
    if not records:
        return pd.DataFrame(), expected_fields

    df = pd.json_normalize(records, sep="_")
    current_fields = set(df.columns)

    if expected_fields is not None:
        new_fields = current_fields - expected_fields
        missing_fields = expected_fields - current_fields

        if new_fields:
            print("⚠️ New fields detected:", new_fields)
        if missing_fields:
            print("⚠️ Missing fields:", missing_fields)

    return df, current_fields
