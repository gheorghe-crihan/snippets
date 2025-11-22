# In CPython 2.7 sqlite3 is a stock module. However, due to not providing Java
# bindings, it is not part of standard Jython distribution. This allows running
# from under Jython through the native Python sqlite3 API, facilitating porting
# efforts. 
# NOTE: This is only a very crude wrapper or emulation layer and by no means a
# fully-functional replacement, as most of the methods are not implemented or
# are just stubs. In particular, it lacks any error codes or exception support.
# It only allows to run certain software, for one, the NLTK modules
# (nltk/corpus/reader/panlex-lite.py, nltk/corpus/reader/sem80.py but probably
# NOT nltk/sem/relextract.py).
# Works grace to the fact that Python imports any module exactly once, or,
# rather, the sqlite3 mimic module being in the CLASSPATH.

from java.lang import Class
from java.sql  import DriverManager, SQLException, Statement, Types

class Row(object):
    def __init__(self, rs):
        self._rs = rs

    def _fetch_rs_cortage(self):
        """Implement Python's fetch() behavior, that is, glue all the types
           into a single cortage.
           NOTE: relies on result set not being empty (checked by the caller).
        """
        _res = []
        _md = self._rs.getMetaData()
        for i in range(self._rs.getColumnCount()):
            _type = _md.getColumnType(i+1)
            if _type == Types.VARCHAR or _type == Types.CHAR:
                _res.append(self._rs.getString(i+1))
            elif _type == Types.INTEGER:
                _res.append(self._rs.getInt(i+1))
            elif _type == Types.FLOAT:
                _res.append(self._rs.getFloat(i+1))
            # TODO: Add more type support!
            # at least the following: DOUBLE, DATE, BIGINT, BOOLEAN, NULL,
            # NUMERIC, TIME, TIMESTAMP, VARCHAR
        return _res

    def fetch(self):
        if self._rs is not None:
            if self._rs.next():
                return self._fetch_rs_cortage()
            else:
                return []

    def fetchall(self):
        _res = []
        if self._rs is not None:
            while self._rs.next():
                _res.append(self._fetch_rs_cortage())
            return _res

    def fetchone(self):
        return self.fetch()


class Cursor(object):
    def __init__(self, con):
        self._row = None
        self.connection = con

    def close(self):
        pass

    def execute(self, statement):
        _st = self.connection.createStatement()
        _is_query = _st.execute(statement)
        if _is_query:
            self._row = Row(_st.getResultSet())
        else:
            return _st.getUpdateCount()        
        return self._row

    def executemany(self):
        pass


class Connection(object):
    def __init__(self, conn_str):
        self._conn_str = conn_str
        _JDBC_URL = 'jdbc:sqlite:%s' % ( conn_str, )
        self._conn = DriverManager.getConnection(_JDBC_URL)#, "org.sqlite.JDBC")
        self._cursor = Cursor(self._conn)

    def close(self):
        pass

    def cursor(self):
        return self._cursor

    def commit():
        pass

    def rollback():
        pass


def connect(conn_str):
    return Connection(conn_str)

def complete_statement(statement):
    pass

def enable_callback_tracebacks(flag, ):
    pass

 