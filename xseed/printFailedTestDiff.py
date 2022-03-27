import sys
import re
from glob import  glob


def saveFailedFunctions(filename, failedTestDict):
    PYTEST_SUMMARY_SECTION_NAME = "short test summary info"
    END_SECTION = "===="
    END_OF_TEST_NAME_MARKER = " - "
    FAILED_TEST_MARKER = "FAILED"

    with open(filename, 'r') as file:
        line = " " 

        is_in_section = False
        # skip lines that are not part of the test summary section
        while(line != "" and not is_in_section):
            line = file.readline()
            if PYTEST_SUMMARY_SECTION_NAME in line:
                is_in_section = True

        # read in lines that are part of test summary section
        line = file.readline()
        while(line != "" and END_SECTION not in line):
            splitLine = line.split(' ')
            if(splitLine[0] != FAILED_TEST_MARKER):
                break
            
            failedTest = (' '.join(splitLine[1:])).split(END_OF_TEST_NAME_MARKER)[0]
            
            if failedTest in failedTestDict:
                failedTestDict[failedTest] += 1
            else:
                failedTestDict[failedTest] = 1
            line = file.readline()


def getTestStats(filename, test_error_dict):
    lines=open(filename, encoding='utf-8').readlines()
    sec=""
    curTest=""
    cur_err_msg=""
    cur_err_code=""

    is_in_or_past_FAILURES = False

    for l in lines:
        if l.startswith("===="):
            sec=" ".join(l.split(" ")[1:-1])

            if "FAILURES" in sec:
                is_in_or_past_FAILURES = True

        if is_in_or_past_FAILURES and "warnings summary" not in sec and "PASSES" not in sec and "ERRORS" not in sec and "short test summary info" not in sec:
            # TODO: check if test condition holds
            if l.startswith("___") and 'test' in l.lower():
                if len(curTest)>0:
                    if curTest not in test_error_dict:
                        test_errors=[]
                    else:
                        test_errors=test_error_dict[curTest]

                    test_errors.append((cur_err_msg, cur_err_code))
                    test_error_dict[curTest] = test_errors
                curTest=l.split(" ")[1].strip()
                cur_err_code=""
                cur_err_msg=""

            if l.startswith("E "):
                if len(cur_err_code) == 0:
                    cur_err_code=re.findall("[a-zA-Z]*Error|Timeout", l)
                    if len(cur_err_code) == 0:
                        # TODO: hacky way to capture asserts for now
                        if "assert" in l:
                            cur_err_code="AssertionError"
                        else:
                            cur_err_code = ""
                    else:
                        cur_err_code=cur_err_code[0]
                    cur_err_msg=l[1:].strip()

    # update last one
    if len(curTest) > 0:
        if curTest not in test_error_dict:
            test_errors = []
        else:
            test_errors = test_error_dict[curTest]

        test_errors.append((cur_err_msg, cur_err_code))
        test_error_dict[curTest] = test_errors
        #print(curTest)


error_dict=dict()
logdir=sys.argv[1]
files=glob(logdir+"/*txt")

failedTestDict = dict()

for file in files:
    #print(file)
    getTestStats(file, error_dict)

for t in error_dict.keys():
    print(t, end=",")
    print(len(error_dict[t]), end=",")
    failure_codes=set([x[1] for x in error_dict[t]])
    for c in failure_codes:
        print("{0}:{1}".format(c, len([x for x in error_dict[t] if x[1] == c])), end=",")
    print()
