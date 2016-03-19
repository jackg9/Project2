# Author: John Gordon
# Email: gordon8@umbc.edu
# File: LocalSearch.py
# Description: This program performs the hill climbing algorithm, hill climbing with random
# restarts, and simulated annealing by the three following functions respectively: 
# 
# hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax)
# hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin,
# ymax)
# simulated_annealing(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax)
# Note: the function_to_optimize is 2 dimensions that takes two arguments and returns a 
# float

import sys
import matplotlib.pyplot as plt
import numpy as np
import time
import code
import random

''' This function minimizes the passed in 2D funtion (func) and checks to see if the
    returned value is better than the current position; making sure it stays within the
    defined bounds from the passed in xmin/xmax and ymin/ymax. 
    If the returned value is better, reset step size, save value (for comparison later) and 
    repeat. 
    Else, the returned value is not better, adjust an element in func and minimize again. Do
    this until all possible adjustments have been made for the current position. If no
    better value is returned from all possible adjustments, decrease step and repeat.
    If step size reaches zero, move to different spot. -> rand spot if hill_climb with
    rand restarts '''
def hill_climb(func, step_size, xmin, xmax, ymin, ymax):

    x = 0 
    y = 0
    best = sys.maxsize
    resluts = [best,x,y,step_size]    # Results returned by check_neighbor()

    # Climb until it reaches a bound or no other neighbors can be found        
    # Increment and decrement x and y in function by the step size until step size
    # reaches 0 (basically 0) or no more neighbors to check
    while step_size > 0.0001:

        results = check_neighbors(func,step_size,xmin,xmax,ymin,ymax,x,y)
        best = results[0]
        x = results[1]
        y = results[2]
        step_size = results[3]

        # Plot hill climb over function.
        plt.plot(x,func(x,y), 'bo')
        #plt.pause(0.0001)
    

    print("Hill Climb found minimal value: ", best, " at:(",x,',',y,')')

''' Hill Climb with random restarts:
    Same as normal hill climb except when step size reaches basically 0, pick a random
    position to start hill climbing again. The parameter 'num_restarts' sets the number
    of restarts performed.
'''
def hill_climb_random_restart(func, step_size, num_restarts, xmin, xmax, 
                              ymin, ymax):

    x = 0 
    y = 0
    best = sys.maxsize
    resluts = [best,x,y,step_size]    # Results returned by check_neighbor()
    restarts = 0

    # Climb until it reaches a bound or no other neighbors can be found        
    # Increment and decrement x and y in function by the step size until step size
    # reaches 0 (basically 0) or no more neighbors to check
    while restarts <= num_restarts:

        results = check_neighbors(func,step_size,xmin,xmax,ymin,ymax,x,y)
        best = results[0]
        x = results[1]
        y = results[2]
        step_size = results[3]

        # If step_size is about to be 0, randomly restart and keep checking
        if step_size <= 0.0001:
            step_size = 0.5
            x = random.uniform(xmin,xmax)
            y = random.uniform(ymin,ymax)
            print("Randomly restarting hill climb... start at: ",x,",",y)
            restarts += 1

        # Plot hill climb over function.
        plt.plot(x,func(x,y), 'c^')
        
    print("Hill Climb with restarts found minimal value: ", best, " at:(",x,',',y,')')

''' This method checks each neighbor next to the current position, it compares all four
    neighbors (right, left, up, down) and chooses best one that is better than current 
    position. If no neighbor is better, decrement step_size and return.
    RETURN: list = [best_new_value, best_x, best_y, step_size]
'''
def check_neighbors(func, step_size, xmin, xmax, ymin, ymax, x, y):
    
    inc_x_val = sys.maxsize
    inc_y_val = sys.maxsize
    dec_x_val = sys.maxsize
    dec_y_val = sys.maxsize
    best_val = sys.maxsize
    inc_new_x = x
    dec_new_x = x
    inc_new_y = y
    dec_new_y = y
    current_val = func(x,y)
    # Can not iterate by float for loops, so make sure varaiables are ints with same
    # amount of times looping
    num = abs(xmax - x)
    x_max = int(num/step_size) + 1    # Add 1 incase int rounds down
    
    num = abs(xmin - x)
    x_min = int(num/step_size) + 1
    
    num = abs(ymax - y)
    y_max = int(num/step_size) + 1

    num = abs(ymin - y)
    y_min = int(num/step_size) + 1
    

    ### Check neighbors to the right ###
    for i in range(0, x_max, 1):
        # If beyond bounds, break out
        if inc_new_x > xmax:
            break
        # If neighbor value is better than current value, set new position (just new x)
        # and new value. Break out of for loop
        if func(inc_new_x,y) < current_val:
            inc_x_val = func(inc_new_x,y)
            break
        # Else, increment by step_size
        else:
            inc_new_x += step_size

    ### Check neighbors to the left ###
    for i in range(0, x_min, 1):
        # If beyond bounds, break out
        if dec_new_x < xmin:
            break
        # If neighbor value is better
        if func(dec_new_x,y) < current_val:
            dec_x_val = func(dec_new_x,y)
            break
        # Else, decrement by step_size
        else:
            dec_new_x -= step_size

    ### Check neighbors above ###
    for i in range(0, y_max, 1):
        # If beyond bounds, break out
        if inc_new_y > ymax:
            break
        # If neighbor value is better than current value
        if func(x,inc_new_y) < current_val:
            inc_y_val = func(x,inc_new_y)
            break
        # Else, increment by step_size
        else:
            inc_new_y += step_size

    ### Check neighbors below ###
    for i in range(0, y_min, 1):
        # If beyond bounds, break out
        if dec_new_y < ymin:
            break
        # If neighbor value is better
        if func(x,dec_new_y) < current_val:
            dec_y_val = func(x,dec_new_y)
            break
        # Else, decrement by step_size
        else:
            dec_new_y -= step_size

    # Compare all new found values to see which is best to return
    vals = [inc_x_val, inc_y_val, dec_x_val, dec_y_val]
    #code.interact(local=locals())
    best_val = min(vals)

    # If a neighbor value was better, find out which one to return new position too
    if best_val < current_val:
        # Set step size back to starting value after success
        step_size = 0.1
        # If a neighbor to the right was best option
        if inc_x_val == best_val:
            print("Neighbor to RIGHT.")
            return [inc_x_val, inc_new_x, y, step_size]
        # Else if neighbor to the left was best option
        elif dec_x_val == best_val:
            print("Neighbor to LEFT.")
            return [dec_x_val, dec_new_x, y, step_size]
        # Else if neighbor above was best
        elif inc_y_val == best_val:
            print("Neighbor ABOVE.")
            return [inc_y_val, x, inc_new_y, step_size]
        # Else if neighbor below was best
        elif dec_y_val == best_val:
            print("Neighbor BELOW.")
            return [dec_y_val, x, dec_new_y, step_size]
    
    # No neighbors were found to be better, lower step_size
    else:
        print("No better neighbor found, decrementing step size...")
        step_size -= 0.005
        return [current_val, x, y, step_size]


''' Simulated Annealing:

'''
def simulated_annealing(func, step_size, max_temp, xmin, xmax, ymin, ymax):

    temp = max_temp
    cooling_rate = 0.003
    x = 0
    y = 0
    best = sys.maxsize
    resluts = [best,x,y,step_size,temp]

    while temp > 1:
        results = sa_check_neighbors(func,step_size,xmin,xmax,ymin,ymax,x,y,temp,
                                     cooling_rate)
        best = results[0]
        x = results[1]
        y = results[2]
        step_size = results[3]
        temp = results[4]

        # Just make sure step size does not reach 0
        if step_size <= 0.0001:
            step_size = 0.1

        # Plot chosen neighbor
        plt.plot(x,func(x,y), 'mD')


    print("Simulated Annealing found minimal value: ", best, " at:(",x,',',y,')')

''' Checking neighbors for SA differs slightly from hill climb 
    RETURN: list = [best_new_value, best_x, best_y, step_size]
'''
def sa_check_neighbors(func,step_size,xmin,xmax,ymin,ymax,x,y,temp,cooling_rate):
    inc_x_val = sys.maxsize
    inc_y_val = sys.maxsize
    dec_x_val = sys.maxsize
    dec_y_val = sys.maxsize
    best_val = sys.maxsize
    best_x = x
    best_y = y
    inc_new_x = x
    dec_new_x = x
    inc_new_y = y
    dec_new_y = y
    current_val = func(x,y)
    prob = 0
    # Can not iterate by float for loops, so make sure varaiables are ints with same
    # amount of times looping
    num = abs(xmax - x)
    x_max = int(num/step_size) + 1    # Add 1 incase int rounds down
    
    num = abs(xmin - x)
    x_min = int(num/step_size) + 1
    
    num = abs(ymax - y)
    y_max = int(num/step_size) + 1

    num = abs(ymin - y)
    y_min = int(num/step_size) + 1
    

    ### Check neighbors to the right ###
    for i in range(0, x_max, 1):
        # If beyond bounds, break out
        if inc_new_x > xmax:
            break
        # If neighbor value is better than current value, set new position (just new x)
        # and new value. Break out of for loop
        if func(inc_new_x,y) < current_val:
            inc_x_val = func(inc_new_x,y)
            break
        # Else, increment by step_size
        else:
            inc_new_x += step_size

    ### Check neighbors to the left ###
    for i in range(0, x_min, 1):
        # If beyond bounds, break out
        if dec_new_x < xmin:
            break
        # If neighbor value is better
        if func(dec_new_x,y) < current_val:
            dec_x_val = func(dec_new_x,y)
            break
        # Else, decrement by step_size
        else:
            dec_new_x -= step_size

    ### Check neighbors above ###
    for i in range(0, y_max, 1):
        # If beyond bounds, break out
        if inc_new_y > ymax:
            break
        # If neighbor value is better than current value
        if func(x,inc_new_y) < current_val:
            inc_y_val = func(x,inc_new_y)
            break
        # Else, increment by step_size
        else:
            inc_new_y += step_size

    ### Check neighbors below ###
    for i in range(0, y_min, 1):
        # If beyond bounds, break out
        if dec_new_y < ymin:
            break
        # If neighbor value is better
        if func(x,dec_new_y) < current_val:
            dec_y_val = func(x,dec_new_y)
            break
        # Else, decrement by step_size
        else:
            dec_new_y -= step_size

    # Compare all new found values to see which is best to return
    vals = [inc_x_val, inc_y_val, dec_x_val, dec_y_val]
    #code.interact(local=locals())
    best_val = min(vals)

    # If a neighbor to the right was best option
    if inc_x_val == best_val:
        best_x = inc_new_x
    # Else if neighbor to the left was best option
    elif dec_x_val == best_val:
        best_x = dec_new_x
    # Else if neighbor above was best
    elif inc_y_val == best_val:
        best_y = inc_new_y
    # Else if neighbor below was best
    elif dec_y_val == best_val:
        best_y = dec_new_y

    # If a neighbor value was better, find out which one to return new position too
    if best_val < current_val:
        # Set step size back to starting value after success
        step_size = 0.1

        # Cool the temp on success
        temp *= 1-cooling_rate
        return [best_val, best_x, best_y, step_size, temp]

    # No neighbors were found to be better, lower step_size
    else:
        prob = np.exp((best_val - current_val)/temp)
        # If probablity is high enough, accept 'worse' neighbor
        #### GETTING STUCK HERE ####
        if prob > random.random():
            print("Accepting worse neighbor...")
            step_size = 0.1
            return [best_val, best_x, best_y, step_size, temp]

        print("No better neighbor found, decrementing step size...")
        step_size -= 0.005
        return [current_val, x, y, step_size]


''' Takes 2 arguments and returns a float '''
def function_to_optimize(x,y):

    r = np.sqrt(x**2 + y**2)
    return ((np.sin(x**2 + 3*(y**2))/(0.1 + r**2)) + (x**2 + (5*(y**2)))*
            (np.exp(1-(r**2))/2))

def main():
    
    func = function_to_optimize
    step_size = 0.1
    xmin = -2.5
    ymin = -2.5
    xmax = 2.5
    ymax = 2.5

    
    x_vals = np.arange(xmin,xmax,0.01)   # Values to plot xmin to xmax
    y_vals = np.arange(ymin,ymax,0.01)   # Values to plot ymin to ymax
    plt.figure(1)   # Create figure for hill climb
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Hill Climb')
    plt.plot(func(x_vals,y_vals), 'g-', linewidth=2)

    start = time.time()
    hill_climb(func, step_size, xmin, xmax, ymin, ymax)

    end = time.time()
    print("Elapsed Time for hill climb: ", end-start)
    plt.show()

    num_restarts = 5
    plt.figure(2)   # Figure for Hill climb with random restarts
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Hill Climb with Random Restarts')
    plt.plot(func(x_vals,y_vals), 'r-', linewidth=2)

    start = time.time()
    hill_climb_random_restart(func, step_size, num_restarts, xmin, xmax, ymin, ymax)
    end = time.time()
    print("Elapsed Time for hill climb with restarts: ", end-start)
    plt.show()

    max_temp = 1000
    plt.figure(3)   # Figure for Simmulated Annealing
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Simmulated Annealing')
    plt.plot(func(x_vals,y_vals), 'k-', linewidth=2)

    start = time.time()
    simulated_annealing(func, step_size, max_temp, xmin, xmax, ymin, ymax)
    end = time.time()
    print("Elapsed Time for Simmulated Annealing: ", end-start)
    plt.show()

if __name__ == "__main__":
    main()
