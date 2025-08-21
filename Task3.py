def maximalRectangle(matrix):
    if not matrix:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    max_area = 0

    # Check every possible rectangle
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == "1":
                # Try expanding rectangle from (i,j)
                min_width = cols
                for k in range(i, rows):
                    if matrix[k][j] == "0":
                        break
                    # find width of 1's in this row
                    width = 0
                    while j + width < cols and matrix[k][j + width] == "1":
                        width += 1
                    min_width = min(min_width, width)
                    # height = (k - i + 1)
                    area = min_width * (k - i + 1)
                    max_area = max(max_area, area)
    
    return max_area


# --- User Input Section ---
if __name__ == "__main__":
    print("Enter number of rows and columns (space-separated):")
    r, c = map(int, input().split())
    print(f"Enter the {r}x{c} binary matrix (each row as {c} space-separated 0/1):")
    matrix = []
    for _ in range(r):
        row = input().split()
        matrix.append(row)

    print("Maximum rectangle area of 1s is:", maximalRectangle(matrix))
