"""
Author: Melody Tribble

Created On: Nov 21, 2017
"""
import threading
from time import sleep

# configuration parameters
time = 0


class Buffer:
    # @param number is the job identifier
    # @param buffer is the job buffer
    # @param priority is the job's priority
    def __init__(self, values):
        self.values_l = values

    # called when printing the object
    def __str__(self):
        values = ''
        for value in self.values_l:
            values += str(value)
        return values


class Job:
    def __init__(self, number, buffer, priority, arrival_time, run_time):
        self.number = number
        self.buffer = buffer
        self.priority = priority
        self.arrival_time = arrival_time
        self.run_time = run_time
        self.stop = False  # for thread termination

    # called when printing the object
    def __str__(self):
        return 'T_%s%sT_%s' % (self.number, self.buffer, self.number)

    def run(self):
        print(threading.currentThread().getName() + ': Starting')
        while True:
            # run the job here!!!
            # terminate
            if self.stop:
                print(threading.currentThread().getName() + ': Ending')
                return

if __name__ == '__main__':

    object_L = []  # keeps track of objects, so we can kill their threads

    buffer_1 = Buffer([0, 0, 0])
    buffer_2 = Buffer([])

    job_1 = Job(1, buffer_1, 3, 1, 3)
    object_L.append(job_1)

    job_2 = Job(2, buffer_2, 2, 3, 10)
    object_L.append(job_2)

    job_3 = Job(3, buffer_1, 1, 6, 3)
    object_L.append(job_3)

    # start all the objects
    thread_L = []
    for obj in object_L:
        thread_L.append(threading.Thread(name=obj.__str__(), target=obj.run))

    for t in thread_L:
        t.start()

    sleep(2)

    # join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()

    print("All simulation threads joined")

