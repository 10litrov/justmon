import re
from twisted.enterprise import adbapi


class DB:
    # https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/converters.py
    ESCAPE_REGEX = re.compile(r"[\0\n\r\032\'\"\\]")
    ESCAPE_MAP = {'\0': '\\0', '\n': '\\n', '\r': '\\r', '\032': '\\Z', '\'': '\\\'', '"': '\\"', '\\': '\\\\'}

    def __init__(self, path, hosts):
        self.hosts = hosts

        self.pool = adbapi.ConnectionPool('sqlite3', path, check_same_thread=False)
        self.pool.runInteraction(self._createSchema)

    # https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/converters.py
    def _escape(self, value):
        return "'%s'" % ("%s" % (self.ESCAPE_REGEX.sub(lambda match: self.ESCAPE_MAP.get(match.group(0)), value),))

    @staticmethod
    def _nameRow(result, columns):
        return [dict(zip(columns, row)) for row in result]

    @staticmethod
    def _createSchema(cursor):
        cursor.execute('CREATE TABLE IF NOT EXISTS pings (host TEXT, date INTEGER, status INTEGER)')
        cursor.execute('CREATE INDEX IF NOT EXISTS host_idx ON pings (host)')
        cursor.execute('CREATE INDEX IF NOT EXISTS date_idx ON pings (date)')

    def getHosts(self):
        return self.hosts.keys()

    def getAllHostStatus(self):
        def hideHosts(data):
            for row in data:
                if self.hosts.get(row['name']):
                    row['name'] = self.hosts[row['name']]
            return data

        query = 'SELECT l.host, l.date, p.status FROM pings AS p ' \
                'INNER JOIN (SELECT host, max(date ) AS date ' \
                'FROM pings WHERE host IN (%s) GROUP BY host) AS l ' \
                'ON p.host = l.host AND p.date = l.date' \
                % ','.join([self._escape(host) for host in self.hosts.keys()])
        return self.pool.runQuery(query)\
            .addCallback(self._nameRow, ['name', 'last', 'status'])\
            .addCallback(hideHosts)

    def setHostStatus(self, host, date, status):
        return self.pool.runOperation(
            'INSERT INTO pings (host, date, status) VALUES (?, ?, ?)', (host, date, status))
