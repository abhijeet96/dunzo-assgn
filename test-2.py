def start_dispenser():
  dispenser.run()

from coffee_dispenser.Dispenser import Dispenser
from coffee_dispenser.Inventory import Inventory

import threading
import time
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format,
                    filename='test-2.log',
                    filemode='w',
                    level=logging.INFO)

inventory = Inventory()
logging.info(inventory.current_inventory)
dispenser = Dispenser(outlets=2, inventory=inventory)

t = threading.Thread(target=start_dispenser)
t.start()
#notice no ALERT on COFFEE_SYRUP
inventory.replenish("$COFFEE_SYRUP", 100)
#mimics ordering two drinks at once
dispenser.request_drinks(drinks=["$HOT_MILK", "$ELAICHI_TEA"])
dispenser.request_drinks(drinks=["$COFFEE", "$HOT_MILK"])
time.sleep(10)
dispenser.request_drinks(drinks=["$GINGER_TEA"])

#ending test on user driven SIGTERM
#should have done it gracefully, but this serves the purpose for now.