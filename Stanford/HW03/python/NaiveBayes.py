# NLP Programming Assignment #3
# NaiveBayes
# 2012

#
# The area for you to implement is marked with TODO!
# Generally, you should not need to touch things *not* marked TODO
#
# Remember that when you submit your code, it is not run from the command line
# and your main() will *not* be run. To be safest, restrict your changes to
# addExample() and classify() and anything you further invoke from there.
#


import sys
import getopt
import os
import math
import collections
import string

class NaiveBayes:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test.
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.stopList = set(self.readFile('../data/english.stop'))
    self.numFolds = 10
    
    # count the number of each type of classes
    self.classes = collections.defaultdict(lambda: 0)
    # count( w_i, c_j )
    self.nbLikehood = collections.defaultdict(lambda: 0)
    # count the total number of all classes
    self.totalClassNum = 0
    # count the vacabulary of all words in all the classes
    self.vocabulary = collections.defaultdict(lambda: 0)
    # count( w, c_j ) the total number of words in each class
    self.total_count_per_class = collections.defaultdict(lambda: 0)

  #############################################################################
  # TODO TODO TODO TODO TODO

  def classify(self, words):
    """ TODO
      'words' is a list of words to classify. Return 'pos' or 'neg' classification.
    """
    classType = ''
    
    # print self.classes['pos'], self.classes['neg']
    # print self.classes['pos'] + self.classes['neg']
    # print self.totalClassNum
    # self.totalClassNum == self.classes['pos'] + self.classes['neg']
    
    self.totalClassNum = self.classes['pos'] + self.classes['neg']
    prob_prior_pos = float(self.classes['pos']) / float(self.totalClassNum)
    prob_prior_neg = float(self.classes['neg']) / float(self.totalClassNum)
    # print prob_prior_pos
    # print prob_prior_neg
    prob_pos = 0
    prob_neg = 0
    for word in words:
        type = 'pos'
        count_word_class = self.nbLikehood[(word, type)]
        count_totalword_class = self.total_count_per_class[type]
        # Do the add-1 smoothing
        prob_pos += math.log( (count_word_class + 1.0) / (count_totalword_class + len(self.vocabulary)) )
        
        type = 'neg'
        count_word_class = self.nbLikehood[(word, type)]
        count_totalword_class = self.total_count_per_class[type]
        prob_neg += math.log( (count_word_class + 1.0)/(count_totalword_class + len(self.vocabulary)) )
    
    prob_pos += math.log(prob_prior_pos)
    prob_neg += math.log(prob_prior_neg)
    
    if prob_pos - prob_neg > 0 :
        classType = 'pos'
    else :
        classType = 'neg'

    return classType


  def addExample(self, klass, words):
    """
     * TODO
     * Train your model on an example document with label klass ('pos' or 'neg') and
     * words, a list of strings.
     * You should store whatever data structures you use for your classifier
     * in the NaiveBayes class.
     * Returns nothing
    """

    self.classes[klass] += 1
    # self.totalClassNum += 1
    for word in words:
        self.vocabulary[word] += 1
        self.nbLikehood[(word, klass)] += 1
        self.total_count_per_class[klass] += 1

    pass

  def filterStopWords(self, words):
    """
    * TODO
    * Filters stop words found in self.stopList.
    """
    filtered = []
    
    for word in words :
        if not word in self.stopList and word.strip() != '':
            filtered.append(word)
    
    return words

  # TODO TODO TODO TODO TODO
  #############################################################################


  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here,
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    # transper contents from list to string then do the split
    result = self.segmentWords('\n'.join(contents))
    # print result
    return result


  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()


  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    
    print posTrainFileNames
    
    for fileName in posTrainFileNames:
      # print fileName
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split

  def train(self, split):
    for example in split.train:
      words = example.words
      # Initial FILTER_STOP_WORDS = False
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      self.addExample(example.klass, words)

  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = []
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
    return splits


  def test(self, split):
    """Returns a list of labels for split.test."""
    labels = []
    for example in split.test:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      guess = self.classify(words)
      labels.append(guess)
    return labels

  def buildSplits(self, args):
    """Builds the splits for training/testing"""
    trainData = []
    testData = []
    # splits is a list
    splits = []
    trainDir = args[0]
    if len(args) == 1:
      print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (self.numFolds, trainDir)

      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      
      # print posTrainFileNames
      for fold in range(0, self.numFolds):
                
        split = self.TrainSplit()
        
        for fileName in posTrainFileNames:
          # print fileName
          example = self.Example()
          example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
          example.klass = 'pos'
          if fileName[2] == str(fold):  # fileName : cv543_5045.txt fileName[2] = '5'
            split.test.append(example)
          else:
            split.train.append(example)  
        for fileName in negTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
          example.klass = 'neg'
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        # In k-fold cross validation set : 
        # splits includes splits[0] / splits[1] / ... / splits[10] 
        splits.append(split)
    
    elif len(args) == 2:  # NO K-fold cross validation 
      split = self.TrainSplit()
      testDir = args[1]
      print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        split.train.append(example)

      posTestFileNames = os.listdir('%s/pos/' % testDir)
      negTestFileNames = os.listdir('%s/neg/' % testDir)
      for fileName in posTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (testDir, fileName))
        example.klass = 'pos'
        split.test.append(example)
      for fileName in negTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (testDir, fileName))
        example.klass = 'neg'
        split.test.append(example)
      # No k-fold cross validation : splits only includes splits[0]
      splits.append(split)
    
    return splits

def main():
  nb = NaiveBayes()

  # default parameters: no stop word filtering, and
  # training/testing on ../data/imdb1
  if len(sys.argv) < 2:
      options = [('','')]
      args = ['../data/imdb1/']
  else:
      (options, args) = getopt.getopt(sys.argv[1:], 'f')
  if ('-f','') in options:
    nb.FILTER_STOP_WORDS = True

  splits = nb.buildSplits(args)
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    # split form splits[0] - splits[9]
    classifier = NaiveBayes()
    accuracy = 0.0
    for example in split.train:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words =  classifier.filterStopWords(words)
      # addExample is the process for Building the Model
      # Use the Training data (Document with label klass('pos' or 'neg') and words )
      # Train the Model on the Training data
      # Store the data structures used for classifier in NaiveBayes class 
      classifier.addExample(example.klass, words)

    for example in split.test:
      words = example.words
      if nb.FILTER_STOP_WORDS:
        words =  classifier.filterStopWords(words)
      # classify is the process for Predicting Based on the Model
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0

    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
    fold += 1
  
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy

if __name__ == "__main__":
    main()
