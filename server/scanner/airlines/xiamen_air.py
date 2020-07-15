from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import sys
from bs4 import BeautifulSoup
import time
import numpy as np
from datetime import datetime
from scanner.common import send_keys_delay_random
from flights_db import insert_to_db
from flight_message_alert import alert_on_valuable_flight, alert_on_valuable_flight_test
import re



