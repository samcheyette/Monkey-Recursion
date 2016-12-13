from LOTlib.Grammar import Grammar

from context import Context
from LOTlib.Primitives import primitive
import random

#Context().__init__()

from LOTlib.Grammar import Grammar
@primitive
def if2_(x, y, z):
    if random.random() < x:
        return y
    else:
        return z

grammar = Grammar()

grammar.add_rule('START', '[%s]', ['op'], 1.0)
grammar.add_rule('START', '%s + [%s]', ['START', 'op'], 1.0)

#p = 0.9
grammar.add_rule('op', '%s.pick_open(p=%s)', ['C', 'PROB'], 1.0)
grammar.add_rule('op', '%s.pick_inner_match(p=%s)', ['C', 'PROB'], 1.0)

grammar.add_rule('op', '%s.pick_closed(p=%s)', ['C', 'PROB'], 1.0)
grammar.add_rule('op', '%s.pick_random()', ['C'], 1.0)
#grammar.add_rule('op', 'if2_', ['PROB', 'op', 'op'], 1.0)

probEqual1 = False
maxInt = 10

if probEqual1:
    grammar.add_rule('PROB', str(1.0), None, 1.0)
else:
    for p in xrange(int((maxInt+1)/2.0), maxInt+1):
        grammar.add_rule('PROB', str(p/float(maxInt)), None, 1.0)
#grammar.add_rule('prob', '0.9', '')
#grammar.add_rule('op', '%s.stop(%s)', ['C', 'INT'], 1.0)

#for i in xrange(6):
  #  grammar.add_rule('INT', str(i), None, 1.0)

grammar.renormalize()

from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Miscellaneous import nicelog

from LOTlib.Hypotheses.Likelihoods.StochasticLikelihood import StochasticLikelihood
import copy
from math import log, factorial
    # define a
class MyHypothesis(StochasticLikelihood, LOTHypothesis):
    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, grammar=grammar, display="lambda C: %s", **kwargs)


    def __call__(self): #, max_length=4):
        ret_vals = []
        C = Context()
        self.fvalue(C)
        ret = tuple(C.slots)
        return ret

    def compute_single_likelihood(self, datum, llcounts, sm=0.01):
        """
                sm smoothing counts are added to existing bins of counts
        """

        assert isinstance(datum.output,
                          dict), "Data supplied to SimpleGenerativeHypothesis must be a dict of function outputs to counts"

        z = float(sum(llcounts.values()))
        lklhd = 1.0
        ttl = 0
        denom = 1
        for k in datum.output.keys():
            resp = datum.output[k]
            ttl += resp
            denom += nicelog(factorial(resp))
            lklhd +=  nicelog((llcounts[k]/z)) * resp
            #print k, datum.output[k], llcounts[k]/z
        #print
        #print datum.output, self.value
        #print ttl, denom, lklhd
        return nicelog(factorial(ttl)) + lklhd - denom


if __name__ == "__main__":

    C = Context()
    C.slots = ["("]
    #C.pick_open()
    #C.pick_open()
    C.pick_inner_match(p=0.5)
    print C.slots