import math
from pathlib import Path

input_data_path = Path(".") / "adventOfCode2025"/ "6" / "input.txt"


def read_input(path: Path) -> list[list[str]]:
    """
    Read cephalopod math homework
    
    :param path: Input data path
    :type path: Path
    :return: Cephalopod math homework data structure
    :rtype: list[list[str]]
    """
    sheet_data = []
    with open(path, "r") as file:
        for line in file.readlines():
            sheet_data.append(line.split())
    
    return sheet_data


def read_input_complex(path: Path) -> list[list[str]]:
    """
    Read cephalopod math input - taking whitespaces into account
    
    :param path: Input file path
    :type path: Path
    :return: List of columns from the raw table NOTE: This data has already been pivoted here
    :rtype: list[list[str]]
    """
    with open(path, "r") as file:
        raw_data = file.read()
    lines = raw_data.split("\n")
    n_rows = len(lines)
    n_cols = len(lines[-1].split())
    out_data = []

    # We need to know the MAX width of the numbers in all rows -> that enables us to know "where" the digits are located & offset
    current_index = 0
    for j in range(n_cols):
        column_data = []
        # Start with operands column -> Tells us column width in characters
        operators_line = lines[-1][current_index:]
        stripped = operators_line[1:].lstrip(" ")
        width = (len(operators_line) - len(stripped) - 1) if stripped else len(operators_line)

        for i in range(n_rows-1):
            current_line = lines[i][current_index:]
            data = current_line[:width]
            column_data.append(data)
        column_data.append(operators_line[0])
        out_data.append(column_data)
        current_index += width + 1
    
    return out_data


def calculate_math(sheet_column: list[str]) -> int:
    """
    Calculate individual row of cephalopod math equation
    
    :param sheet_column: 1 column from the Cephalopod math data sheet. NOTE: The final element must be an operation marker
    :type sheet_column: list[str]
    :return: The result of the equation
    :rtype: int
    """
    operation = sheet_column[-1]
    sheet_data = sheet_column[:-1]
    if operation == "+":
        return sum([int(x) for x in sheet_data])
    elif operation == "*":
        return math.prod([int(x) for x in sheet_data])


def calculate_complex_math(sheet_column: list[str]) -> int:
    """
    Calculate column result using more complex maths
    
    :param sheet_column: Input column - NOTE: This is a list of strings as the order does matter
    :type sheet_column: list[str]
    :return: The result of the operation, described in the last element of the column
    :rtype: int
    """
    operation = sheet_column[-1]
    digits = len(sheet_column[0])
    n_numbers = len(sheet_column) - 1

    numbers = []
    for j in range(digits):
        number = ""
        for i in range(n_numbers):
            number += sheet_column[i][j]
        numbers.append(int(number.replace(" ", "")))
    
    numbers.append(operation)
    return calculate_math(numbers)


def pivot(sheet_data: list[list[str]]) -> list[list[str]]:
    """
    Pivot sheet data to be by the column instead of by the rows
    
    :param sheet_data: Sheet data - by the rows
    :type sheet_data: list[list[str]]
    :return: Sheet data, where each inner list represents 1 column from the dataset
    :rtype: list[list[str]]
    """
    n_rows = len(sheet_data)
    n_cols = len(sheet_data[0])

    pivot_table = []
    for j in range(n_cols):
        col_data = []
        for i in range(n_rows):
            col_data.append(sheet_data[i][j])
        pivot_table.append(col_data)
    
    return pivot_table

if __name__ == "__main__":
    data = read_input(input_data_path)
    pivot_data = pivot(data)
    col_sums = map(calculate_math, pivot_data)
    total = sum(col_sums)
    print(f"Total math homework sum: {total}")
    complex_data = read_input_complex(input_data_path)
    col_sums = map(calculate_complex_math, complex_data)
    total_complex = sum(col_sums)
    print(f"Total math homework sum in complex case: {total_complex}")
