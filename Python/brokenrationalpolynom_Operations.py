#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Polynoms f(x),g(x) ∈ Q[x]
f(x) = -1/3x2 + 2 ------> f = [(2, 1), (0, 1), (-1, 3)]

Operations[dx, +, -, *, /, ggt] on Polynoms  ∈ Q[x]
"""

"""
Example inputs:

[(-7, 1), (1, 3), (12, 1)], [(-3, 1), (2, 1)]
[(0, 1), (6, 1), (2, 1), (2, 1), (1, 1)], [(3, 1), (1, 1)]
[(0, 1), (-10, 1), (-3, 1), (-9, 1), (2, 1)], [(0, 1), (-4, 1), (8, 1), (9, 1), (8, 1), (-5, 3), (2, 4)]
[(1, 1), (1, 1), (0, 1), (1, 1), (1, 1)], [(-1, 1), (0, 1), (1, 1), (2, 1), (-1, 1)]
[(4, 7), (0, 1), (5, 5), (-9, 6), (2, 3)], [(6, 5), (-7, 2), (-8, 1)]
"""

import sys

def add(m,n):

    a=[m[0],m[1]]
    b=[n[0],n[1]]
    
    if a[1]!=b[1]:
        a[0]*=b[1]
        b[0]*=a[1]
        a[1]=b[1]=a[1]*b[1]

    res = a[0]+b[0],a[1]
    return reduce(res)
    
def sub(m,n):
    a=[m[0],m[1]]
    b=[n[0],n[1]]
    
    if a[1]!=b[1]:
        a[0]*=b[1]
        b[0]*=a[1]
        a[1]=b[1]=a[1]*b[1]

    res = a[0]-b[0],a[1]
    return reduce(res)

def mul(m,n):
    res=(m[0]*n[0],m[1]*n[1])
    return reduce(res)
    
def div(m,n):
    res=(m[0]*n[1],m[1]*n[0])
    return reduce(res)
    
def reduce(m):
    def ggT(a,b):
        if a%b==0:
            return round(b)
        return ggT(b,a%b)
    
    a,b=m[0],m[1]
    ggt=ggT(a,b)
    a//=ggt
    b//=ggt
    res=(int(a),int(b))
    
    return res

def pol_dif(f):
    dif=[]
    for i in range(1,len(f)):
        li = f[i][0]*i, f[i][1]
        dif.append(reduce(li))
    return dif

def pol_add(f,g):
    #adds shorter Polynom to the longer one
    li=[]
    
    if len(f)<len(g):
        f,g=g,f
        
    for i in range(len(g)):
        li.append(add(f[i],g[i])) 
    for i in range(len(f)-(len(f)-len(g)),len(f)):
        li.append(reduce(f[i]))
    while li[len(li)-1]==(0,1):
                #removes unneeded (0,1) from list end 
                li.pop()
    return li

def pol_sub(f,g):
    
    li=[]

    if len(f)>=len(g):    
        for i in range(len(g)):
            li.append(sub(f[i],g[i]))
        #Appends rest of f without add partner to the end of the list    
        for i in range(len(f)-(len(f)-len(g)),len(f)):
            li.append(add((0,1),f[i]))
            
    else:
        for i in range(len(f)):
            li.append(sub(f[i],g[i]))
        #Rest of g without sub partner is subtracted from 0 and appended to the end of the list
        for i in range(len(g)-(len(g)-len(f)),len(g)):
            li.append(sub((0,1),g[i]))

    return li

def pol_mul(f,g):
    li=[[0,1]]*(len(f)+len(g)-1)

    for i in range(len(f)):
        for j in range(len(g)):
            subli=mul(f[i],g[j])
            li[i+j]=add(li[i+j],subli)
    return li

def pol_div(f,g):
    #calculates result length
    erg=[[0,1]]*(len(f)-len(g)+1)
    
    if len(f)>=len(g):
        for i in range(len(erg)):
            #max dividend degree / max divisor degree
            erg[len(erg)-1-i]=(div(f[len(f)-1-i],g[len(g)-1]))
            s=[]
            #s <- subtrahend = g*(max dividend degree / max divisor degree)
            s=pol_mul(g,erg[:len(erg)-i])
            #f with a degree reduced by 1: f = f-s
            f=pol_sub(f,s)
            
            re=[i for i in f]
           
            if len(re)==re.count((0,1)):
                re=[]
                break
            while re[len(re)-1]==(0,1):
                #removes unneeded (0,1) from the rests end 
                re.pop()
    #if degree of divisors > dividend --> can not divide
    else:
        re=f
    return erg,re

def pol_ggT(f,g):
    res=pol_div(f,g)
    
    if res[1]==[]:
        return g
    return pol_ggT(g,res[1])