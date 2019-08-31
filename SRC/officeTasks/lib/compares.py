import re
import officeTasks as OT

class Compare(object):
    """All things, comparison related"""
    
    def __init__(self):
        self.ipCapture = re.compile('\\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b')


    def hostsCompare(self, fullHost, foundHost, dotPatch = True):
        """Reports what was found and not found
        
        dotPatch comes from the FQDN vs hostname concept
        If you set dotPatch = False, foo.bar.com stays foo.bar.com
        If you leave dotPatch = True, foo.bar.com becomes foo for comparison
        IPv4 is immunized against dotPatch, however IPv6 isn't
        Future versions will patch IPv6
        """
        ## Rip
        with open(fullHost, 'r') as iFile:
            fullList = iFile.read().splitlines()
        with open(foundHost, 'r') as iFile:
            foundList = iFile.read().splitlines()
        
        ## Deal with capitals
        fullSet = set([i.lower() for i in fullList])
        foundSet = set([i.lower() for i in foundList])
        
        ## Deal with duplicates
        print ('')
        if len(fullSet) != len(fullList):
            dLen = len(fullList) - len(fullSet)
            print ('Duplicates in FULL: {0}\n'.format(str(dLen)))
        if len(foundSet) != len(foundList):
            dLen = len(foundList) - len(foundSet)
            print ('Duplicates in FOUND: {0}\n'.format(str(dLen)))
        
        ## dotPatch cycle
        if dotPatch is True:
            dpFull = set()
            dpFound = set()
            for i in fullSet:
                ## Verify not IP -- kinda
                if not re.findall(self.ipCapture, i):
                    dpFull.add(i.split('.')[0])
                else:
                    dpFull.add(i)
            for i in foundSet:
                ## Verify not IP -- kinda
                if not re.findall(self.ipCapture, i):
                    dpFound.add(i.split('.')[0])
                else:
                    dpFound.add(i)
            fullSet = dpFull
            foundSet = dpFound
        
        ## Compare
        notFound = fullSet - foundSet
        found = fullSet.intersection(foundSet)
        extras = foundSet - fullSet
        
        ## Notate
        print ('Unique quantity in FULL: {0}\n'.format(len(fullSet)))
        print ('Unique quantity in FOUND: {0}\n\n'.format(len(foundSet)))
        if len(notFound) > 0:
            print ('notFound exists: {0}\n'.format(str(len(notFound))))
        if len(found) > 0:
            print ('found exists: {0}\n'.format(str(len(found))))
        if len(extras) > 0:
            print('extras exists {0}\n'.format(str(len(extras))))

        return found, notFound, extras


    def hirShort(self, csv):
        """Take a host inventory report, insert a short hostname column and
        lower() them
        
        This makes comparisons between lists of hosts that mix FQDN and shorts,
        easier
        
        returns headers and the (list, tupled)
        """
        ipCapture = re.compile('\\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b')
        print('shortening {0}\n'.format(csv))
        cList = OT.csv.csv2list(csv)
        
        ## Get headers
        headerList = cList.pop(0)
        headerList.insert(0, 'sn')
        
        ## Iterate through the rows, and sn it
        nList = []
        for i in cList:
            
            ## Lowercase it
            i[0] = i[0].lower()
            
            ## Verify not IP -- kinda
            if not re.findall(ipCapture, i[0]):
                sn = i[0].split('.')[0]
            else:
                sn = i[0]
                
            x = i
            x.insert(0, sn)
            nList.append(x)
        return headerList, nList
