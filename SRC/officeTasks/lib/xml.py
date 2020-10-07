from lxml import etree

class Xml(object):
    """Work with XML"""

    def rootGrabber(self, xml):
        """Return useful iterations for the xml"""

        ## Base
        self.tree = etree.parse(xml)
        self.root = self.tree.getroot()

        ## Iteratives
        self.iterList = [i for i in self.root.iter()]
        self.iterSet = set(self.iterList)
        self.rootList = list(self.root)
