import json
import logging
import threading
import os

class Inventory:
  """
  Used to maintain the inventory in the coffee machine.
  """
  def __init__(self, config_path="config_inventory.json"):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(dir_path, config_path), "r")
    self._current_inventory = json.loads(f.read())

    logging.info(f"Inventory: {self._current_inventory}")

    #initialising locks on each ingredient
    self._locks = {}
    for item, val in self._current_inventory.items():
      self._locks[item] = threading.Lock()

  @property
  def current_inventory(self):
    return self._current_inventory

  @property
  def locks(self):
    return self._locks

  def replenish(self, ingredient, amount) -> bool:
    """
    increase the inventory of a particular ingredient by an amount (ml)
    :return:
    """
    if ingredient not in self.current_inventory:
      logging.error("Ingredient {} not supported.".format(ingredient))
      raise Exception("Ingredient {} not supported.".format(ingredient))

    with self._locks[ingredient]:
      logging.debug("lock on {}".format(ingredient))
      self.current_inventory[ingredient]['amount'] += amount
      logging.debug("Releasing lock on {}".format(ingredient))

    logging.debug(f"Ingredient {ingredient} replenished by {amount}")
    return True

  def consume(self, ingredient, amount) -> bool:
    """
    decrease the inventory of a particular ingredient by an amount (ml)
    """
    if ingredient not in self.current_inventory:
      logging.error("Ingredient {} not supported.".format(ingredient))
      raise Exception("Ingredient {} not supported.".format(ingredient))

    if self.current_inventory[ingredient]['amount'] < amount:
      return False

    with self._locks[ingredient]:
      logging.debug("lock on {}".format(ingredient))
      self.current_inventory[ingredient]['amount'] -= amount
      logging.debug("Releasing lock on {}".format(ingredient))

    logging.debug(f"Ingredient {ingredient} used up by {amount}")
    return True
