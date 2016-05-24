import random
import sys
import json
import os.path

class BiGram:

    wordMap = {}
    debug = True

    def __init__(self, source):
        datafile = 'bigram_data.txt'

        if os.path.isfile(datafile):
            with open(datafile, 'r') as infile:
                self.wordMap = json.load(infile)
        else:
            previous = None
            with open(source, 'r') as f:
                for line in f:
                    for word in line.split():
                        current = word.rpartition('_')[0]
                        if previous is not None:
                            if previous in self.wordMap.keys() is not None:
                                if current in self.wordMap[previous].keys() is not None:
                                    self.wordMap[previous][current] += 1
                                else:
                                    self.wordMap[previous][current] = 1
                            else:
                                self.wordMap[previous] = {current : 1}
                        previous = current

            with open(datafile, 'w') as outfile:
                json.dump(self.wordMap, outfile)

    def generate_given(self, keyword, length):
        sys.stdout.write(keyword + " ")
        if keyword in self.wordMap:
            while(length > 0):
                ran = random.random()
                #Still need to use random variable to select next word. Currently just grabs the next word in map.
                next_word = self.weighted_pick(self.wordMap[keyword])
                keyword = next_word
                sys.stdout.write(keyword + " ")
                length -= 1
                if length % 10 == 0:
                    sys.stdout.write("\n")

    def weighted_pick(self, d):
        r = random.uniform(0, sum(d.itervalues()))
        s = 0.0
        for k, w in d.iteritems():
            s += w
            if r < s: return k
        return k

if __name__ == '__main__':
    source = "training_dataset.txt"
    biGram = BiGram(source)
    biGram.generate_given("In", 50)