from statistics import mean


def get_average_name_length(names: list[str]) -> float:
    """Calculate the average length of customer names."""
    return mean(len(name) for name in names)


def find_name_closest_to_average_length(names: list[str], average_length: float) -> str:
    """Find the name with length closest to the average length."""
    return min(names, key=lambda name: abs(len(name) - average_length))
