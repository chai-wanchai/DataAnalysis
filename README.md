# DataAnalysis
This project about Analysis Signal with EDF file from NSRR dataset 

##### Method ######
------ Prepare File -----------
1.Download file from NSRR
2.prepare environment for python
  -Install python 3.6
  -Install numpy+mkl,scipy from http://www.lfd.uci.edu/~gohlke/pythonlibs/
  -Install pyedflib from pip install pyedflib
3.check frequency of data and group it by frequency
4.move file by frequency (in RemoveFile.py)
5.read signal from file and save to CSV file all file (in readFileEDF.py)
