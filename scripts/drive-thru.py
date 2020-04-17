#!/usr/bin/python3
import random
import simpy
import numpy


###########################################
#Author: Alan Fleming
#Email: alanfleming1998@gmail.com
#Description: This is a script to simulate a McDonalds Drivethru 
#Asummuptions: The inter-arrival time is representable by a exponential distribution
#              The ordering line has an infinite queue
#              The ordering time is representable by a lognormal distribution
#              The Payment time is representable by a lognormal distribution
#              The Pickup time is representable by a exponential distribution
#              No cars will leave the line due to excessive wait times or length
###########################################


#process to make customers
def customergen(env, winOrder, linePay, winPay, linePick, winPick,
                arrivalTime, orderTime, payTime, PickupTime):
    print("starting gen")
    number = 0
    while(True):
        #select pump, line, and wait for a new customer
        t = random.expovariate(1.0/0.722)
        #handle negative arrival time
        if(t < 0):
            t = 0
        arrivalTime.put(t)

        yield env.timeout(t)
        #make and run a new customer
        c = customer(env, number, winOrder, linePay, winPay, linePick, winPick,
                    orderTime, payTime, PickupTime) 
        env.process(c)
        number = number+1

#process to run customers through customerwash
def customer(env, number, winOrder, linePay, winPay, linePick, winPick,
             orderTime, payTime, PickupTime):
    print("%d arrives at drive-thru at %d" % (number, env.now))
    #order time
    window = winOrder.request()
    yield window
    
    t = random.lognormvariate(-1.367,0.684)
    #handle negative required time
    if(t < 0):
        t = 0
    orderTime.put(t)
    yield env.timeout(t)

    #get a spot in line before you release the window
    line = linePay.request()
    yield line
    winOrder.release(window)

    #take a spot at the window and leave the line
    window = winPay.request()
    yield window
    linePay.release(line)

    #pay time
    t = random.lognormvariate(0.830,1.010)
    if(t < 0):
        t = 0
    payTime.put(t)
    
    yield env.timeout(t)

    #get a spot in line before you release the window
    line = linePick.request()
    yield line
    winPay.release(window)

    #take a spot at the window and leave the line
    window = winPick.request()
    yield window
    linePick.release(line)

    #pickup time
    t = random.expovariate(1.0/-0.827)
    if(t < 0):
        t = 0
    PickupTime.put(t)

    yield env.timeout(t)
    
    winPick.release(window)



#seed the random number
random.seed(2019)


##reminders for random numbers
#arival random number => random.expovariate(1.0/mean)
#pump random number => random.lognormvariate(scale,shape)

##settup and run the simpulation

#make the enviroment
env = simpy.Environment()

#setup the resources
orderWindow = simpy.Resource(env,capacity=1)
payLine = simpy.Resource(env,capacity=3)
payWindow = simpy.Resource(env,capacity=1)
pickupLine = simpy.Resource(env,capacity=1)
pickupWindow = simpy.Resource(env,capacity=1)

#setup stores for record keeping
arrivalTime = simpy.Store(env)
orderTime = simpy.Store(env)
payTime = simpy.Store(env)
PickupTime = simpy.Store(env)


#setup the process
env.process(customergen(env, orderWindow, payLine, payWindow, pickupLine, pickupWindow, arrivalTime, orderTime, payTime, PickupTime))

#run the sim for 1020 time units
env.run(until = 120)


print("averages: \narrival time: %3.5f , order time: %3.5f , pay time: %3.5f , pickup time: %3.5f" %
        (numpy.mean(arrivalTime.items) ,numpy.mean(orderTime.items) ,numpy.mean(payTime.items) ,numpy.mean(PickupTime.items)))
