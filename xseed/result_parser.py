from parsimonious.grammar import Grammar
from parsimonious.grammar import NodeVisitor
grammar = Grammar('''
str = pat results in fulltime  pat
results = sresult (sep sresult)*
sresult = count result
sep = "," _
result = ~"failed|skipped|xpassed|passed|warnings|warning|errors|error|reruns|rerun|xfailed|xfail" _
in = "in" _
pat = "="+ _
fulltime = time frac?
count = ~"[0-9]+"  _
frac = ~"\([0-9:]+\)" _
time =  ~"[0-9.]+" _ ~"(seconds)|s|h|m" _
_  = ~"\s*"

''')


class MyVisitor(NodeVisitor):
    def __init__(self):
        self.results = dict()
        self.results['failed'] = 0
        self.results['passed'] = 0

    def visit_sresult(self, node, visited_children):
        self.results[node.children[1].text.strip()] = int(node.children[0].text)
        return node

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node


def parse_line(line):
    t = grammar.parse(line)
    m = MyVisitor()
    m.visit(t)
    return m.results

