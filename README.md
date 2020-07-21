# Information-Extraction

Information extraction in Python using Conditional Random Fields to segment/chunk the course description of UCLA data set. This project will be using markup tag to indicate the type of chunk. 


Eg.

Lecture, four hours; outside study, eight hours. Requisite: course 180. Additional requisites for each offering announced in advance by department. Selections from design, analysis, optimization, and implementation of algorithms; computational complexity and general theory of algorithms; algorithms for particular application areas. Subtitles of some current sections: Principles of Design and Analysis (280A); Distributed Algorithms (280D); Graphs and Networks (280G). May be repeated for credit with consent of instructor and topic change. Letter grading. 
 

For example, here is the chunking of the above sample:  <format> Lecture, four hours; outside study, eight hours. </format> <requisite> Requisite: course 180. Additional requisites for each offering announced in advance by department. </requisite> <description> Selections from design, analysis, optimization, and implementation of algorithms; computational complexity and general theory of algorithms; algorithms for particular application areas. </description> <others> Subtitles of some current sections: Principles of Design and Analysis (280A); Distributed Algorithms (280D); Graphs and Networks (280G). <others> <others> May be repeated for credit with consent of instructor and topic change. </others> <grading> Letter grading. </grading>