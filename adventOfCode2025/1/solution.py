from pathlib import Path

# settings
input_data_path = Path(".") / "adventOfCode2025"/ "1" / "input.txt"
dial_steps = 100
pos = 50 # Starting position
counter = 0

# code implementation
def translate_command(command: str) -> int:
    """
    Docstring for translate_command
    
    :param command: Command input from the data file
    :type command: str
    :return: Translated input to be actioned on the position tracker
    :rtype: int
    """

    if command[0].lower() == "l":
        return -1 * int(command[1:-1]) 
    elif command[0].lower() == "r":
        return int(command[1:-1])
    else:
        raise ValueError(f"Unknown command word: {command[0]}")

with open(input_data_path, "r+") as f:
    input_data_lines = f.readlines()

for line in input_data_lines:
    delta = translate_command(line)
    new_pos = pos + delta
    print(f"Position is: {pos}")
    print(f"Command is: {line[:-1]}")
    print(f"Counter is: {counter}")

    # Count how many times we land on 0 during this rotation
    times_at_zero = 0

    if delta > 0:
        # Moving right: count how many multiples of dial_steps we pass
        times_at_zero = (pos + delta) // dial_steps
    elif delta < 0:
        # Moving left: need to account for starting position
        abs_delta = abs(delta)
        if pos == 0:
            # Starting at 0, moving left: count complete wraps
            times_at_zero = abs_delta // dial_steps
        elif abs_delta >= pos:
            # We'll pass through 0: once when we first reach it,
            # then once per 100 clicks after that
            times_at_zero = 1 + (abs_delta - pos) // dial_steps
        # else: abs_delta < pos, so we don't reach 0 at all

    counter += times_at_zero
    pos = new_pos % dial_steps

print(f"Password is: {counter}")