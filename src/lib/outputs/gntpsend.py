# -*- coding: utf-8 -*-
from lib.core import Output
from subprocess import call

class GntpSend(Output):
    def init(self):
        self.title = getattr(self, "title", "from Boxnya")


    def throw(self, packet):
        message = packet["data"]
        if isinstance(message, unicode):
            message = message.encode("utf-8")
        else:
            message = str(message)

        cmdline = ["gntp-send", self.title, message]
        self.log("cmd: " + " ".join(cmdline))
        call(cmdline, shell=False)
