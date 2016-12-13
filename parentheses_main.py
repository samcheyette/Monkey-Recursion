from LOTlib.DataAndObjects import FunctionData
from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
from model_parentheses import *
from LOTlib.TopN import TopN
from collections import Counter
from LOTlib.Miscellaneous import logsumexp, qq
from math import exp, log

def isValidCenterEmbed(parens):
    if len(parens) == 0:
        return True
    else:
        if (((parens[0], parens[len(parens) - 1]) not in Context().matching)
            or parens[0] in parens[1:] or parens[len(parens) - 1] in parens[:len(parens) - 1]):
            return False
        else:
            return isValidCenterEmbed(parens[1:len(parens)-1])

def simulateData(parens, randomValidLsts = [], pC=1.0,pT=0.0, N=12):
    allParens = {}
    for i in xrange(len(parens)):
        for j in xrange(len(parens)):
            for k in xrange(len(parens)):
                for l in xrange(len(parens)):
                    ps = (parens[i], parens[j], parens[k], parens[l])
                    if isValidCenterEmbed(ps):
                        allParens[ps] = int((pC / 2.0) * N)

                    elif pC < 1.0 and ps in randomValidLsts:
                        allParens[ps] = int((pT/float((len(randomValidLsts)))) * N)
                    elif pC + pT < 1.0:
                        allParens[ps] = int((1.0 - pT - pC) * N)


    return allParens


def run(data, TOP=100, STEPS=1000):
    #if LOTlib.SIG_INTERRUPTED:
      #  return ""
    #data = [FunctionData(input=(), output={lst: len(lst)})]
    h0 = MyHypothesis()
    tn = TopN(N=TOP)
    # run the sampler
    counter = Counter()
    for h in MHSampler(h0, data, steps=STEPS, acceptance_temperature=1.0, likelihood_temperature=1.0):#, likelihood_temperature=10.0):
        # counter[h] += 1
        tn.add(h)

    z = logsumexp([h.posterior_score for h in tn])
    sort_post_probs = [(h, exp(h.posterior_score - z)) for h in tn.get_all(sorted=True)][::-1]
    return sort_post_probs


def main():


    lst = ["(", "[", "]", ")"]
    randomTstLists = [("(", ")", "[", "]"), ("[", "]", "(", ")")]

    #d will simulate N participants who center embed correctly at rate pC,
    #tail embed at rate pT and do something else the rest of the time
    #FINISH THIS!!!
    d = simulateData(lst, randomTstLists, pC=0.4, pT=0.6, N=500)
    for k in d.keys():
        print d, d[k]

    data = [ FunctionData(input=(), output=d, alpha=0.9) ]
    r = run(data, TOP=5, STEPS=5000)
    for i in r:
        print i
        print i[0](), i[0](), i[0]()

if __name__ == "__main__":

    main()




def some_stuff():


    #simulate some data with high probability of
    #center embedding
    #and a lower probability of tail recursion
    lst = ["(", "[", "]", ")"]
    randomTstLists = [("(", ")", "[", "]"), ("[", "]", "(", ")")]
    d = simulateData(lst, randomTstLists, p=1.0, N=12)

    for k in d.keys():
        if d[k] > 0.0:
            print k, d[k]
    print len(d)

    #print isValidCenterEmbed(("(", "]"))
    #print isValidCenterEmbed(('(', '(', ')', ']'))

    data = [ FunctionData(input=(), output=d, alpha=0.9) ]
    h0 = MyHypothesis()
    from numpy import exp
    for h in MHSampler(h0, data, steps=5000):
        None
        #exp(h.compute_likelihood(data)) > 0.0 or
        y = h()
        #print h, y
        if isValidCenterEmbed(y):
            #print "hello"
            #None
            print exp(h.compute_posterior(data)), h, y#, isValidCenterEmbed(y)
        #else:
           # print h.compute_likelihood(data), h, y