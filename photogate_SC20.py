#!/usr/bin/env python3
"""
"""
import logging
from gpiozero import DigitalInputDevice
import time
import math
import argparse

class Photogate_SC20(object):
    def __init__(self, gate_0_pin: int, gate_1_pin: int, gate_distance: float, pin_factory = None):
        """
        :type gate0_pin: None
        :type gate1_pin: None
        :type gate_distance: Float
        """
        logging.info('Initializing a photogate.')
        self._gate_0 = DigitalInputDevice(gate_0_pin, pin_factory = pin_factory)
        self._gate_1 = DigitalInputDevice(gate_1_pin, pin_factory = pin_factory)
        self._gate_distance = gate_distance
        self._gate_0_trigger_time = float('nan')
        self._gate_1_trigger_time = float('nan')
        _gate_0.when_deactivated = self._trigger_gate_0
        _gate_1.when_deactivated = self._trigger_gate_1
        
    def _trigger_gate_0(self):
        self._gate_0_trigger_time = time()
    
    def _trigger_gate_1(self):
        return self._gate_1_trigger_time = time()
        
    def reset(self):
        self._gate_0_trigger_time = float('nan')
        self._gate_1_trigger_time = float('nan')
    
    def get_gate_0_trigger_time(self):
        return _gate_0_trigger_time
    
    def get_gate_1_trigger_time(self):
        return _gate_1_trigger_time
    
    def get_gate_distance(self):
        return self._gate_distance
    
    def get_speed(self):
        if math.isnan(_gate_0_trigger_time) or math.isnan(_gate_1_trigger_time):
            return float('nan')
        else:
            return self._gate_distance/(self._gate_1_trigger_time - self._gate_0_trigger_time)
    
    def measure_speed(self):
        self._gate_0.wait_for_inactive()
        self._gate_1.wait_for_inactive()
        return self.get_speed()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Runs the photogate to determine the speed of "
                    "an object that passes through the photogate.")
    parser.add_argument("-p0", dest="pin_0", default=17, type=int,
                        help="GPIO pin of the photogate's gate 0")
    parser.add_argument("-p1", dest="pin_1", default=27, type=int,
                        help="GPIO pin of the photogate's gate 1")
    args = vars(parser.parse_args())

    photogate = Photogate(gate_0_pin=args['pin_0'], gate_1_pin=args['pin_1'])
    print("Running...")
    while True:
        speed = photogate.measure_speed()
        gate_0_trigger_time = photogate.get_gate_0_trigger_time()
        gate_1_trigger_time = photogate.get_gate_1_trigger_time()
        print("Gate 0 Trigger Time:     {:f}".format(gate_0_trigger_time))
        print("Gate 1 Trigger Time:     {:f}".format(gate_1_trigger_time))
        print("Speed:     {:f}".format(speed))
        print("Waiting for the next trigger...")