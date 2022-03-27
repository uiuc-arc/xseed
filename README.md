## XSEED

This repository contains the implementation for our tool, XSEED, and other experimental data from our paper: [To Seed or Not to Seed?
An Empirical Analysis of Usage of Seeds for Testing in Machine Learning Projects](https://saikatdutta.web.illinois.edu/papers/seeds-icst22.pdf) 
published at ICST 2022 conference.

Our source has been evaluated using Ubuntu 18.04 64 bit system. Running them on other OSes may need additional steps.

## Tool Details 

### Installation

1. Clone the repository 
2. XSEED needs Python 3.6+. Install dependencies: `pip install -r requirements`
3. Cd into repository. Create projects directory: `mkdir -p projects` 

### Running tests and collecting info

The script `xseed/run_seed_all.sh` takes the `github slug`, `number of times each test` (N), and `number of parallel
threads` (K) as inputs. Then it performs the following steps:
1. Clone the github repo and install it in a new conda environment. It uses the 
`xseed/general_setup.sh` script to install each project.
The project will be setup in `projects` folder.
2. Run each test N times using K threads (both with and without seeds). The script
`xseed/remove_seeds_script.py` removes seed setting APIs from a given project and
creates a new branch.
3. Collect all test results and create a report

The reports will be created in `projects/[projectname]/final_report_and_logs_for_test_runs_[projectname]_` folder.
It will contain `[projectname]_[uniqueid]_wseed` folder containing pytest logs of running
the tests with seed and  `[projectname]_[uniqueid]_woseed` folder containing pytest logs of 
running the tests *without* seeds. Finally, the `final_report_for_test_runs_[projectname]_` file
will contain the list of tests that failed without seeds but passed with seeds 
(with error types and frequencies). 


Note: This script requires `sudo` access to install system dependencies. 
If you don't have sudo access, change `global` to `local` on line 69 in `run_seed_all.sh`.  

The details of the projects that we evaluated are in `projectdata.csv` 

## Experiment data

**Project Data**: The details of the projects that we evaluated are in `projectdata.csv`

**Pull Requests and Issues**: `prs.csv` contains the list of all Pull Requests or Issues that
we sent and their links, current status, and fix type

**Test results**: `project_test_result_summary.txt` contains the lists of tests that fail without seeds across
all projects

**Project Stats and Topics**: Use `python topics.py` to get a summary of all topics and project
stats. This requires installing pandas.

**Full test execution logs of each Project**: This step help download all experimental data and generate Table 2 in the paper. Steps:
1. Download full experiment data from [https://zenodo.org/record/6388114](Zenodo).
2. Extract each logs_*.gz file inside the folder.
3. Run `python failedTestsParser.py [root of downloaded folder]`. This will generate table 2. Note that this may take several minutes.

### Citing our work

If you use our tool our any technique from our paper, cite us using:
```
@inproceedings{dutta2022seeds,
  title={To Seed or Not to Seed? An Empirical Analysis of Usage of Seeds for Testing in Machine Learning Projects},
  author={Dutta, Saikat and Arunachalam, Anshul and Misailovic, Sasa},
  booktitle={ICST},  
  year={2022}
}

```






