#operate with processes instead of threads. spawn new processes. Different from threads because no shared memory; have own process ID, everything else. 
#each process can have threads within it 

import multiprocessing 
import random
import math 
import argparse 
import time

class counter(object):
    def __init__(self): 
        self.all_darts = 0
        self.lock = multiprocessing.Lock() 
    def increment(self):
        self.lock.acquire()
        #try: #very few downsides to using try environments, lots of upsides 
         #   self.value += 1
        
        #finally:
        self.lock.release() 
    def __str__(self):
        return str(self.all_darts)



def worker2(store, n):
    total = 0
    for i in range(n):
        x_coord = random.uniform(-1,1) 
        y_coord = random.uniform(-1,1)
        if ((x_coord**2)*1.0 + (y_coord**2)**0.500) <= 1:
            total += 1
    #print (total)
    #print ((math.pi) - (((total*1.0)/(n*1.0))*4))
    store.put(total)

#------------------------------------------------------------------

def main():
    t0 = time.clock()

    y = counter()
    queue = multiprocessing.Queue()
    multi = []

    parser = argparse.ArgumentParser()
    parser.add_argument("t", help="number of threads", type=int)
    parser.add_argument("d", help="number of darts", type=int)
    args = parser.parse_args()
    num_darts = args.d
    num_threads = args.t

    #num_darts = 100 #number of darts
    num_threads = 50

    for i in range(num_threads): 
        job = multiprocessing.Process(target = worker2, args=(queue, num_darts))
        multi.append(job)
        job.start()

    for i in multi:
        i.join() #still 0 

   #print (y)
    newtotal = 0
    while not queue.empty():
        newtotal += queue.get()
    print ("New total is: ", newtotal)
    print ((newtotal/num_darts)*4)
    print ((math.pi) - (((newtotal*1.0)/(num_darts*1.0))*4))

    print ('This program took ', time.clock()-t0, ' seconds to complete')
    print("End of program")



if __name__ == '__main__':
    main()

#make a unit box 2x2, there is a circle inside of it. throw a series of darts that land on the board with x,y coords (-1 to 1), and calculate how many of those darts land within the circle vs the rest of the square. 