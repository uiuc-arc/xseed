#!/usr/bin/env bash
find -name "setup.cfg" -exec rm -f {} \;
find -name "pytest.ini" -exec rm -f {} \;
LC_ALL=en_US.UTF-8 timeout 3600s pytest -v --continue-on-collection-errors &> $1/$2.txt
