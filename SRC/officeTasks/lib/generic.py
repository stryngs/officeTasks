import os
import re
import shutil

class Generic(object):
    """Things that don't have a specific 'thing'"""

    def sweep(self, objName, mkdir = False):
        """Lazy broom attempt for files of directories"""
        if os.path.isdir(objName):
            try:
                shutil.rmtree(objName, ignore_errors = True)
                success = True
            except:
                pass
        else:
            try:
                os.remove(objName)
                success = True
            except:
                pass

        if success is True and mkdir is True:
            os.mkdir(objName)


    def fileMenu(self, fileType = 'csv', mDir = '.'):
        """Create a menu for input based on fileType for the current directory

        Using this function is a nice lazy way to create a numbered menu for
        input based on filetype

        Uses current directory as the default location

        Returns a semi formatted menu
        """
        tgtList = []
        dirList = os.listdir(mDir)
        for i in dirList:
            if re.search('\.{0}$'.format(fileType), i):
                tgtList.append(i)

        fMenu = ''
        for n, i in enumerate(tgtList):
            fMenu += ('[{0}] {1}\n'.format(n, i))
        return fMenu, tgtList
