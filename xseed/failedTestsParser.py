import argparse
import sys
import re
from glob import glob

from TestData import LibData, LogData, TestData
from result_parser import parse_line
import re
import numpy as np


def saveFailedFunctions(filename, failedTestDict):
    PYTEST_SUMMARY_SECTION_NAME = "short test summary info"
    END_SECTION = "===="
    END_OF_TEST_NAME_MARKER = " - "
    FAILED_TEST_MARKER = "FAILED"

    with open(filename, 'r') as file:
        line = " "

        is_in_section = False
        # skip lines that are not part of the test summary section
        while (line != "" and not is_in_section):
            line = file.readline()
            if PYTEST_SUMMARY_SECTION_NAME in line:
                is_in_section = True

        # read in lines that are part of test summary section
        line = file.readline()
        while (line != "" and END_SECTION not in line):
            splitLine = line.split(' ')
            if (splitLine[0] != FAILED_TEST_MARKER):
                break

            failedTest = (' '.join(splitLine[1:])).split(END_OF_TEST_NAME_MARKER)[0]

            if failedTest in failedTestDict:
                failedTestDict[failedTest] += 1
            else:
                failedTestDict[failedTest] = 1
            line = file.readline()


def general_stats_parser(filename):
    pattern = re.compile(
        "=+ ([0-9]+ (failed|xpassed|rerun|passed|skipped|warnings|errors|error|xfailed|xfail|warning)(, )?)+ in [0-9.]+[ ]*(m|h|s|(seconds))( [0-9:()]+)? =+")
    lines = open(filename, encoding='utf-8').readlines()
    f = False
    result_numbers = dict()
    for l in lines[::-1]:
        r = re.match(pattern, l)
        if r is not None:
            result_numbers = parse_line(r.group(0))
            f = True
            break

    if not f:
        return None
    return result_numbers


def getTestStats(filename, test_error_dict):
    lines = open(filename, encoding='utf-8').readlines()
    sec = ""
    curTest = ""
    cur_err_msg = ""
    cur_err_code = ""

    is_in_or_past_FAILURES = False
    cur_file_tests = dict()
    for l in lines:
        if l.startswith("="):
            sec = " ".join(l.split(" ")[1:-1])

            if "FAILURES" in sec:
                is_in_or_past_FAILURES = True

        if is_in_or_past_FAILURES and "warnings summary" not in sec and "PASSES" not in sec and "ERRORS" not in sec and "short test summary info" not in sec:
            if l.startswith("_") and 'test' in l.lower():
                if len(curTest) > 0:
                    if curTest not in test_error_dict:
                        test_errors = TestData()
                    else:
                        test_errors = test_error_dict[curTest]

                    test_errors.failure_types[cur_err_code] = test_errors.failure_types.get(cur_err_code, 0) + 1
                    test_error_dict[curTest] = test_errors
                curTest = " ".join(l.split(" ")[1:-1]).strip()  # re-check
                curTest = re.sub("0x[a-zA-Z0-9]+>", "", curTest)
                cur_err_code = ""
                cur_err_msg = ""
                full_test_id  = ""
            if len(curTest)> 0 and l.startswith("self =") and "testMethod" in l:
                try:
                    full_test_id_snip = l[7:][1:-1]
                    prefix=full_test_id_snip.split(" ")[0]
                
                    testname = full_test_id_snip.split("testMethod=")[1]
                    full_test_id = prefix + "." + testname
                    full_test_id = re.sub("0x[a-zA-Z0-9]+>", "", full_test_id)
                    if len(full_test_id) > 0:
                        test_error_dict[full_test_id] = test_error_dict.get(full_test_id, test_error_dict.get(curTest, TestData()))
                        test_error_dict.pop(curTest, None)
                        curTest = full_test_id
                except:
                    import traceback as tb
                    tb.print_exc()
                    print("Error", filename)
                    break
               

            if re.match("([a-zA-Z_-]*/)*[a-zA-Z0-9_\.-]*:[0-9]+:", l) and len(full_test_id)==0 and len(curTest)>0:
                full_test_id=l.split(":")[0] + ":" + curTest
                test_error_dict[full_test_id] = test_error_dict.get(full_test_id, test_error_dict.get(curTest, TestData()))
                test_error_dict.pop(curTest, None)
                curTest = full_test_id
                

            if l.startswith("E "):
                if len(cur_err_code) == 0:
                    cur_err_code = re.findall("[a-zA-Z]*Error|Timeout|Exception|BadZipFile", l)
                    if len(cur_err_code) == 0:
                        if "assert" in l:
                            cur_err_code = "AssertionError"
                        else:
                            cur_err_code = ""
                    else:
                        cur_err_code = cur_err_code[0]
                    cur_err_msg = l[1:].strip()

    # update last one
    if len(curTest) > 0:
        if curTest not in test_error_dict:
            test_errors = TestData()
        else:
            test_errors = test_error_dict[curTest]
        test_errors.failure_types[cur_err_code] = test_errors.failure_types.get(cur_err_code, 0) + 1
        test_error_dict[curTest] = test_errors


def parseDir(files, libdata):
    test_dict = dict()
    for file in files:
        logdata = LogData()
        logdata.result_summary = general_stats_parser(file)
        if logdata.result_summary is None:
            libdata.timeouts += 1
            continue
        libdata.runs += 1
        total_failed = logdata.result_summary['failed']

        getTestStats(file, test_dict)
    
    return test_dict



def getTable(main_log_dir):
    import os
    import pickle
    all_dirs = glob(main_log_dir+"/final*")
    projectdata = dict()
    for d in all_dirs:        
        projectname = "_".join(d.split("/")[-1].split("_")[7:])
        print(projectname)
        binfile = d+"/"+projectname + ".pkl"
        binfile='r'
        if os.path.exists(binfile):
            with open(binfile, 'rb') as f:
                libdata = pickle.load(f)
            if libdata.timeouts == 0:
                woseed_files = glob(d + "/*woseed/*txt")
                result_summary = general_stats_parser(woseed_files[0])

                libdata.tests = result_summary['passed'] + result_summary['failed']                
        else:
            wseed_files = glob(d + "/*wseed/*txt")
            woseed_files = glob(d + "/*woseed/*txt")
            libdata = LibData()
            libdata.testdata_w_seed = parseDir(wseed_files, libdata)
            libdata.testdata_wo_seed = parseDir(woseed_files, libdata)
            with open(binfile, 'wb') as f:
                pickle.dump(libdata, f)
        projectdata[projectname] = libdata

    totalproj = 0
    totaltests = 0
    totalws = 0
    totalwos = 0
    totaluniq = 0
    totalzerofifty=0
    totalfiftyhundred = 0
    totalfailurerates = []
    for p in sorted(projectdata.keys()):
        if projectdata[p].timeouts > 0:
            continue
        tests = projectdata[p].tests
        wseedfailed = len(projectdata[p].testdata_w_seed)
        woseedfailed = len(projectdata[p].testdata_wo_seed)
        faileduniq = [k for k in projectdata[p].testdata_wo_seed if k not in projectdata[p].testdata_w_seed]
        
        if len(faileduniq) > 0:
            failurerates = [sum(projectdata[p].testdata_wo_seed[k].failure_types.values())/500 for k in faileduniq]            
            zerotofifty = len([k for k in failurerates if k < 0.50])
            morethanfifty = len([k for k in failurerates if k >= 0.50])
            print("{0}&{1}&{2}&{3}&{4}&{5:.2f}\\% ($\\pm${6:.2f})&{7}&{8}\\\\".format(p[:-1], tests, wseedfailed, woseedfailed, len(faileduniq), np.mean(failurerates)*100, np.std(failurerates), zerotofifty, morethanfifty))
        else:
            #print("{0}&{1}&{2}&{3}&{4}&{5}&{6}&{7}".format(p, tests, wseedfailed, woseedfailed, len(faileduniq), "-", "-", "-", "-"))
            continue
        totalproj+=1
        totaltests+=tests
        totalws+=wseedfailed
        totalwos+=woseedfailed
        totaluniq+=len(faileduniq)
        totalzerofifty+=zerotofifty
        totalfiftyhundred+=morethanfifty
        totalfailurerates+=failurerates
    print("\\midrule")
    print("\\textbf{{Total/Avg}} ({0} projects)&{1}&{2}&{3}&{4}&{5:.2f}&{6}&{7}\\\\".format(totalproj, totaltests, totalws, totalwos, totaluniq, np.mean(totalfailurerates)*100, totalzerofifty, totalfiftyhundred))
            

    
if __name__ == '__main__':
    basedir = sys.argv[1]
    getTable(sys.argv[1])




        

