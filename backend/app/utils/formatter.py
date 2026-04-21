from typing import Any

ROUND_DECIMALS = 2


def round_floats(obj: Any) -> Any:
    """
    Recursively round all float values inside nested structures.
    Leaves ints, strings, None untouched.
    """
    if isinstance(obj, float):
        return round(obj, ROUND_DECIMALS)

    if isinstance(obj, list):
        return [round_floats(x) for x in obj]

    if isinstance(obj, dict):
        return {k: round_floats(v) for k, v in obj.items()}

    return obj


def map_to_original_feature(transformed_name: str) -> str:
    # Handles one-hot encoded names
    return transformed_name.split("_")[0]
