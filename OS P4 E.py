import numpy as np

# Create an array
arr = np.array([15, 45, 22, 78, 56, 90, 34, 90])

print("Original Array:", arr)

# Find the maximum value
max_value = np.max(arr)

# Filter array to return only the maximum value(s)
filter_arr = arr[arr == max_value]

print("Maximum Value:", max_value)
print("Filtered Array:", filter_arr)
print("S120 ABHAY YADAV")
