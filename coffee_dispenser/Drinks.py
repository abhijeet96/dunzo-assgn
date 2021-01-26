from .Ingredient import Ingredient

class Drinks:
  #Composition of drinks in ml
  #Since the ingredients maintain an order here,
  #a deadlock will not happen.
  DRINKS = {
    "$GINGER_TEA": {
      "ingredients": {
        Ingredient.MILK: 10,
        Ingredient.WATER: 50,
        Ingredient.TEA_SYRUP: 10,
        Ingredient.GINGER_SYRUP: 5,
        Ingredient.SUGAR_SYRUP: 10
      }
    },
    "$ELAICHI_TEA": {
      "ingredients": {
        Ingredient.MILK: 10,
        Ingredient.WATER: 50,
        Ingredient.TEA_SYRUP: 10,
        Ingredient.ELAICHI_SYPRUP: 5,
        Ingredient.SUGAR_SYRUP: 10
      }
    },
    "$COFFEE": {
      "ingredients": {
        Ingredient.MILK: 10,
        Ingredient.WATER: 50,
        Ingredient.COFFEE_SYRUP: 10,
        Ingredient.SUGAR_SYRUP: 10
      }
    },
    "$HOT_MILK": {
      "ingredients": {
        Ingredient.MILK: 50
      }
    },
    "$HOT_WATER": {
      "ingredients": {
        Ingredient.MILK: 50
      }
    }
  }