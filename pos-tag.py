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
    labels = ['#', '$', '``', "''", '(', ')', ',', '--', '.', ':', 'CC', 'CD', 'DT',
              'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', '-LRB-', 'LS', 'MD', 'NN', 'NNP',
              'NNPS', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS',
              'RP', '-RRB-', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP',
              'VBZ', 'WDT', 'WP', 'WP$', 'WRB']
    min_prob = 1
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

            # Normalize type map
            for key, values in self.maps['typeMap'].iteritems():
                total = sum(values.itervalues())
                # Inner Map
                for type_succeed, count in values.iteritems():
                    # Normalize counts & cast to floats
                    count = float(count) / total
                    values[type_succeed] = count

            # Normalize word map
            for key, values in self.maps['wordMap'].iteritems():
                total = sum(values.itervalues())
                # Inner Map
                for word_succeed, count in values.iteritems():
                    # Normalize counts & cast to floats
                    count = float(count) / total
                    values[word_succeed] = count

            with open(datafile, 'w') as outfile:
                json.dump(self.maps, outfile)

        # Find min_prob
        for key, values in self.maps['typeMap'].iteritems():
            # Inner Map
            for type_succeed, count in values.iteritems():
                if values[type_succeed] < self.min_prob:
                    self.min_prob = values[type_succeed]

        # Find min_prob
        for key, values in self.maps['wordMap'].iteritems():
            # Inner Map
            for type_succeed, count in values.iteritems():
                if values[type_succeed] < self.min_prob:
                    self.min_prob = values[type_succeed]

        self.min_prob /= 10

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

    # Assigns a label to each observed word using the viterbi algorithm
    def viterbi_label(self, obs):
        V = [{}]
        for st in self.labels:
            if st in self.maps['wordMap'].keys() is not None:
                if obs[0] in self.maps['wordMap'][st].keys() is not None:
                    V[0][st] = {"prob": self.maps['wordMap'][st][obs[0]], "prev": None}
                else:
                    V[0][st] = {"prob": self.min_prob, "prev": None}
        # Run Viterbi when t > 0
        for t in range(1, len(obs)):
            V.append({})
            for st in self.labels:
                max_tr_prob = 0
                for prev_st in self.labels:
                    if(prev_st in V[t - 1].keys() is not None and prev_st in self.maps['typeMap'].keys() is not None and
                            st in self.maps['typeMap'][prev_st].keys() is not None):
                        max_tr_prob = max(max_tr_prob, V[t - 1][prev_st]["prob"] * self.maps['typeMap'][prev_st][st])
                for prev_st in self.labels:
                    if (prev_st in V[t - 1].keys() is not None and prev_st in self.maps['typeMap'].keys() is not None and
                            st in self.maps['typeMap'][prev_st].keys() is not None):
                        if V[t - 1][prev_st]["prob"] * self.maps['typeMap'][prev_st][st] == max_tr_prob:
                            if st in self.maps['wordMap'].keys() is not None:
                                if obs[t] in self.maps['wordMap'][st].keys() is not None:
                                    max_prob = max_tr_prob * self.maps['wordMap'][st][obs[t]]
                                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                                else:
                                    V[t][st] = {"prob": max_tr_prob * self.min_prob, "prev": prev_st}
                                break
        opt = []
        # The highest probability
        max_prob = max(value["prob"] for value in V[-1].values())
        previous = None
        # Get most probable state and its backtrack
        for st, data in V[-1].items():
            if data["prob"] == max_prob:
                opt.append(st)
                previous = st
                break
        # Follow the backtrack till the first observation
        for t in range(len(V) - 2, -1, -1):
            opt.insert(0, V[t + 1][previous]["prev"])
            previous = V[t + 1][previous]["prev"]
        print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob


if __name__ == '__main__':
    source = "training_dataset.txt"
    print "BiGram:"
    biGram = BiGram(source)
    biGram.generate_given("In", 50)

    print ""
    print "HMM:"
    hmm = HMM(source)
    #hmm.generate_given("In", "IN", 50)

    words = [[]]
    with open("2009-Obama.txt", 'r') as f:
        for line in f:
            for word in line.split():
                if word != '.':
                    words[-1].append(word)
                else:
                    words[-1].append('.')
                    words.append([])
    if len(words[-1]) == 0:
        words.pop()

    for sentence in words:
        print sentence
        hmm.viterbi_label(sentence)
