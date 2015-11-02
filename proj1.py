import os, sys, random, math, bisect, logging
from ds.list import Singly

NDIGITS = 3

class Process(object):
    """
    """
    def __init__(self, procid, arrival_time, service_time):
        """
        """
        self.id = procid
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.CPU_time_completed = service_time
        self.departure_time = 0.0

    def remaining_time(self):
        return self.service_time - self.CPU_time_completed

    def __repr__(self):
        return ("{{id: {},  "
                 "arrival: {}, "
                 "Ts: {}, "
                 "completed: {}, "
                 "departure: {}}}".format(
                    self.id,
                    round(self.arrival_time, NDIGITS),
                    round(self.service_time, NDIGITS),
                    round(self.CPU_time_completed, NDIGITS),
                    round(self.departure_time, NDIGITS)
                 ))

class Event(object):
    """
    """
    def __init__(self, event_type, time):
        self.event_type = event_type
        self.time = time

    def __repr__(self):
        return ('{{type: {}, event time: {}}}'
                .format(EventType.mapping[self.event_type],
                        round(self.time, NDIGITS)))

class EventType:
    arrival, timeslice, departure, sample = range(4)

    mapping = {
        0 : 'arrival',
        1 : 'timeslice',
        2 : 'departure',
        3 : 'sample',
    }

class BaseScheduler(object):
    """
    """
    def __init__(self, arrival_rate, sim):
        self.process_list = []
        self.ready_queue = []
        self.sim = sim
        self.CPU = None

    def analyze(self):
        """
        """
        logging.debug('\t(7)\tanalyze, ready queue: {}'.format(self.ready_queue))
        if len(self.ready_queue) > 0:
            logging.debug('\t(8)\tscheduling: {}'.format(self.ready_queue[0]))
            self.schedule(self.ready_queue[0])

    def check(self):
        """prepares to schedule CPU
        """
        logging.debug('\t(6)\tcheck, CPU: {}'.format(self.CPU))

        if not self.CPU:
            self.analyze()
        elif self.CPU.remaining_time() <= 0:
            self.egress(self.CPU)
            self.analyze()

    def schedule(self, process):
        """removes process from ready queue, sends to CPU"""
        self.ready_queue.remove(process)
        current_time = self.sim.clock
        process.departure_time = current_time + process.service_time
        self.sim._schedule_departure(process)
        self.CPU = process

    def ingress(self, process):
        self.process_list.append(process)
        self.ready_queue.append(process)
        self.check()

    def egress(self, process):
        self.sim._record_departure(process)

class FCFS(BaseScheduler):
    """
    """
    def __init__(self, arg1, arg2):
        super(FCFS, self).__init__(arg1, arg2)

class SRTF(BaseScheduler):
    """
    """
    def __init__(self, arg1, arg2):
        super(SRTF, self).__init__(arg1, arg2)

class RR(BaseScheduler):
    """
    """
    def __init__(self, arg1, arg2):
        super(RR, self).__init__(arg1, arg2)

class HRTF(BaseScheduler):
    """
    """
    def __init__(self, arg1, arg2):
        super(HRTF, self).__init__(arg1, arg2)

class Simulator(object):
    """
    """
    rand = random.SystemRandom()

    @classmethod
    def genexp(cls, arrival_rate):
        """
        """
        x = 0
        while (x == 0):
            u =  Simulator.rand.uniform(0,1)
            x = (-1/float(arrival_rate))*math.log(u)
        return x

    def __init__(self, arrival_rate, arg2):
        """
        """
        #self.event_queue = Singly()
        self.schedulers = [ FCFS(arrival_rate, self),
                            SRTF(arrival_rate, self),
                            RR(arrival_rate, self),
                            HRTF(arrival_rate, self) ]
        self.current_scheduler = None
        self.event_mapping = {
            0 : self._dispatch_process, # arrival
            1 : self._trigger_scheduler, # timeslice
            2 : self._record_departure, # departure
            3 : self._sample_ready_queue, # sample
        }
        self.arrival_rate = arrival_rate
        self._reset()

    def _reset(self):
        """
        """
        self.event_queue = []
        self.process_list = []
        self.running = True
        self.clock = 0.0
        self.last_arrival = None
        self.lastid = 0
        self.departure_count = 0

    def _process_results(self):
        """
        """
        pass

    def _schedule_arrival(self):
        """
        """
        time_offset = 0.0
        if self.last_arrival:
            time_offset = self.last_arrival.time

        new_event_time = Simulator.genexp(self.arrival_rate) + time_offset
        logging.debug("\t(1)\tnew {}, time: \t{}, current: \t{}, diff: \t{}"
                      .format(EventType.mapping[EventType.arrival],
                              round(new_event_time, NDIGITS),
                              round(self.clock, NDIGITS),
                              round(new_event_time-self.clock, NDIGITS)))
        new_event = Event(EventType.arrival, new_event_time)

        #logging.debug('schedule arrival: {}'.format(new_event))

        self.last_arrival = new_event
        bisect.insort_left(self.event_queue, new_event)

        #logging.info(self.event_queue[-1])

    def _genid(self):
        """
        """
        self.lastid += 1
        return self.lastid

    def _dispatch_process(self, event):
        """
        """
        #logging.debug("\t(4)\tdispatch {}, time: \t{}, current: \t{}, diff: \t{}\n"
        #              .format(EventType.mapping[event.event_type],
        #                      round(event.time, NDIGITS),
        #                      round(self.clock, NDIGITS),
        #                      round(event.time-self.clock, NDIGITS)))
        new_process = Process(self._genid(), self.clock, 0.06)
        logging.debug('\t(4)\tdispatch {}'.format(new_process))
        self.current_scheduler.ingress(new_process)

    def _schedule_departure(self, process):
        """
        """
        new_event = Event(EventType.departure, process.departure_time)
        self.event_queue.append(new_event)

    def _trigger_scheduler(self):
        """
        """
        logging.debug('\t()\ttrigger scheduler')
        self.current_scheduler.check()

    def _record_departure(self, process):
        """
        """
        logging.debug('\t(5)\trecord departure #{}: {}'
                        .format(self.departure_count, process))
        self.departure_count += 1

    def _sample_ready_queue(self):
        """
        """
        logging.debug('\t()\tsample')
        pass

    def run(self):
        """
        """
        tmp = 0
        for scheduler in self.schedulers:
            self.current_scheduler = scheduler
            while self.running:
                self._schedule_arrival()

                next_event = self.event_queue[0]
                logging.debug('\t(2)\tnext event: {}, event queue length: {}'
                                .format(next_event, len(self.event_queue)))
                self.event_queue.remove(next_event)
                logging.debug('\t(3)\tremoving from queue, event queue length: {}'
                                .format(len(self.event_queue)))
                self.clock = next_event.time

                self.event_mapping[next_event.event_type](next_event)

                tmp += 1
                print
                print self.event_queue
                print
                if self.departure_count > 3:
                    self.running = False

        self._process_results()
        self._reset()
        #print self.genexp(self.arg1)

        # ////////////////////////////////////////////////////////////
        # int run_sim()
        # {
        #   struct event* eve;
        #   while (!end_condition)
        #     {
        #       eve = head;
        #       clock = eve->time;
        #       switch (eve->type)
        # 	{
        # 	case EVENT1:
        # 		process_event1(eve);
        # 		break;
        # 	case EVENT2:
        # 		process_event2(eve);
        # 		break;
        #
        # 	// add more events
        #
        # 	default:
        # 		// error
        # 	}
        #
        #       head = eve->next;
        #       free(eve);
        #       eve = NULL;
        #     }
        #   return 0;
        # }
        # ////////////////////////////////////////////////////////////////

def main(argv):
    """
    """
    logging.basicConfig(level=logging.DEBUG)
    sim = Simulator(int(argv[1]), int(argv[2]))
    results = sim.run()

def usage():
    """
    """
    print "Usage:"
    print "$ python proj1 arg1 arg2"

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
        sys.exit()

    main(sys.argv)
