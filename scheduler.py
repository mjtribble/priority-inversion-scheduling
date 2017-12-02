"""
Author: Melody Tribble

Created On: Nov 21, 2017
"""


# This class creates a buffer and it's functionality
import sys


class Buffer:

    # create a new buffer object
    def __init__(self, number, value):
        self.number = number
        self.value = value
        self.j_list = []

    # This is called when printing the object
    def __str__(self):
        return "Buffer %s <%s>" % (self.number, self.value)

    # This adds a job to the end of the buffer
    def add_job(self, j):
        self.j_list.append(j)


# This class creates and prints a job
class Job:

    # This creates and instantiates a new job
    def __init__(self, number, priority, arrival_time, run_time):
        self.number = number
        self.priority = priority
        self.arrival_time = arrival_time
        self.run_time = run_time
        self.completed_time = 0
        self.remaining_time = run_time

    # This is called when printing a job
    def __str__(self):

        # T_1 Job
        if self.number is 1:
            return 'T_%s111T_%s.' % (self.number, self.number)

        # T_2 Job
        elif self.number is 2:
            return 'T_%s%sT_%s.' % (self.number, 'N' * self.completed_time, self.number)

        # T_3 Job
        else:
            return 'T_%s%sT_%s.' % (self.number, '3' * self.completed_time, self.number)


# Start program here
if __name__ == '__main__':

    # file to write output to
    orig_stdout = sys.stdout
    f = open('tribble-3.output.txt', 'w')
    sys.stdout = f

    # Given list of jobs to run
    job_l = [(1, 3), (3, 2), (6, 3), (8, 1), (10, 2), (12, 3), (26, 1)]

    # sort job lists by arrival time, the first value in the tuple
    job_l = sorted(job_l, key=lambda tup: tup[0])

    # list to hold the being processed and run
    processes_l = []

    # Create Buffers
    buffer_1 = Buffer(1, '0')
    buffer_2 = Buffer(2, 'N')

    # Create Jobs and add them to the appropriate Buffer
    for i in job_l:

        t = i[1]
        arrival_t = i[0]

        if t is 1:
            job = Job(number=1, priority=3, arrival_time=arrival_t, run_time=3)
            buffer_1.add_job(job)

        if t is 2:
            job = Job(number=2, priority=2, arrival_time=arrival_t, run_time=10)
            buffer_2.add_job(job)

        if t is 3:
            job = Job(number=3, priority=1, arrival_time=arrival_t, run_time=3)
            buffer_1.add_job(job)

        print("Job created : ", i)

    # set buffer lists to a variable
    b1 = buffer_1.j_list
    b2 = buffer_2.j_list

    # starting time is zero
    time = 0

    # determines which job to run first based on which arrived first,
    # removes them from the buffer, sets the system time to their arrival time
    # adds them to the process list
    if b1[0].arrival_time <= b2[0].arrival_time:
        processes_l.append(b1[0])
        time = b1[0].arrival_time
        b1.remove(b1[0])
    else:
        processes_l.append(b2[0])
        time = b2[0].arrival_time
        b2.remove(b2[0])

    # runs while there are unfinished jobs.
    while processes_l:

        # sets current job to the beginning of the buffer
        current_job = processes_l[0]
        current_job.arrival_time = time
        finish_time = current_job.arrival_time + current_job.remaining_time
        preempt_job = None
        next_job = None

        # If current job is T2 and buffer 1 is not empty,
        #  check buffer 1 for a T1 that could preempt it.
        if current_job.number == 2 and b1:
            for i in b1:
                if i.number == 1 and i.arrival_time < finish_time:
                    preempt_job = i
                    b1.remove(i)
                    break
            if b1[0].number == 1 and b1[0].arrival_time == current_job.arrival_time:
                preempt_job = b1[0]
                b1.remove(b1[0])

        # If the current job is T3, and buffer 2 is not empty,
        #  check buffer 2 for a T2 that could preempt it.
        if current_job.number == 3 and b2:
            if b2[0].arrival_time < finish_time:
                preempt_job = b2[0]
                b2.remove(b2[0])

        # If there is a job that will interrupt the current job
        if preempt_job:

            # current job was NOT preempted before it was able to run.
            if preempt_job.arrival_time > current_job.arrival_time:

                # set the current jobs remaining time
                current_job.completed_time = preempt_job.arrival_time - current_job.arrival_time
                current_job.remaining_time -= current_job.completed_time

                # print the current job
                print('time %s, %s' % (time, current_job))


                time = preempt_job.arrival_time

            # add the next job to the font of the list.
            processes_l.insert(0, preempt_job)

        # If there is a job that will run
        else:  # the current job will finish without being preempted
            current_job.completed_time = finish_time - current_job.arrival_time
            current_job.remaining_time -= current_job.completed_time
            print('time %s, %s' % (time, current_job))
            time = finish_time
            processes_l.remove(current_job)

        # the process list is empty, choose next job to run
        if not processes_l:

            # if both buffers still have jobs to run choose the next job based on arrival time and priority.
            if b1 and b2:

                # choose buffer 1's job if it arrives first,
                #  or if there is a tie and buffer 1's job has a higher priority
                if b1[0].arrival_time < b2[0].arrival_time \
                        or (b1[0].arrival_time == b2[0].arrival_time and b1[0].priority > b2[0].priority):
                    processes_l.append(b1[0])
                    b1.remove(b1[0])

                # else choose the job in buffer 2
                else:
                    processes_l.append(b2[0])
                    b2.remove(b2[0])

                if processes_l[0].arrival_time > time:
                    time = processes_l[0].arrival_time

            # if only buffer 1 has jobs left to run
            elif b1:
                processes_l.append(b1[0])
                b1.remove(b1[0])
                if processes_l[0].arrival_time > time:
                    time = processes_l[0].arrival_time

            # if only buffer 2 has jobs left to run
            elif b2:
                processes_l.append(b2[0])
                b2.remove(b2[0])
                if processes_l[0].arrival_time > time:
                    time = processes_l[0].arrival_time

    sys.stdout = orig_stdout
    f.close()
