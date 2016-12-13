import random

class Context():

    def __init__(self):
        #self.visible_set = []
        self.slots = []
        self.open_set = ["(", "["]
        self.closed_set = [")", "]"]
        self.matching = [("(", ")"), ("[", "]")]
        self.repick =1.0

    def choose_remaining(self, whichSet):
        leftToReturn = []
        for k in whichSet:
            if k not in self.slots:
                leftToReturn.append(k)
        return leftToReturn

    def find_all_matching(self,remaining):
        #takes a list of all remaining
        #parentheses to choose from
        #returns a subset of those, which match
        #things in slots
        all_poss = []
        for t in remaining:
            assert(t not in self.slots)
            matches = False
            for tup in self.matching:
                if t == tup[0]:
                    if tup[1] in self.slots:
                        all_poss.append(tup[1])
                elif t == tup[1]:
                    if tup[0] in self.slots:
                        all_poss.append(tup[0])
        return all_poss

    def find_match(self, m, remaining):
        #takes a parenthesis and a list of all
        #remaining items on the board
        #and returns None if there are no matches
        #and the match if it exists
        for r in remaining:
            if (m, r) in self.matching or (r, m) in self.matching:
                return r
        return None

    def find_outer_match(self, remaining):
        for s in self.slots:
            match = self.find_match(s, remaining)
            if match != None:
                return match
        return None

    def find_inner_match(self, remaining):
        best_match = None
        for s in self.slots:
            match = self.find_match(s, remaining)
            if match != None:
                best_match = match
        return best_match


    # what should we do when we already have picked?
    # for now just do nothing
    def pick_open(self, p=1.0):
        #p = probability of picking open
        #open_set = ["(", "["]
        #closed_set = [")", "]"]
        if random.random() < p:
            if random.random() < self.repick:
                leftToReturn = self.choose_remaining(self.open_set)
                if len(leftToReturn) > 0:
                    #what should we do when we already have picked?
                    #for now just do nothing
                    self.slots.append(leftToReturn[random.randint(0,len(leftToReturn) - 1)])
            else:
                self.slots.append(self.open_set[random.randint(0, len(self.open_set) - 1)])
        else:
            #self.slots.append(self.closed_set[random.randint(0,len(self.closed_set) - 1)])
            if random.random() < self.repick:
                leftToReturn = self.choose_remaining(self.closed_set)
                if len(leftToReturn) > 0:
                    # what should we do when we already have picked?
                    # for now just do nothing
                    self.slots.append(leftToReturn[random.randint(0, len(leftToReturn) - 1)])
            else:
                self.slots.append(self.closed_set[random.randint(0, len(self.closed_set) - 1)])

    def pick_closed(self, p=1.0):
        # p = probability of picking closed
        if random.random() < p:
            #self.slots.append(self.closed_set[random.randint(0, len(self.closed_set) - 1)])
            if random.random() < self.repick:
                leftToReturn = self.choose_remaining(self.closed_set)
                if len(leftToReturn) > 0:
                    # what should we do when we already have picked?
                    # for now just do nothing
                    self.slots.append(leftToReturn[random.randint(0, len(leftToReturn) - 1)])
            else:
                self.slots.append(self.closed_set[random.randint(0, len(self.closed_set) - 1)])

        else:
            #self.slots.append(self.open_set[random.randint(0, len(self.open_set) - 1)])
            if random.random() < self.repick:
                leftToReturn = self.choose_remaining(self.open_set)
                if len(leftToReturn) > 0:
                    # what should we do when we already have picked?
                    # for now just do nothing
                    self.slots.append(leftToReturn[random.randint(0, len(leftToReturn) - 1)])
            else:
                self.slots.append(self.open_set[random.randint(0, len(self.open_set) - 1)])

    def pick_random(self):
        all_paren = self.open_set + self.closed_set
        if random.random() < self.repick:
            leftToReturn = self.choose_remaining(all_paren)
        # p = probability of picking closed
            if len(leftToReturn) > 0:
                self.slots.append(leftToReturn[random.randint(0, len(leftToReturn) - 1)])
        else:
            self.slots.append(all_paren[random.randint(0, len(all_paren) - 1)])

    def pick_outer_match(self, p=1.0):
        # p = probability of picking open
        #open_set = ["(", "["]
        #closed_set = [")", "]"]
        leftToReturn = (self.choose_remaining(self.open_set) +
                        self.choose_remaining(self.closed_set))
        if random.random() < p or len(self.slots) == 0:
            if random.random() < self.repick:
                if len(leftToReturn) > 0:
                    match = self.find_outer_match(leftToReturn)
                    #assert (match != None)
                    if match != None:
                        self.slots.append(match)

            else:
                    # for i in leftToReturn
                raise "not Implemented!"

        else:
            # self.slots.append(self.closed_set[random.randint(0,len(self.closed_set) - 1)])
            if random.random() < self.repick:
                if len(leftToReturn) > 0:
                    self.slots.append(leftToReturn[random.randint(0, len(leftToReturn) - 1)])

            else:
                raise "not Implemented!"


    def pick_inner_match(self, p=1.0):
        # p = probability of picking open
        #open_set = ["(", "["]
        #closed_set = [")", "]"]
        leftToReturn = (self.choose_remaining(self.open_set) +
                        self.choose_remaining(self.closed_set))
        if random.random() < p or len(self.slots) == 0:
            if random.random() < self.repick:
                if len(leftToReturn) > 0:
                    match = self.find_inner_match(leftToReturn)
                    #assert (match != None)
                    if match != None:
                        self.slots.append(match)

            else:
                    # for i in leftToReturn
                raise "not Implemented!"

        else:
            # self.slots.append(self.closed_set[random.randint(0,len(self.closed_set) - 1)])
            if random.random() < self.repick:
                if len(leftToReturn) > 0:
                    self.slots.append(leftToReturn[random.randint(0, len(leftToReturn) - 1)])

            else:
                raise "not Implemented!"
