from twisted.application import internet, service
from twisted.internet import interfaces
from twisted.python import usage

import justmon


class Options(usage.Options):
    optParameters = [
        ['database', 'd', './justmon.db', 'Database file path'],
        ['host', 'h', 'localhost', 'HTTP server interface address'],
        ['port', 'p', 8080, 'HTTP server interface port'],
        ['interval', 'i', 30, 'Hosts check interval'],
        ['command', 'c', '/usr/local/bin/fping', 'fping location'],
    ]
    # optFlags = []

    def parseArgs(self, *args):
        self['hosts'] = dict([(arg.split('=', 1)+[None])[:2] for arg in args])

    def getSynopsis(self):
        return super(Options, self).getSynopsis() + ' [host[=caption]...]'


def makeService(options):
    return justmon.makeService(options)
