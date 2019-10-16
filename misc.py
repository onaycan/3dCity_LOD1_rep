import math

def permutation_symbol(i,j,k):
    return (i-j)*(j-k)*(k-i)/2

def cross_product(v1,v2):
    normal=[0.0,0.0,0.0]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                normal[i]+=permutation_symbol(i,j,k)*v1[j]*v2[k]
    return normal

def dot_product(v1, v2):
    return math.sqrt(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])