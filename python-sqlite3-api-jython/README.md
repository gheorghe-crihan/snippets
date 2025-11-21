# Rationale
In CPython 2.7 ```sqlite3``` is a stock module. However, due to not providing
Java bindings, it is not part of standard Jython distribution. The module
allows running from under Jython through the native Python sqlite3 API,
facilitating the porting efforts.

**NOTE: This is only a very crude wrapper or emulation layer and by no means a
fully-functional replacement, as most of the methods are not implemented or
are just stubs. In particular, it lacks any error codes or exception support.**

It only allows to run certain software, for one, the NLTK modules
(```nltk/corpus/reader/panlex-lite.py```, ```nltk/corpus/reader/sem80.py```
but probably **NOT** ```nltk/sem/relextract.py```).

Works grace to the fact that Python imports any module exactly once, or,
rather, the sqlite3 mimic module being in the ```CLASSPATH```.
