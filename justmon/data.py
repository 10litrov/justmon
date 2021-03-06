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
    def _makeNamedColumns(result, columns):
        return [dict(zip(columns, row)) for row in result]

    def _hideHosts(self, data):
        for row in data:
            if self.hosts.get(row['name']):
                row['name'] = self.hosts[row['name']]
        data.sort(key=lambda x: x['name'])
        return data

    @staticmethod
    def _createSchema(cursor):
        cursor.execute('CREATE TABLE IF NOT EXISTS pings (host TEXT, date INTEGER, status INTEGER)')
        cursor.execute('CREATE INDEX IF NOT EXISTS host_idx ON pings (host)')
        cursor.execute('CREATE INDEX IF NOT EXISTS date_idx ON pings (date)')
        cursor.execute('CREATE TRIGGER IF NOT EXISTS ins_trg BEFORE INSERT ON pings '
                       'WHEN NEW.status IN (SELECT status FROM pings WHERE host=NEW.host ORDER BY date DESC LIMIT 1) '
                       'BEGIN SELECT RAISE(IGNORE); END')

    def getHosts(self):
        return self.hosts.keys()

    def getHostsStatus(self):
        query = 'SELECT l.host, strftime("%%Y-%%m-%%dT%%H:%%M:%%SZ", l.date, "unixepoch"), p.status FROM pings AS p ' \
                'INNER JOIN (SELECT host, max(date) AS date ' \
                'FROM pings WHERE host IN (%s) GROUP BY host) AS l ' \
                'ON p.host = l.host AND p.date = l.date' \
                % ','.join([self._escape(host) for host in self.hosts.keys()])
        return self.pool.runQuery(query)\
            .addCallback(self._makeNamedColumns, ['name', 'last', 'status'])\
            .addCallback(self._hideHosts)

    def setHostStatus(self, host, date, status):
        return self.pool.runOperation(
            'INSERT INTO pings (host, date, status) VALUES (?, ?, ?)', (host, date, status))

    def getHostStats(self, host):
        query = ''
        return self.pool.runQuery(query, )\
            .addCallback(self._makeNamedColumns, [])
