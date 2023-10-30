#!/usr/bin/env python

import argparse
import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def getArgs():
    ''' Parse given arguments
    '''

    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('filename', help='File with color hashes')
    parser.add_argument('--min', type=int, metavar='Int', required=True, help='Start sequence number')
    parser.add_argument('--max', type=int, metavar='Int', required=True, help='End sequence number')
    parser.add_argument('--iteration', type=int, metavar='Int',required=True, help='Iteration number')

    if len(sys.argv) == 1:
        logger.info(' Printing help')
        args = parser.parse_args(['-h'])

    else:
        args = parser.parse_args()
        return args

def printGradientGauge(args):
    ''' Prints gradient gauge as a yaml configuration for usage with HomeAssistant
    '''

    min = args.min
    max = args.max
    iteration = args.iteration
    filename = args.filename

    fhandler = open (filename, 'r')

    print(
        '''
type: gauge
entity: sensor.<SENSOR>
name: <NAME>
needle: true
min: {}
max: {}
segments: '''.format(min, max)
        )
    
    sequence = min - iteration
    for line in fhandler.readlines():
        sequence += iteration
        print("  - from: {}".format(sequence))
        print("    color: '{}'".format(line.rstrip()))


if __name__ == "__main__":
    try:
        args = getArgs()
        printGradientGauge(args)

    except KeyboardInterrupt:
        logger.warning(" Script interrupted by user!")

    except FileNotFoundError as error2:
        logger.error(error2)


