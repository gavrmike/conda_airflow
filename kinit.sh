#!/usr/bin/env bash

while true; do
	kinit `cat /keytab/username` -kt /keytab/keytab
	date
	sleep 6h
done
