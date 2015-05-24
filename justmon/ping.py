from datetime import datetime
from twisted.application.internet import TimerService
from twisted.internet.defer import inlineCallbacks
from twisted.internet.utils import getProcessOutput
from twisted.python import log


class PingService(TimerService):
    def __init__(self, step, db, cmd):
        TimerService.__init__(self, step, self.ping)

        self.db = db
        self.cmd = cmd

    @inlineCallbacks
    def ping(self):
        output = yield getProcessOutput(self.cmd, args=self.db.getHosts(), errortoo=True)
        log.msg('; '.join(output.splitlines()))

        for host, status in [line.split(' ', 1) for line in output.splitlines()]:
            self.db.setHostStatus(host, datetime.now(), status == 'is alive')
