#!/usr/bin/env bash

while true; do
	kinit `cat /keytab/username` -kt /keytab/password
	date
	sleep 6h
done
