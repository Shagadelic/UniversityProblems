#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Given list of n points.
point = Tuple (xi, yi) ∈ R2, i ∈ {0, . . . , n − 1}
find best fitting line y = mx + b
"""

"""
Example inputs:
a = [(0 , -0.302287) ,  (1 ,0.48864), (2 ,2.56601), (3,4.42318),  (4,2.57443),
  (5, 4.38737), (6 ,5.71113), (7 ,7.58872) , (8 ,7.55638),  (9 ,9.48674)]
"""

def cost_function(a,m,b):
    cost=0
    for tupel in a:
        cost+=abs((m*tupel[0]+b)-tupel[1])   
    return cost

def regression(a, m, b,   c=0, op=None, mt=True, bt=True):
        
    if mt==False and bt==False:#cost cannot be reduced further
        return tuple(op[1:])#returns m and b tuple
        
    def cf(a,m,b):#cost function with, m and b in return statement
        cost=0
        for tupel in a:
            cost+=abs((m*tupel[0]+b)-tupel[1])   
        return cost,m,b
        
    if op==None:#start value
        op=cf(a,m,b)

    c=c%2#checks whether m or b gets changed
    
    if c==0:
        valm=cf(a,m-0.01,b)
        valp=cf(a,m+0.01,b)
        
        if valm[0] < valp[0] and valm[0] < op[0]:
            op=valm
            return regression(a, op[1], op[2], c+1 ,op, mt=True, bt=bt)
        
        elif valp[0] < valm[0] and valp[0] < op[0]:
            op=valp
            return regression(a, op[1], op[2], c+1 ,op, mt=True, bt=bt)
            
        else:#Change of m does not improve cost
            return regression(a, op[1], op[2], c+1 ,op, mt=False, bt=bt)
    elif c==1:
        valm=cf(a,m,b-0.01)
        valp=cf(a,m,b+0.01)
        
        if valm[0] < valp[0] and valm[0] < op[0]:
            op=valm
            return regression(a, op[1], op[2], c+1 ,op, mt, bt=True)
        
        elif valp[0] < valm[0] and valp[0] < op[0]:
            op=valp
            return regression(a, op[1], op[2], c+1 ,op, mt, bt=True)
            
        else:#Change of b does not improve cost
            return regression(a, op[1], op[2], c+1 ,op, mt, bt=False)
