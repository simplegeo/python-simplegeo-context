#!/usr/bin/env python

import random
import time
import numpy

from simplegeo.context import Client
from simplegeo.shared import APIError

MY_OAUTH_KEY = ''
MY_OAUTH_SECRET = ''

API_VERSION = '1.0'
API_HOST = ''
API_PORT = 80

class PerformanceTest(object):
    def __init__(self, number_of_requests=10000):
        self.number_of_requests = number_of_requests
        self.client = Client(MY_OAUTH_KEY, MY_OAUTH_SECRET, API_VERSION, API_HOST, API_PORT)
        print self.client
        self.responses = []

    def run(self):
        requests_completed = 0
        requests_failed = 0

        for i in range(self.number_of_requests):
            try:
                print 'Trying request %s' % i
                timed_response = self._timed_response()
                requests_completed += 1
                self.responses.append(timed_response)
            except APIError:
                requests_failed += 1
                
        print self.responses
        print '%s requests completed, %s requests failed' % (requests_completed, requests_failed)

        times = [response['time_elapsed'] for response in self.responses]
        print '\n\nmin: %s max: %s avg: %s\n\n' % (min(times), max(times), (sum(times) / len(times)))
        bins = [i * 0.1 for i in range(20)] + [2.0] + [10.0]
        histogram = numpy.histogram(times, bins=bins)
        frequencies = [frequency for frequency in histogram[0]]
        bins = [bin for bin in histogram[1]]
        for (i, bin) in enumerate(bins):
            print '%ss' % bin
            try:
                print '\t' + str(frequencies[i]) + '\t' + '=' * frequencies[i]
            except:
                pass

    def _timed_response(self):
        (lat, lon) = self._random_lat_lon()
        print 'Timing client.get_context(%s, %s)' % (lat, lon)
        start_time = time.time()
        response = self.client.get_context(lat, lon)
        time_elapsed = time.time() - start_time
        print time_elapsed
        return {'lat': lat,
                'lon': lon,
                'response': response,
                'time_elapsed': time_elapsed}

    def _random_lat_lon(self):
        return (random.uniform(-90.0, 90.0), random.uniform(-180.0, 180.0))

def main():
    performance_test = PerformanceTest()
    performance_test.run()

if __name__ == '__main__':
    main()
