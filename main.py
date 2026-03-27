from banner_parser import *
from scanner import *
import asyncio


sites=input_take()
asyncio.run(scan(sites))
