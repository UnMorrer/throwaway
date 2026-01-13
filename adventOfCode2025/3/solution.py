from pathlib import Path

input_data_path = Path(".") / "adventOfCode2025"/ "3" / "input.txt"


def read_input(input_data_path: Path) -> list[list[int]]:
    """
    Read input text file into a list of lists
    Each sublist contains individual joltages of all batteries
    
    :param path: Input path
    :type path: Path
    :return: List, with sublists containing individual battery joltages
    :rtype: list[list[int]]
    """
    with open(input_data_path, "r+") as file:
        battery_lines = file.readlines()
    
    return [list(line.strip()) for line in battery_lines]


def calculate_max_joltage_simple(batteries: list[int]) -> int:
    """
    Calculate max joltage of line by finding 2 batteries with highest individual joltage
    
    :param batteries: List of batteries iwht individual joltage
    :type batteries: list[int]
    :return: The highest joltage possible to create/retrieve
    :rtype: int
    """
    # Algorithm rundown
    # Step 1: Find largest integer in the row of batteries
    index, value = max(enumerate(batteries), key=lambda x: x[1])

    # Step 2a: Look at largest number AFTER largest integer -> largest joltage -> DONE
    after_largest = batteries[index+1:]
    if len(after_largest) >= 1:
        aftervalue = max(after_largest)
        return int(f"{value}{aftervalue}")

    # Step 2b: If joltage after battery is empty, look at largest number to the left -> Largest joltage
    else:
        before_largest = batteries[:index]
        beforevalue = max(before_largest)
        return int(f"{beforevalue}{value}")


def find_highest_joltage_recursive(batteries: list[int], activations: int, joltage: int) -> str:
    """
    Find the maximum joltage from batteries possible by checking if battery with <joltage>j exists in the last <activations> digits
    
    :param batteries: List of batteries with individual joltages
    :type batteries: list[int]
    :param activations: Number of batteries to turn on (remaining)
    :type activations: int
    :param joltage: Target joltage to search
    :type joltage: int
    :return: Joltage produced by turning on all <activations> batteries. This string has length <activations>
    :rtype: str
    """
    # Check if we need to run this again
    if activations == 0:
        return ""

    # Check if there's a <joltage> battery at least <activations> digits from the end
    max_joltage = int(max(batteries))
    battery_count = len(batteries)
    try:
        index = batteries.index(str(joltage))
    except ValueError:
        index = -1
    num_batteries_remaining = battery_count - index - 1 # How many batteries to the right of current joltage
    batteries_remaining = batteries[index+1:]

    # No batteries with high enough joltage found -> reduce joltage
    if (max_joltage < joltage
    # Special case -> Selection would involve leaving too few batteries available to complete the rest of the task -> reduce joltage
    or num_batteries_remaining + 1 < activations
    # Special case: Joltage does not exist among batteries
    or index == -1):
        return find_highest_joltage_recursive(batteries, activations, joltage-1)

    # Special case - exactly as many digits to the right as we need -> take them all
    if num_batteries_remaining + 1 == activations:
        return f"{joltage}" + "".join(batteries_remaining)

    # Regular case - choose sufficient joltage battery and invoke function again on remaining batteries
    remainder_digits = find_highest_joltage_recursive(batteries_remaining, activations-1, 9)
    return f"{joltage}{remainder_digits}"


if __name__ == "__main__":
    battery_data = read_input(input_data_path)
    joltage_simple = 0
    joltage_complex = 0
    for line in battery_data:
        max_joltage = calculate_max_joltage_simple(line)
        max_joltage_complex = find_highest_joltage_recursive(line, 12, 9)
        joltage_simple += max_joltage
        joltage_complex += int(max_joltage_complex)
        #print(f"Max joltage: {max_joltage} in line {''.join(line)}")
        print(f"Max joltage: {max_joltage_complex} in line {''.join(line)}")
    
    print(f"Max joltage for task 1: {joltage_simple}")
    print(f"Max joltage for task 2: {joltage_complex}")
