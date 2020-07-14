import time
import os
import sys
import numpy as np


def send_keys_delay_random(controller,keys,min_delay=0.05,max_delay=0.25):
    for key in keys:
        controller.send_keys(key)
        time.sleep(np.random.uniform(low=min_delay,high=max_delay))

