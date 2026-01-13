from pathlib import Path

from pydantic import BaseModel

input_data_path = Path(".") / "adventOfCode2025"/ "4" / "input.txt"
paper_marker = "@"
access_threshold = 4


class StorageSpace(BaseModel):
    # Coordinates
    row: int
    col: int
    # Status
    item: str
    removable: bool


class Storage():
    def __init__(self, data: list[list[str]], access_threshold: int) -> None:
        self.access_threshold = access_threshold
        self.rows = len(data)
        self.cols = len(data[0])
        self.items = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(StorageSpace(
                    row=i,
                    col=j,
                    item=data[i][j],
                    removable=False
                ))
            self.items.append(row)
        
        self.check_all_removable()


    def check_all_removable(self) -> int:
        """
        Check if paper can be removed for ALL fields
        :return: Total number of spaces from where papers could be removed
        :rtype: int
        """
        total_removable = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.check_removable(i, j):
                    total_removable += 1
        
        return total_removable


    def check_removable(self, row: int, col: int) -> bool:
        """
        Check if paper can be removed from space in row index <row> and column index <col>
        Updates data for the space in-place
        
        :param row: Row index to check
        :type row: int
        :param col: Column index to check
        :type col: int
        :return: True if paper from space can be removed, false if not
        :rtype: bool
        """
        space = self.items[row][col]
        if space.item != "@":
            return False

        neighbours = self.get_neighbours(space)
        total_paper = sum(1 for space in neighbours if space.item == paper_marker)
        if total_paper < self.access_threshold:
            self.items[row][col].removable = True
            return True
        return False


    def remove_all(self) -> int:
        """
        Remove paper from ALL tiles where removability criteria is met
        
        :return: Number of tiles from which paper was removed
        :rtype: int
        """
        total_removed = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.items[i][j].removable:
                    self.items[i][j].item = "x"
                    total_removed += 1
        return total_removed


    def get_neighbours(self, space: StorageSpace) -> list[StorageSpace]:
        """
        Return neighbours for item at space - accounting for boundaries of the storage space
        
        :param space: Storage space item
        :type space: StorageSpace
        :return: List of storage spaces and their contents in the order: top_l, top, top_r, r, l, bot_l, bot, bot_r
        :rtype: list[StorageSpace]
        """
        i = space.row
        j = space.col
        top_l = None
        top = None
        top_r = None
        l = None
        r = None
        bot_l = None
        bot = None
        bot_r = None

        if i == 0:
            top_l = StorageSpace(row=i-1, col=j-1, item=".", removable=False)
            top = StorageSpace(row=i-1, col=j, item=".", removable=False)
            top_r = StorageSpace(row=i-1, col=j+1, item=".", removable=False)
        elif i == self.rows - 1:
            bot_l = StorageSpace(row=i+1, col=j-1, item=".", removable=False)
            bot = StorageSpace(row=i+1, col=j, item=".", removable=False)
            bot_r = StorageSpace(row=i+1, col=j+1, item=".", removable=False)
        
        if j == 0:
            top_l = StorageSpace(row=i-1, col=j-1, item=".", removable=False)
            l = StorageSpace(row=i, col=j-1, item=".", removable=False)
            bot_l = StorageSpace(row=i+1, col=j-1, item=".", removable=False)
        elif j == self.cols - 1:
            top_r = StorageSpace(row=i-1, col=j+1, item=".", removable=False)
            r = StorageSpace(row=i, col=j+1, item=".", removable=False)
            bot_r = StorageSpace(row=i+1, col=j+1, item=".", removable=False)
        
        top_l = self.items[i-1][j-1] if top_l is None else top_l
        top = self.items[i-1][j] if top is None else top
        top_r = self.items[i-1][j+1] if top_r is None else top_r
        l = self.items[i][j-1] if l is None else l
        r = self.items[i][j+1] if r is None else r
        bot_l = self.items[i+1][j-1] if bot_l is None else bot_l
        bot = self.items[i+1][j] if bot is None else bot
        bot_r = self.items[i+1][j+1] if bot_r is None else bot_r

        return [top_l, top, top_r, l, r, bot_l, bot, bot_r]


    def print_board(self) -> None:
        """
        Print board state fro debug purposes
        """
        for row_i in self.items:
            print("".join([space.item for space in row_i]))


def read_data(path: Path) -> list[list[str]]:
    """
    Read input data into a list of strings, representing each position
    
    :param path: Input file path
    :type path: Path
    :return: List of lists, inner list has a string in each position
    :rtype: list[list[str]]
    """

    with open(input_data_path, "r+") as file:
        storage_lines = file.readlines()
    
    return [list(line.strip()) for line in storage_lines]


if __name__ == "__main__":
    data = read_data(input_data_path)
    num_rows = len(data)
    num_cols = len(data[0])
    paper_char = "@"

    storage = Storage(data, access_threshold)
    removable = storage.check_all_removable()
    iteration = 0
    total_removed = 0

    while removable > 0:
        removed = storage.remove_all()
        # storage.print_board()
        print(f"Iteration: {iteration} | Removed paper: {removed}")
        total_removed += removed
        removable = storage.check_all_removable()
        iteration += 1

    print(f"Removed total paper: {total_removed} in {iteration} steps")
