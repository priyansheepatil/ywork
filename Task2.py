def min_candies(ratings):
    n = len(ratings)
    candies = [1] * n
    
    # Left to Right
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            candies[i] = candies[i-1] + 1
    
    # Right to Left
    for i in range(n-2, -1, -1):
        if ratings[i] > ratings[i+1]:
            candies[i] = max(candies[i], candies[i+1] + 1)
    
    return sum(candies)


def main():
    print("Candies Distribution Problem")
    print("Enter ratings separated by spaces (e.g., 1 0 2):")
    ratings = list(map(int, input().strip().split()))
    
    result = min_candies(ratings)
    print("Minimum candies required:", result)


if __name__ == "__main__":
    main()
