import getpass
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from time import sleep

class Eml(object):
    """Send an email via Python"""

    def conDetails(self, server, uname, pword, debug = False, port = 587):
        """Connection details"""
        if debug is False:
            self.debug = 0
        else:
            self.debug = 1
        self.server = server
        self.sender = uname
        self.password = pword
        self.port = port


    def mxPrep(self, rcpList, subject, body, dName = None, rName = None):
        """Prep the contents of the email"""
        self.rName = rName
        if dName is None:
            self.dName = self.sender
        else:
            self.dName = dName
        self.recipients = rcpList
        self.subject = subject
        self.body = body


    def mxCon(self, multi = False):
        """Setup the mx connection"""
        self.sendObj = smtplib.SMTP(self.server + ':{0}'.format(str(self.port)))
        self.sendObj.set_debuglevel(self.debug)
        if multi is not False:
            self.multi = True
        else:
            self.multi = False


    def mxSend(self):
        """Send the mx"""
        ## Connect based on mxCon
        self.sendObj.starttls()
        self.sendObj.login(self.sender, self.password) ### What if we login multiple times on the same obj?

        ## Prep the msg
        msg = MIMEText(self.body)
        msg.set_type('text/html')
        msg['Subject'] = self.subject
        msg['From'] = formataddr((str(Header(self.dName)), self.sender))
        try:
            msg['To'] = ", ".join(self.recipients)
        except:
            print(self.recipients)
            print(', '.join(self.recipients))
        if self.rName is not None:
                msg['reply-to'] = self.rName

        ## Send the mail, by default close connection
        self.sendObj.sendmail(self.sender, self.recipients, msg.as_string())
        if self.multi is False:
            self.sendObj.close()


    def wrapper(self):
        """Quick interactive email send"""
        try:
            svr = raw_input('Server name?\n')
            prt = raw_input('Port? [587]\n')
            if prt == '':
                prt = 587
            tRcp = raw_input('Recipients? (sep by , for multiple)\n')
            rcp = [i.strip() for i in tRcp.split(',')]
            sbj = raw_input('Subject?\n')
            bdy = raw_input('Body?\n')
            dbg = raw_input('Debug mode [0]\n')
            if dbg == '':
                dbg = False
            else:
                dbg = True
            uname = raw_input('User name?\n')
        except:
            svr = input('Server name?\n')
            prt = input('Port? [587]\n')
            if prt == '':
                prt = 587
            tRcp = input('Recipients? (sep by , for multiple)\n')
            rcp = [i.strip() for i in tRcp.split(',')]
            sbj = input('Subject?\n')
            bdy = input('Body?\n')
            dbg = input('Debug mode? [0]\n')
            if dbg == '':
                dbg = False
            else:
                dbg = True
            uname = input('User name?\n')
        pword = getpass.getpass('Password?\n')
        self.conDetails(svr, uname, pword, debug = dbg, port = prt)
        self.mxPrep(rcp, sbj, bdy)
        self.mxCon()
        self.mxSend()

if __name__ == '__main__':
    em = Eml()
    em.wrapper()
