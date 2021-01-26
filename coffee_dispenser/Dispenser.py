import threading
import queue
import time
import logging

from .Inventory import Inventory
from .Drinks import Drinks

class ServiceExit(Exception):
  """
  Custom exception which is used to trigger the clean exit
  of all running threads and the main program.
  """
  pass

class MonitorInventory(threading.Thread):
  """
  This thread is used to monitor the inventory and throws an alert if
  an ingredient goes below a specific level.
  """
  def __init__(self, inventory):
    threading.Thread.__init__(self)
    self.inventory = inventory
    self.shutdown_flag = threading.Event()

  def monitor_inventory(self):
    current_inventory = self.inventory.current_inventory
    for item, info in current_inventory.items():
      if info["amount"] < info["reminder"]:
        logging.info(f"ALERT: Running low on {item}, please restock.")

  def run(self):
    while not self.shutdown_flag.is_set():
      self.monitor_inventory()
      time.sleep(30)


class Task(threading.Thread):
  """
  Number of threads spawned
  will be equal to outlets. Each thread will poll the shared
  queue and process the task request.
  """
  def __init__(self, task_queue, inventory):
    threading.Thread.__init__(self)
    self.shutdown_flag = threading.Event()
    self.task_queue = task_queue
    self.inventory = inventory

  def make_drink(self):
    """
    Pops an item from the queue, tries to get a lock on all ingredients,
    and if possible, serves drink.
    else, rolls back lock on ingredients reserved (if any).
    :return:
    """
    logging.info("Waiting for task...")
    task = self.task_queue.get(block=True)
    logging.debug(f"Picked up {task}")

    #fetches information about drink
    drink_info = Drinks.DRINKS.get(task, None)

    if not drink_info:
      raise Exception("Unknown drink: {}".format(task))

    acquired_locks = []
    res = True

    for ingredient, qty in drink_info['ingredients'].items():
      res = self.inventory.consume(ingredient=ingredient, amount=qty)
      if res:
        acquired_locks.append((ingredient, qty))
      else:
        logging.error(f"{task} couldn't be served. Not enough {ingredient}")
        break

    if not res:
      #rolling back if not enough resources
      for acq_lock in acquired_locks:
        self.inventory.replenish(ingredient=acq_lock[0], amount=acq_lock[1])
      return
    else:
      #serving drink
      #I believed it would be more intuitive if the message is shown like this
      #with a sleep.
      logging.info("Serving Drink: {}".format(task))
      time.sleep(2)
      logging.info("Finished Serving Drink: {}".format(task))
      logging.debug(self.inventory.current_inventory)


  def run(self):
    while not self.shutdown_flag.is_set():
      self.make_drink()
      time.sleep(5)


class Dispenser:
  """
  Entrypoint to the Dispenser.
  """
  def __init__(self, outlets: int, inventory: Inventory, **kwargs):
    self.outlets = outlets
    self.inventory = inventory

    #thread-safe queue
    self.task_queue = queue.Queue(maxsize=self.outlets)

  def add_drink_to_task_queue(self, drink):
    """
    adds drink to task queue.
    :param drink
    """
    self.task_queue.put(item=drink, block=True)

  def request_drinks(self, drinks):
    """
    This function is exposed to mimic ordering multiple drinks at once.
    orders the given list of drinks at once.
    :param drinks: (list) of Drinks
    """
    threads = []
    drinks = drinks[:self.outlets]
    for drink in drinks:
      logging.debug(f"Adding {drink}")
      t = threading.Thread(target=self.add_drink_to_task_queue,
                           kwargs={"drink": drink})
      threads.append(t)
      t.start()

    for t in threads:
      t.join()

  def run(self):
    worker_threads = list()
    try:
      for _ in range(self.outlets):
        t = Task(task_queue=self.task_queue, inventory=self.inventory)
        worker_threads.append(t)
        t.start()

      monitor_amt = MonitorInventory(inventory=self.inventory)
      monitor_amt.start()

      while True:
        time.sleep(0.5)

    except ServiceExit:
      for t in worker_threads:
        t.shutdown_flag.set()
      monitor_amt.shutdown_flag.set()

      for t in worker_threads:
        t.join()
      monitor_amt.join()