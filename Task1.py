def print_board(board):
    """Print Sudoku board simply"""
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))


def find_empty(board):
    """Find next empty cell (0 means empty)"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None


def is_valid(board, num, pos):
    """Check if num can be placed at pos (row, col)"""
    row, col = pos

    # Row check
    if num in board[row]:
        return False

    # Column check
    for i in range(9):
        if board[i][col] == num:
            return False

    # 3x3 box check
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False

    return True


def solve(board):
    """Backtracking algorithm"""
    empty = find_empty(board)
    if not empty:
        return True  # Solved

    row, col = empty
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num  # Place number

            if solve(board):  # Continue solving
                return True

            board[row][col] = 0  # Reset if wrong

    return False


def get_user_input():
    """Take Sudoku puzzle input from user"""
    print("Enter Sudoku row by row (use 0 for empty cells):")
    board = []
    for i in range(9):
        while True:
            try:
                row = list(map(int, input(f"Row {i+1}: ").split()))
                if len(row) != 9:
                    print(" Please enter exactly 9 numbers.")
                    continue
                board.append(row)
                break
            except ValueError:
                print("Enter only numbers.")
    return board


# Main program
if __name__ == "__main__":
    board = get_user_input()

    print("\nOriginal Puzzle:")
    print_board(board)

    if solve(board):
        print("\nSolved Puzzle:")
        print_board(board)
    else:
        print("No solution exists.")

