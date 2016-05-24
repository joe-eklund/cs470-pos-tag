import random
import sys
import json
import os.path


class BiGram:

    wordMap = {}
    debug = True

    # Initialize Bi-Gram
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

    # Generate text using the map
    def generate_given(self, keyword, length):
        sys.stdout.write(keyword + " ")
        if keyword in self.wordMap.keys():
            while length > 0:
                next_word = self.weighted_pick(self.wordMap[keyword])
                keyword = next_word
                sys.stdout.write(keyword + " ")
                length -= 1
                if length % 10 == 0:
                    sys.stdout.write("\n")

    # Randomly selects key based on a weight
    def weighted_pick(self, d):
        r = random.uniform(0, sum(d.itervalues()))
        s = 0.0
        for k, w in d.iteritems():
            s += w
            if r < s: return k
        return k


class HMM:

    maps = {'typeMap' : {}, 'wordMap' : {}}
    debug = True

    # Initialize HMM
    def __init__(self, source):
        datafile = 'hmm_data.txt'

        if os.path.isfile(datafile):
            with open(datafile, 'r') as infile:
                self.maps = json.load(infile)
        else:
            previous = None
            prev_type = None
            with open(source, 'r') as f:
                for line in f:
                    for word in line.split():
                        current = word.rpartition('_')[0]
                        cur_type = word.rpartition('_')[2]
                        if prev_type is not None:
                            if prev_type in self.maps['typeMap'].keys() is not None:
                                if cur_type in self.maps['typeMap'][prev_type].keys() is not None:
                                    self.maps['typeMap'][prev_type][cur_type] += 1
                                else:
                                    self.maps['typeMap'][prev_type][cur_type] = 1
                            else:
                                self.maps['typeMap'][prev_type] = {cur_type : 1}

                            if cur_type in self.maps['wordMap'].keys() is not None:
                                if current in self.maps['wordMap'][cur_type].keys() is not None:
                                    self.maps['wordMap'][cur_type][current] += 1
                                else:
                                    self.maps['wordMap'][cur_type][current] = 1
                            else:
                                self.maps['wordMap'][cur_type] = {current : 1}
                        prev_type = cur_type

            with open(datafile, 'w') as outfile:
                json.dump(self.maps, outfile)

    # Generate text using the map
    def generate_given(self, keyword, word_type, length):
        sys.stdout.write(keyword + " ")
        if word_type in self.maps['typeMap'].keys():
            while length > 0:
                next_type = self.weighted_pick(self.maps['typeMap'][word_type])
                next_word = self.weighted_pick(self.maps['wordMap'][next_type])
                word_type = next_type
                keyword = next_word
                sys.stdout.write(keyword + " ")
                length -= 1
                if length % 10 == 0:
                    sys.stdout.write("\n")

    # Randomly selects key based on a weight
    def weighted_pick(self, d):
        r = random.uniform(0, sum(d.itervalues()))
        s = 0.0
        for k, w in d.iteritems():
            s += w
            if r < s: return k
        return k


if __name__ == '__main__':
    source = "training_dataset.txt"
    print "BiGram:"
    biGram = BiGram(source)
    biGram.generate_given("In", 50)

    print ""
    print "HMM:"
    hmm = HMM(source)
    hmm.generate_given("In", "IN", 50)
