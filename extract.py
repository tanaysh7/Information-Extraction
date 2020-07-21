#use model to convert description to tagged form using CRF
from bs4 import BeautifulSoup
import pycrfsuite
import spacy
import numpy as np
import pandas as pd
import sys

nlp = spacy.load('en_core_web_sm')


f=open("test-ucla.txt", "r")
contents =f.read()

f=open(sys.argv[2], "r")
testraw =f.read()

test_data=contents
# fd=open("train-ucla.txt", "r")
# train_data =fd.read()
# f.close()
# fd.close()
def make_data_from_xml(lines_of_text):
  alsent=[]
  for line_desc in lines_of_text.split('\n'):
    if line_desc!='':
      content=BeautifulSoup(line_desc,features="lxml")
      if content.body:
        for i in content.body:
          if i.name:
            sent=[]
            doc = nlp(str(i.string))
            for token in doc:
              sent.append((token.text, token.pos_, token.dep_,i.name))
            alsent.append(sent)
  return alsent

def make_data_from_strings(str_in):
  sent=[]
  doc = nlp(str(str_in))
  for token in doc:
    sent.append((token.text, token.pos_, token.dep_,"tag"))
  return [sent]
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
    ]
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:postag=' + postag1,
            '-1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:postag=' + postag1,
            '+1:postag[:2]=' + postag1[:2],
        ])
    else:
        features.append('EOS')
                
    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, dep, label in sent]

def sent2tokens(sent):
    return [token for token, postag,dep, label in sent]



# train_sent=make_data_from_xml(train_data)

# X_train = [sent2features(s) for s in train_sent]
# y_train = [sent2labels(s) for s in train_sent]

# trainer = pycrfsuite.Trainer(verbose=False)

# for xseq, yseq in zip(X_train, y_train):
#     trainer.append(xseq, yseq)

tagger = pycrfsuite.Tagger()
tagger.open(sys.argv[1])

col=['format','description','grading','others','requisite']

d=pd.DataFrame(0, index=col, columns=col)

desc=''
#Loop starts

for m,test_line in enumerate(test_data.split('\n')):
  test_sent=make_data_from_xml(test_line)
  test_X=make_data_from_strings(testraw.split('\n')[m])

  #X_test = [sent2features(s) for s in test_sent]
  X_test = [sent2features(s) for s in test_X]
  y_test = [sent2labels(s) for s in test_sent]
  y_pred = [tagger.tag(xseq) for xseq in X_test]


  for i,j in enumerate(y_pred):
    if y_test[i]==j[0]:
      d[j[0]][j[0]]+=1
    else:
      d[j[0]][y_test[i][0]]+=1

  #print(d)


  predsent=''
  for i,j in enumerate(y_pred):
  
    
    prev=None
    for p,q in enumerate(j):
      
      if prev!=q:
        if not prev:
          predsent+='<'+q+'>'+test_X[i][p][0]
        else:
          predsent+='</'+prev+'> '+'<'+q+'>' +test_X[i][p][0]
        prev=q
      else:
        if test_X[i][p][0] in ['.',',','/',';',':',')']:
          predsent+=test_X[i][p][0]
        else:
          if p>0:
            if test_X[i][p-1][0] in ['(','/']:
              predsent+=test_X[i][p][0]
            else:
              predsent+=' '+test_X[i][p][0]
          else:
            predsent+=' '+test_X[i][p][0]
    predsent+='</'+prev+'>'
  desc+=predsent+'\n'

fx = open(sys.argv[3],"w") 
fx.write(desc)  
fx.close()


precision=dict()
recall=dict()
f1=dict()

for i in d.columns:
  if d[i][i]!=0:
    precision[i]=d[i][i]/d.loc[:,i].sum()
    recall[i]=d[i][i]/d.loc[i,:].sum()
    f1[i]=2*(precision[i]*recall[i])/(precision[i]+recall[i])
  else:
    precision[i]=0
    recall[i]=0
    f1[i]=0


kp=pd.concat([pd.DataFrame.from_dict(precision, orient='index'),pd.DataFrame.from_dict(recall, orient='index'),pd.DataFrame.from_dict(f1, orient='index')],axis=1)
kp.columns=columns=['Precision','Recall','F1 Score']

print(kp)