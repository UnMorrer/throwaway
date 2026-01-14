from pathlib import Path

input_data_path = Path(".") / "adventOfCode2025"/ "5" / "input.txt"

def data_loader(path: Path) -> tuple[list[tuple[int]], list[int]]:
    """
    Data loader function for the inventory management system
    
    :param path: Input file path
    :type path: Path
    :return: A tuple of list<fresh ID tuple (start, end)> and list<available ingredient IDs>
    :rtype: tuple[list[tuple[int]], list[int]]
    """
    fresh_ids = []

    with open(path, "r") as file:
        input = file.read()
    
    sections = input.strip().split("\n\n")
    ranges = sections[0]
    ids = sections[1]

    for line in ranges.split("\n"):
        start, end = map(int, line.split("-"))
        fresh_ids.append((start, end))

    available_ids = [int(line) for line in ids.split('\n')]
    
    return fresh_ids, available_ids


def count_fresh_simple(fresh_ids: list[tuple[int]], available_ids: list[int]) -> int:
    """
    Use fresh ID range and available IDs to count how many fresh articles are available
    
    :param fresh_ids: List of (start, end) fresh ID ranges
    :type fresh_ids: list[tuple[int]]
    :param available_ids: List of available IDs
    :type available_ids: list[int]
    :return: Number of available items that are also fresh
    :rtype: int
    """
    counter = 0
    for id in available_ids:
        for start, end in fresh_ids:
            if start <= id and id <= end:
                counter += 1
                break

    return counter


def count_number_fresh(fresh_ids: list[tuple[int]]) -> int:
    """
    Count number of ingredients that are fresh
    
    :param fresh_ids: Fresh ID range input: (start, end)
    :type fresh_ids: list[tuple[int]]
    :return: Number of articles that are fresh
    :rtype: int
    """
    max_fresh = 0
    total_fresh = 0
    sorted_fresh_ids = sorted(fresh_ids, key=lambda x: x[0])

    for start, end in sorted_fresh_ids:
        if end > max_fresh:
            total_fresh += max(end - max(start, max_fresh) + 1, 0)
            if start <= max_fresh:
                total_fresh -= 1
            max_fresh = max(max_fresh, end)
    
    return total_fresh


if __name__ == "__main__":
    fresh_ids, available_ids = data_loader(input_data_path)
    available_fresh = count_fresh_simple(fresh_ids, available_ids)
    total_fresh = count_number_fresh(fresh_ids)
    print(f"Available number of fresh items: {available_fresh}")
    print(f"Number of fresh inventory entries: {total_fresh}")
