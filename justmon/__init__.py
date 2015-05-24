from twisted.application import internet, service

from data import DB
from web import WebSite
from ping import PingService


def makeService(options):
    db = DB(options['database'], options['hosts'])
    services = service.MultiService()
    internet.TCPServer(options['port'], WebSite(db), interface=options['host']).setServiceParent(services)
    PingService(options['interval'], db, options['command']).setServiceParent(services)
    return services
