This aims to design a coffee dispenser with a pre-set drinks menu and a list of
pre-set ingredients. However, this can be modified as per convenience. In a
3-tier app, this would anyways reside in the DB.

Features:
- Serves you a drink if enough ingredients are available
- Throws an alert if any ingredient goes below a certain configurable limit
- Allows you to replenish an ingredient

Deadlock on ingredients was avoided by using ordered dictionary of drinks.

