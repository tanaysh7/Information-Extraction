# Information-Extraction

Information extraction in Python using Conditional Random Fields to segment/chunk the course description of UCLA data set. This project will be using markup tag to indicate the type of chunk. 


Eg.
Lecture, four hours; outside study, eight hours. Requisite: course 180. Additional requisites for each offering announced in advance by department. Selections from design, analysis, optimization, and implementation of algorithms; computational complexity and general theory of algorithms; algorithms for particular application areas. Subtitles of some current sections: Principles of Design and Analysis (280A); Distributed Algorithms (280D); Graphs and Networks (280G). May be repeated for credit with consent of instructor and topic change. Letter grading. 
 

For example, here is the chunking of the above sample:  
```<format> Lecture, four hours; outside study, eight hours. </format> <requisite> Requisite: course 180. Additional requisites for each offering announced in advance by department. </requisite> <description> Selections from design, analysis, optimization, and implementation of algorithms; computational complexity and general theory of algorithms; algorithms for particular application areas. </description> <others> Subtitles of some current sections: Principles of Design and Analysis (280A); Distributed Algorithms (280D); Graphs and Networks (280G). <others> <others> May be repeated for credit with consent of instructor and topic change. </others> <grading> Letter grading. </grading>
```

## Execution format: 

python extract.py ucla.model test_raw test-ucla.txt 

(arg1- model arg2- descriptions as lines arg3- tagged file to evaluate text) 
 
## Output:  

• Prints Evaluation 

• O/p file – test_generated.txt  
 
## Features implemented: 
 
        'bias',         
        'word.lower=' + word.lower(),         
        'word[-3:]=' + word[-3:],         
        'word[-2:]=' + word[-2:],         
        'word.isupper=%s' % word.isupper(),         
        'word.istitle=%s' % word.istitle(),         
        'word.isdigit=%s' % word.isdigit(),         
        'postag=' + postag,         
        'postag[:2]=' + postag[:2],                  
        features.append('BOS')         
        features.append('EOS') 
 
 

 
Model Evaluation: 
Prediction on training set : 
|  |Precision |   Recall  | F1 Score         |
|---|--------|-------------|---------------------|
| format     |  1.000000  | 1.000000  |1.000000  |
| description|  0.993631  | 1.000000 | 0.996805  |
| grading    |  1.000000  |1.000000 | 1.000000  |
| others     |  1.000000  |0.993464 | 0.996721  |
| requisite  |  1.000000  |1.000000|  1.000000  |
 


 
Prediction on test set : 
|      |Precision  | Recall |  F1 Score| 
|---|--------|-------------|---------------------|
|format     |   1.000000 | 1.00000 | 1.000000| 
|description|   0.927273 | 1.00000 | 0.962264| 
|grading    |   1.000000 | 1.00000 | 1.000000| 
|others     |   1.000000 | 0.83871 | 0.912281| 
|requisite  |   0.973684 | 1.00000 | 0.986667| 
 