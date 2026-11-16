def process_name(name):
    """Normalize a name, returning an empty string for non-string input."""
    if not isinstance(name, str):
        return ""
    return name.strip().title()


def calculate_average(numbers):
    """Calculate the average of a list of numbers; return 0.0 for invalid input."""
    if not isinstance(numbers, list) or len(numbers) == 0:
        return 0.0

    if not all(
        isinstance(n, (int, float)) and not isinstance(n, bool)
        for n in numbers
    ):
        return 0.0

    return sum(numbers) / len(numbers)


def process_age(age):
    """Convert an age to an integer; reject invalid or negative values."""
    try:
        age = int(age)
        if age < 0:
            return None
        return age
    except (ValueError, TypeError):
        return None


if __name__ == "__main__":
    print("Testing Fixed Processor Application")
    print("Name:", process_name(" sharath reddy "))
    print("Average:", calculate_average([10, 20, 30]))
    print("Age:", process_age("21"))

    print("\nTesting Invalid Inputs:")
    print("Invalid Name:", process_name(None))
    print("Empty Average:", calculate_average([]))
    print("Invalid Age:", process_age("hello"))
