"""
Author: Melody Tribble

Created On: Nov 21, 2017
"""


class Buffer:
    def __init__(self, number, value):
        self.number = number
        self.value = value
        self.j_list = []
        # self.stop = False  # for thread termination

    # called when printing the object
    def __str__(self):
        return "Buffer %s <%s>" % (self.number, self.value)

    def add_job(self, j):
        self.j_list.append(j)


class Job:
    def __init__(self, number, priority, arrival_time, run_time):
        self.number = number
        self.priority = priority
        self.arrival_time = arrival_time
        self.run_time = run_time
        self.remaining_time = self.run_time

    # called when printing the object
    def __str__(self):

        if self.number is 1:
            return 'T_%s111T_%s' % (self.number, self.number)

        elif self.number is 2:
            time_complete = self.run_time - self.remaining_time
            return 'T_%s%sT_%s' % (self.number, 'N' * time_complete, self.number)

        else:
            return 'T_%s333T_%s' % (self.number, self.number)


if __name__ == '__main__':

    # List of jobs to run
    job_l = [(1, 3), (3, 2), (6, 3), (8, 1), (10, 2), (12, 3), (26, 1)]
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

    b1 = buffer_1.j_list
    b2 = buffer_2.j_list

    time = 0
    if b1[0].arrival_time <= b2[0].arrival_time:
        processes_l.append(b1[0])
        time = b1[0].arrival_time
        b1.remove(b1[0])
    else:
        processes_l.append(b2[0])
        time = b2[0].arrival_time
        b2.remove(b2[0])

    while processes_l:
        current_job = processes_l[0]
        current_job.arrival_time = time
        finish_time = current_job.arrival_time + current_job.remaining_time
        next_job = None

        for i in b1:
            bool = ((i.arrival_time < finish_time) and (i.priority == 3 and current_job.priority != 3)) or (
                i.arrival_time == finish_time and current_job.priority != 3)
            if bool:
                next_job = i
                b1.remove(i)
                break

        for j in b2:
            if ((j.arrival_time < finish_time) and current_job.priority == 1) \
                    or (j.arrival_time == finish_time):
                next_job = j
                b2.remove(j)
                break

        if next_job:  # add next job to the font of the list.
            if next_job.arrival_time == finish_time:
                current_job.remaining_time = 0
                print('time %s, %s' % (time, current_job))
                processes_l.remove(current_job)
                time = finish_time

            elif next_job.arrival_time > current_job.arrival_time:
                current_job.remaining_time = current_job.remaining_time - (next_job.arrival_time - current_job.arrival_time)
                print('time %s, %s' % (time, current_job))

            processes_l.insert(0, next_job)

            if next_job.arrival_time > time: time = next_job.arrival_time

        else:  # if current_job is finished remove from process_l
            print('time %s, %s' % (time, current_job))
            processes_l.remove(current_job)
            time = finish_time

        # the process list is empty but still low priority jobs in buffer 1
        if not processes_l and b1:
            next_job = b1[0]
            processes_l.insert(0, b1[0])
            b1.remove(next_job)
