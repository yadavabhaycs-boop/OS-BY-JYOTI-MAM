import numpy as np

# Create a single array
arr = np.array([10, 20, 30, 40, 50])

# Display the array
print("Original Array:", arr)

# Access elements
print("First Element:", arr[0])
print("Last Element:", arr[-1])

# Update an element
arr[2] = 35
print("After Updating:", arr)

# Basic operations
print("Addition (+10):", arr + 10)
print("Multiplication (*2):", arr * 2)

# Array statistics
print("Sum:", np.sum(arr))
print("Maximum:", np.max(arr))
print("Minimum:", np.min(arr))
print("Mean:", np.mean(arr))

# Size and Shape
print("Size:", arr.size)
print("Shape:", arr.shape)

print("S120 ABHAY YADAV")
