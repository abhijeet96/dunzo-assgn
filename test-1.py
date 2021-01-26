def start_dispenser():
  dispenser.run()

from coffee_dispenser.Dispenser import Dispenser
from coffee_dispenser.Inventory import Inventory

import threading
import time
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format,
                    filename='test-1-debug.log',
                    filemode='w',
                    level=logging.INFO)

inventory = Inventory()
logging.info(inventory.current_inventory)
dispenser = Dispenser(outlets=3, inventory=inventory)

t = threading.Thread(target=start_dispenser)
t.start()
dispenser.request_drinks(drinks=["$GINGER_TEA", "$ELAICHI_TEA"])
dispenser.request_drinks(drinks=["$COFFEE", "$COFFEE", "$COFFEE"])
time.sleep(10)
dispenser.request_drinks(drinks=["$COFFEE"])

#ending test on user driven SIGTERM
#should have done it gracefully, but this serves the purpose for now.
