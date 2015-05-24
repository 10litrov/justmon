Just Monitor
============

A simple python program for host monitoring.

`Twisted <https://twistedmatrix.com/trac/>`_ and `fping <http://fping.org/>`_ required.

Usage: twistd [options] justmon [options] [host[=caption]...]
Options:
  -d, --database=  Database file path [default: ./justmon.db]
  -h, --host=      HTTP server interface address [default: localhost]
  -p, --port=      HTTP server interface port [default: 8080]
  -i, --interval=  Hosts check interval [default: 30]
  -c, --command=   fping location [default: /usr/local/bin/fping]
