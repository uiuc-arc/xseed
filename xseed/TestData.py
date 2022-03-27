class LibData:
    def __init__(self):
        self.tests = 0
        self.runs = 0
        self.timeouts = 0
        self.logdata = list()
        self.testdata_w_seed = dict()
        self.testdata_wo_seed = dict()


class LogData:
    def __init__(self):
        self.result_summary = dict()


class TestData:
    def __init__(self):
        self.testname = None
        self.classname = None
        self.filename = None
        self.passed = 0
        self.failed = 0
        self.other = 0
        self.failure_types = dict()
        self.assertion_failures = dict() # map from assertion type to num failures
