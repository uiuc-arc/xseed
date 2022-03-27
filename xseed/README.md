# flakyPieScripts

#### Scripts to help with the detection and analysis of nondeterministic tests used in various open source Python libraries


## remove_seed_setting.sh
#### Usage 
`./remove_seed_setting.sh [dir name] [file to save output]`

#### Description 
comments out lines containing the word `seed` (capitalization does not matter) in python files

## general_conda_setup.sh
#### Usage
`./general_conda_setup.sh [path to miniconda3/anaconda3 dir] [dir] [github repo url]`

#### Description 
clones a github repo and sets up a conda environment

#### Note
assumes github repo url in form of `https://github.com/USER/PROJECT.git`

## run_tests.sh
#### Usage
`./run_tests.sh [dir name] [name of conda env] [number of times to run tests]`

#### Description
runs the command `pytest tests` the specified number of times and saves output to files (using a timestamp as a unique identifier)

## run_test_file.sh
#### Usage
`./run_test_file.sh [dir name] [name of conda env] [number of times to run tests] [full path to test command file]`

#### Description
runs the test command file the specificed number of times and saves output into text files (named for their run numbers) stored in a directory (using a timestamp as a unique identifier)

## general_run_tests.sh
#### Usage
`./general_run_tests.sh [dir name] [name of conda env] [name of tests dir] [number of times to run tests] [name of output text file (without extension)] [path to miniconda3/anaconda3 dir] [full path to test command file]`

#### Description
runs the test command file the specified number of times and saves output to files (using a timestamp as a unique identifier)

## printFailedTestDiff.py
#### Usage
`python3 printFailedTestDiff.py [all results files]`

#### Description
parses pytest results to determine which tests fail nondeterministically and prints results

#### Note
recommended method of running the program is to move into the directory containing pytest result files and run `ls | xargs python3 /path/to/printFailedTestDiff.py`

## failedTestDiff.py
#### Usage
`python3 failedTestDiff.py [all results files]`

#### Description
parses pytest results to determine which tests fail nondeterministically and outputs CSV containing results

#### Note
recommended method of running the program is to move into the directory containing pytest result files and run `ls | xargs python3 /path/to/failedTestDiff.py`
