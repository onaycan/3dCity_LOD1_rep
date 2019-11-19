# python3 program to evaluate 
# area of a polygon using 
# shoelace formula 
  
# (X[i], Y[i]) are coordinates of i'th point. 
def polygonArea(X, Y, n): 
  
    # Initialze area 
    area = 0.0
  
    # Calculate value of shoelace formula 
    j = n - 1
    for i in range(0,n): 
        area += (X[j] + X[i]) * (Y[j] - Y[i]) 
        j = i   # j is previous vertex to i 
      
  
    # Return absolute value 
    return int(abs(area / 2.0)) 
  
# Driver program to test above function 
X = [0, 2, 4] 
Y = [1, 3, 7] 
n = len(X) 
print(polygonArea(X, Y, n)) 
  
# This code is contributed by 
# Smitha Dinesh Semwal 