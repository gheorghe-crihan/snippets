#!/bin/sh
mvn package
jar --create --file=sqlite3.jar -C sqlite3 .
