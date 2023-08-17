from .lib import compares
from .lib import csv
from .lib import eml
from .lib import generic

"""
Storing XML thoughts just because

## Base
tree = etree.parse(xml)
root = self.tree.getroot()

## Iteratives
iterList = [i for i in self.root.iter()]
iterSet = set(self.iterList)
rootList = list(self.root)
"""

## Instantiations
cmp = compares.Compare()
csv = csv.Csv()
eml = eml.Eml()
gnr = generic.Generic()
