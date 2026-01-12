from math import sqrt
from pathlib import Path
from typing import Union

input_data_path = Path(".") / "adventOfCode2025"/ "2" / "input.txt"


def read_input(input_data_path: Path) -> list[list[int]]:
    """
    Read input text file into a list of lists
    Each sublist contains all integers of the valid ID range
    
    :param path: Input path
    :type path: Path
    :return: List, with sublists containing valid IDs to use
    :rtype: list[list[int]]
    """
    with open(input_data_path, "r+") as file:
        contents = file.read()
    
    return_list = []
    id_ranges = contents.split(",")
    for id_range in id_ranges:
        limits = id_range.split("-")
        start = int(limits[0])
        end = int(limits[1])
        ids = [i for i in range(start, end+1)]
        return_list.append(ids)

    return return_list


def detect_invalid_twice(num: Union[int, str]) -> bool:
    """
    Detect invalid IDs, based on whether there is a twice-repeating pattern in the number
    
    :param num: Input number for detection
    :type num: Union[int, str]
    :return: True if invalid, False if valid
    :rtype: bool
    """
    numstr = str(num)
    length = len(numstr)

    # For odd-length numbers, this cannot happen so return true
    if length % 2 == 1:
        return False
    
    # For all other numbers, check if 1st part equals to 2nd part
    part1 = numstr[0: (length//2)]
    part2 = numstr[(length//2):]
    if part1 == part2:
        return True
    return False


def find_divisors(num: int) -> list[int]:
    """
    Find all integer divisors for a given number
    
    :param num: The number to find the divisors for
    :type num: Union[int, str]
    :return: The divisors of the number. Note: 1 is included in all cases
    :rtype: list[int]
    """
    divisors = []
    for i in range(1, int(sqrt(num)) + 1):
        if num % i == 0:       # If 'i' is a divisor of 'num'
            divisors.append(i) # Add 'i' to the list of divisors
            if i != num // i:
                divisors.append(num // i)
    return divisors


def detect_invalid_advanced(num: Union[int, str]) -> bool:
    """
    Detect invalid numbers. This means that a pattern repeats in the number **at least** twice.
    
    :param num: Input number for detection
    :type num: Union[int, str]
    :return: True if invalid, False if valid
    :rtype: bool
    """

    # Maximum, there can be n patterns, where n is the length of the number
    # We can check for i=1,2 ... n if a pattern is repeating
    # A pattern can only exist if the number is evenly divisible by n -> It is enough to check divisors
    n = int(num)
    numstr = str(num)
    length = len(numstr)
    divisors = find_divisors(length)[1:] # 1 is always 1st divisor which we don't care about
    for d in divisors:
        step = length // d # How many characters in repeating pattern
        pattern = numstr[0: step]
        for i in range(0, length, step):
            part = numstr[i: i+step]
            if part != pattern:
                break
            elif i == (length - step):
                print(f"Number {n} has {d} patterns repeating of length {step}")
                return True
    
    return False


if __name__ == "__main__":
    find_divisors(2)
    find_divisors(3)
    find_divisors(6)

    sum_ids_simple = 0
    sum_ids_complex = 0
    input = read_input(input_data_path)
    for id_range in input:
        for id in id_range:
            if detect_invalid_twice(id):
                # print(f"Invalid ID (simple): {id}")
                sum_ids_simple += id
                sum_ids_complex += id
            
            elif detect_invalid_advanced(id):
                print(f"Invalid ID (complex): {id}")
                sum_ids_complex += id
    
    print(f"Sum of invalid IDs for 1st task: {sum_ids_simple}")
    print(f"Sum of invalid IDs for 2nd task: {sum_ids_complex}")
