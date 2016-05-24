import random

class BiGram:

    wordMap = {}
    debug = True

    def __init__(self, source):
        previous = None
        with open(source, 'r') as f:
            for line in f:
                for word in line.split():
                    current = word.rpartition('_')[0]
                    #print current
                    if previous is not None:
                        if previous in self.wordMap.keys() is not None:
                            if current in self.wordMap[previous].keys() is not None:
                                self.wordMap[previous][current] += 1
                            else:
                                self.wordMap[previous][current] = 1
                        else:
                            self.wordMap[previous] = {current : 1}
                    previous = current

    '''
    This iterates through our wordmap. For each key it pulls out the associated map for that key. 
    We then iterate through our inner map and normalize our counts by dividing the current counts by the length of the inner map.
    '''
    def normalize_word_map(self):
        #Outer map.
        for key, values in self.wordMap.iteritems():
            #Inner Map
            for word_succeed, count in values.iteritems():
                #Normalize counts & cast to floats
                count = float(count) / float(len(values))
                values[word_succeed] = count   

    def generate_given(self, keyword, length):
        print "TODO"

if __name__ == '__main__':
    # Initialize GUI
    source = "training_dataset_small.txt"
    biGram = BiGram(source)
    biGram.normalize_word_map()
    biGram.generate_given("hello", 10)