import numpy as np

#create a dataset(stimulate customer data)
np.random.seed(0)#Makes your random numbers reproducible
ages = np.random.randint(18, 70, size=20)#creates an array btw (start, stop and size)
spending = np.random.randint(100, 1000, size=20)#creates an array btw (start, stop and size)
rating = np.random.rand(20) * 5#Creates array of floats between 0 and 1
print("Ages:", ages)
print("Spending:", spending)
print("Rating:", rating)

#Combine into a Matrix(Stack into a 2D array (Matrix of 3 rows × 20 columns))
data = np.array([ages, spending, rating])
print(data.shape)

#Transpose to get 20 rows × 3 columns
data = data.T
print(data.shape)

#Indexing and Slicing
 #First 5 customer rows
print(data[:5])
 # Age of customer 10
print("age of 10th customer:", data[9][0])

#Reshape & Matrix Math
reshaped = data.T.reshape(6, 10)
print(reshaped)

#statistics
print("average mean of ages:", np.mean(data[:, 0]))
print("max spending:", np.max(data[:, 1]))
print("min spending:", np.min(data[:, 1]))
print("standard deviation in rating:", np.std(data[:, 2]))