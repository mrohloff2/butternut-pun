import json
from time import sleep
import pandas as pd
import requests

"""
Max Rohloff
4/24/2023
Purpose: Pull information from RESTCONF to access interface information from our IOS XE devices then change the IP address information by asking the user which interface and IP they would like to change
"""