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
def customergen(env, winOrder, linePay, winPay, linePick, winPick):
    print("starting gen")
    number = 0
    while(True):
        #select pump, line, and wait for a new customer
        t = random.expovariate(1.0/0.722)
        #print(pump,line,t)
        yield env.timeout(t)
        #make and run a new customer
        c = customer(env, number, winOrder, linePay, winPay, linePick, winPick)
        env.process(c)
        number = number+1

#process to run customers through customerwash
def customer(env, number, winOrder, linePay, winPay, linePick, winPick):
    print("%d arrives at drive-thru at %d" % (number, env.now))
    #order time
    t = random.lognormvariate(-1.367,0.684)
    yield env.timeout(t)
    #pay time
    t = random.lognormvariate(0.830,1.010)
    yield env.timeout(t)
    #pickup time
    t = random.expovariate(1.0/-0.827)
    yield env.timeout(t)




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


#setup the process
env.process(customergen(env, orderWindow, payLine, payWindow, pickupLine, pickupWindow))

#run the sim for 1020 time units
env.run(until = 1020)
