# Python script to process the .txt book files into python data structs
book_name = "../data/agot"
print "Song of Ice and Fire Data Analysis:%s" % book_name

# First we need to open the book and store all of the words into an array
buff = "%s_f.txt" % book_name
b_file = open(buff)

book = []

for s in b_file:
  v = s.split()
  for i in v:
    book.append(i)
  
# Make 2 dictionaries 
 # key:chars -> val:community
 # key:chars -> val:nicknames

c_file = open("chars_final.txt")

char_house = {}
char_alias = {}
char = []
alias_list = []

for s in c_file:
  v = s.split(";");
  v[0] = v[0].strip()
  v[1] = v[1].strip()
  
  char_house[v[1]] = v[0];
  char.append(v[1])

  fl = v[1].split();
  first = fl[0];

  alias = v[2].split(",")
  for i in range(0,len(alias)):
    alias[i] = alias[i].strip()
    alias_list.append(alias[i])

  char_alias[v[1]] = alias;
  char_alias[v[1]].append(first)
  alias_list.append(first)

# Iterate through the book
# Create a list recording the appearences of characters

book_vec = [-1]*len(book)

for i in range(0, len(book)):
  for j in range(0, len(char)):
    if (book[i] in char_alias[char[j]]):
      book_vec[i] = j

#print book_vec

def weighted_graph(book_vec, char_house):
  # Create a graph by going through the book_vec and creating edges when characters appear within 50 words of eachother.

  import networkx as nx
  ng = nx.Graph()

  z_vec = [-1]*25;
  book_vec = book_vec + z_vec;

  for i in range(0, len(book_vec) - 25):
    if (book_vec[i] > -1):
      for j in range(i, i + 25):
        if (book_vec[j] > -1):
          sub = char[book_vec[i]]
          tar = char[book_vec[j]]
           
          if sub == tar:
            continue

          # Check for the subject node in the graph
          if sub in ng:
            ng.node[sub]['weight'] += 1
          else:
            ng.add_node(sub, weight = 1, house = char_house[sub])

          # Check for the target node in the graph
          if tar in ng:
            ng.node[tar]['weight'] += 1
          else:
            ng.add_node(tar, weight = 1, house = char_house[tar])

          # Check for the edge in the graph
          if ng.has_edge(sub, tar):
            ng[sub][tar]['weight'] += 1
          else:
            ng.add_edge(sub, tar, weight = 1)

  buff = "%s_weighted.graphml" % book_name
  nx.write_graphml(ng, buff)
  buff = "%s_weighted.gexf" % book_name
  nx.write_gexf(ng, buff)

def multi_graph(book_vec, char_house):
  # Create a graph by going through the book_vec and creating edges when characters appear within 100 words of eachother.

  import networkx as nx
  ng = nx.MultiGraph()

  z_vec = [-1]*25;
  book_vec = book_vec + z_vec;

  for i in range(0, len(book_vec) - 25):
    if (book_vec[i] > -1):
      for j in range(i, i + 25):
        if (book_vec[j] > -1):
          sub = char[book_vec[i]]
          tar = char[book_vec[j]]
          
          if sub == tar:
            continue

          # Check for the subject node in the graph
          if sub in ng:
            ng.node[sub]['weight'] += 1
          else:
            ng.add_node(sub, weight = 1, house = char_house[sub])

          # Check for the target node in the graph
          if tar in ng:
            ng.node[tar]['weight'] += 1
          else:
            ng.add_node(tar, weight = 1, house = char_house[tar])

          ng.add_edge(sub, tar, time = i, key = i)
  
  #buff = "%s_multi.graphml" % book_name
  #nx.write_graphml(ng, buff)
  print ng.number_of_edges()
  buff = "%s_multi.gexf" % book_name
  nx.write_gexf(ng, buff)

# multi_graph(book_vec, char_house)

def remove_stop_words(book, char, alias_list):
  # Remove all the stop words from a file

  book_s = []

  file_name = "words"
  w_file = open(file_name)

  words = []
  for s in w_file:
    v = s.split()
    for i in v:
      words.append(i)

  for s in book:
    v = s.split();
    for i in v:
      if (i not in alias_list):
        i = i.lower()
      if (i not in words):
        book_s.append(i)

  book = book_s

  return book

book = remove_stop_words(book,char, alias_list)

# Machine Learning Implementation
def bayes(book, char, char_alias):

  import re
  import math
  import string

  class classifier:
    def __init__(self,getfeatures,filename=None):
      # Counts of feature/category combinations
      self.fc={}
      # Counts of documents in each category
      self.cc={}
      self.getfeatures=getfeatures
      self.thresholds={}
          
    # Increase the count of a feature/category pair
    def incf(self,f,cat):
      self.fc.setdefault(f,{})
      self.fc[f].setdefault(cat,0)
      self.fc[f][cat]+=1

    # Increase the count of a category
    def incc(self,cat):
      self.cc.setdefault(cat,0)
      self.cc[cat]+=1

    # The number of times a feature has appeared in a category
    def fcount(self,f,cat):
      if f in self.fc and cat in self.fc[f]:
        return float(self.fc[f][cat])
      return 0.0

    # The number of items in a category
    def catcount(self,cat):
      if cat in self.cc:
        return float(self.cc[cat])
      return 0

    # The total number of items
    def totalcount(self):
      return sum(self.cc.values( ))

    # The list of all categories
    def categories(self):
      return self.cc.keys( )

    # Function used to train the classifier based on known inputs
    def train(self,documents,cat):
      features=self.getfeatures(document)
      
      # Increment the count for every feature with this category
      for f in features:
        self.incf(f,cat)
    
      # Increment the count for this category
      self.incc(cat)
      
    def fprob(self,f,cat):
      if self.catcount(cat)==0: return 0

      # The total number of times this feature appeared in this
      # category divided by the total number of items in this category
      return self.fcount(f,cat)/self.catcount(cat)
      
    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
      # Calculate current probability
      basicprob=prf(f,cat)

      # Count the number of times this feature has appeared in
      # all categories
      totals=sum([self.fcount(f,c) for c in self.categories( )])

      print "f", f
      print "cat", cat
      print "basicprob", basicprob
      print "totals", totals
      

      # Calculate the weighted average
      bp=((weight*ap)+(totals*basicprob))/(weight+totals)
      return bp

    def setthreshold(self,cat,t):
      self.thresholds[cat]=t

    def getthreshold(self,cat):
      if cat not in self.thresholds: return 1.0
      return self.thresholds[cat]

    def classify(self,item,default=None):
      probs={}

      # Find the category with the highest probability
      max=0.0
      for cat in self.categories( ):
        probs[cat]=self.prob(item,cat)

        if probs[cat]>max:
          max=probs[cat]
          best=cat

      # Make sure the probability exceeds threshold*next best
      for cat in probs:
        if cat==best: continue
        if probs[cat]*self.getthreshold(best)>probs[best]:
          return default
      
      return best

  class naivebayes(classifier):
      
    def docprob(self,document,cat):
      features=self.getfeatures(document)
      # Multiply the probabilities of all the features together
      p=1
      for f in features: 
        p*=self.weightedprob(f,cat,self.fprob)

      return p
          
    def prob(self,item,cat):
      catprob=self.catcount(cat)/self.totalcount()
      docprob=self.docprob(item,cat)
      print "docprob:", docprob
      return docprob*catprob  

  # Returns the set of words surrounding a certian character
  # Provide a document that is a set of words around a single
  # mention of a character
  # We can combine all mentions of a character in some meaningful
  # way later
  def getwords(word_list):
    return word_list

  def produce_word_lists(book, char):
    char_words_lists = []
    for i in range(10, len(book) - 10):
      if (book[i] in char_alias[character]):
        char_word_lists.append(book[i-10:i+10])

    return char_word_lists

  # Classify a character based on his surroundings
  cl = naivebayes(getwords)

  # Dead Characters
  # Joffery  - 2 
  #D_list = produce_word_lists(book, char[2])
  for (i in range(0, len(D_list)):
    cl.train(D_list[i], "dead")
  
  # Ned      - 69
  #D_list = produce_word_lists(book, char[69])
  #for (word_list in D_list):
  #  cl.train(word_list, "dead")
  
  # Robb     - 75
  #D_list = produce_word_lists(book, char[75])
  #for (word_list in D_list):
  #  cl.train(word_list, "dead")
  
  # Viserys  - 82
  #D_list = produce_word_lists(book, char[82])
  #for (word_list in D_list):
  #  cl.train(word_list, "dead")
  
  # Living Well Characters
  # Arya     - 65
  #A_list = produce_word_lists(book, char[65])
  #for (word_list in D_list):
  #  cl.train(word_list, "alive")
  
  # Daenerys - 80
  #A_list = produce_word_lists(book, char[80])
  #for (word_list in D_list):
  #  cl.train(word_list, "alive")
  
  # Baelish  - 56
  #A_list = produce_word_lists(book, char[56])
  #for (word_list in D_list):
  #  cl.train(word_list, "alive")
  
  # Bran     - 67
  #A_list = produce_word_lists(book, char[67])
  #for (word_list in D_list):
  #  cl.train(word_list, "alive")
  
  #print "categories", cl.categories()
  #print "total count", cl.totalcount()
  #print "catcount", cl.catcount("dead"), cl.catcount("alive")

  #f = "crow"

  #print "fcount(f,dead)", cl.fcount(f, "dead")
  #print "fcount(f,alive)", cl.fcount(f, "alive")

  #print "fprob(f,dead)", cl.fprob(f, "dead")
  #print "fprob(f,alive)", cl.fprob(f, "alive")

  #print "weightedprob(f,dead,fprob)", cl.weightedprob(f,"dead",cl.fprob)
  #print "weightedprob(f,alive,fprob)", cl.weightedprob(f,"alive",cl.fprob)

  #print "class", cl.classify("Eddard Stark")
bayes(book, char, char_alias)
