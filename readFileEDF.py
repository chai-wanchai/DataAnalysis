from os import listdir
from os.path import isfile, join
import os.path
import pyedflib
import numpy as np
from scipy.stats import kurtosis
import csv

def chunks(ls, n):
    return np.asarray([np.asarray(ls[i:i+n]) for i in range(0, len(ls), n)])

###################  Section read EDF file ##################
def ReadEDFFile (Path,FileName):
	f = pyedflib.EdfReader(Path)
	n = f.signals_in_file
	#print("signal:",n)
	signal_labels = f.getSignalLabels()
	#print("signal:",signal_labels[0])
	minN = min(f.getNSamples())
	##############################
	epoch = 30    # Config Epoch as 5s 10s 15s 30s #
	######## Frequency 1 Hz ##########
	SaO2=chunks(f.readSignal(0),(int)((f.getNSamples()[0]/minN)*epoch))
	PR=chunks(f.readSignal(1),(int)((f.getNSamples()[1]/minN)*epoch))
	Position=chunks(f.readSignal(11),(int)((f.getNSamples()[11]/minN)*epoch))
	light=chunks(f.readSignal(12),(int)((f.getNSamples()[12]/minN)*epoch))
	ox_stat=chunks(f.readSignal(13),(int)((f.getNSamples()[13]/minN)*epoch))
	######## Frequency 10 Hz ###########
	airflow=chunks(f.readSignal(8),(int)((f.getNSamples()[8]/minN)*epoch))
	ThorRes=chunks(f.readSignal(9),(int)((f.getNSamples()[9]/minN)*epoch))
	AbdoRes=chunks(f.readSignal(10),(int)((f.getNSamples()[10]/minN)*epoch))
	########  Frequency 50 Hz ##########
	EOG_L =chunks(f.readSignal(5),(int)((f.getNSamples()[5]/minN)*epoch))
	EOG_R =chunks(f.readSignal(6),(int)((f.getNSamples()[6]/minN)*epoch))
	######### Frequency 125 Hz ########
	EEG_sec=chunks(f.readSignal(2),(int)((f.getNSamples()[2]/minN)*epoch))
	EEG=chunks(f.readSignal(7),(int)((f.getNSamples()[7]/minN)*epoch))
	EMG=chunks(f.readSignal(4),(int)((f.getNSamples()[4]/minN)*epoch))
	######## Frequency 250 Hz #########
	ECG=chunks(f.readSignal(3),(int)((f.getNSamples()[3]/minN)*epoch))
	##################################
	f._close()
	loopEpoch =(int)(minN/epoch)
	print(loopEpoch)
	People =[FileName.split('.edf')[0]]
	
	for I in range(loopEpoch):
		ALL =[min(SaO2[I]),max(SaO2[I]),np.mean(SaO2[I]),np.std(SaO2[I]),kurtosis(SaO2[I]),
		min(PR[I]),max(PR[I]),np.mean(PR[I]),np.std(PR[I]),kurtosis(PR[I]),
		min(Position[I]),max(Position[I]),np.mean(Position[I]),np.std(Position[I]),kurtosis(Position[I]),
		min(light[I]),max(light[I]),np.mean(light[I]),np.std(light[I]),kurtosis(light[I]),
		min(ox_stat[I]),max(ox_stat[I]),np.mean(ox_stat[I]),np.std(ox_stat[I]),kurtosis(ox_stat[I]),
		min(airflow[I]),max(airflow[I]),np.mean(airflow[I]),np.std(airflow[I]),kurtosis(airflow[I]),
		min(ThorRes[I]),max(ThorRes[I]),np.mean(ThorRes[I]),np.std(ThorRes[I]),kurtosis(ThorRes[I]),
		min(AbdoRes[I]),max(AbdoRes[I]),np.mean(AbdoRes[I]),np.std(AbdoRes[I]),kurtosis(AbdoRes[I]),
		min(EOG_L[I]),max(EOG_L[I]),np.mean(EOG_L[I]),np.std(EOG_L[I]),kurtosis(EOG_L[I]),
		min(EOG_R[I]),max(EOG_R[I]),np.mean(EOG_R[I]),np.std(EOG_R[I]),kurtosis(EOG_R[I]),
		min(EEG_sec[I]),max(EEG_sec[I]),np.mean(EEG_sec[I]),np.std(EEG_sec[I]),kurtosis(EEG_sec[I]),
		min(EEG[I]),max(EEG[I]),np.mean(EEG[I]),np.std(EEG[I]),kurtosis(EEG[I]),
		min(ECG[I]),max(ECG[I]),np.mean(ECG[I]),np.std(ECG[I]),kurtosis(ECG[I]),
		min(EMG[I]),max(EMG[I]),np.mean(EMG[I]),np.std(EMG[I]),kurtosis(EMG[I])]
		People.append(ALL)
	
	WriteHeaderCSV (People,People[0])
	
############### end section read file EDF ##############


########################  Write CSV File #############################################

def WriteHeaderCSV (listData,File):
	if os.path.isfile("SignalEpoch30s.csv"):
		print (File," Save to CSV File")
		with open('SignalEpoch30s.csv', 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow(listData)
			
	else:
		###Create header og CSV as e1_EEG(sec) mean epoch 1 of signal EEG
		print ("Create file")
		s =['subject']
		Signal = ['SaO2_min','SaO2_max','SaO2_avg','SaO2_SD','SaO2_kurtosis',
			'PR_min','PR_max','PR_avg','PR_SD','PR_kurtosis',
			'position_min','position_max','position_avg','position_SD','position_kurtosis',
			'light_min','light_max','light_avg','light_SD','light_kurtosis',
			'ox_stat_min','ox_stat_max','ox_stat_avg','ox_stat_SD','ox_stat_kurtosis',
			'airflow_min','airflow_max','airflow_avg','airflow_SD','airflow_kurtosis',
			'ThorRes_min','ThorRes_max','ThorRes_avg','ThorRes_SD','ThorRes_kurtosis',
			'AbdoRes_min','AbdoRes_max','AbdoRes_avg','AbdoRes_SD','AbdoRes_kurtosis',
			'EOG(L)_min','EOG(L)_max','EOG(L)_avg','EOG(L)_SD','EOG(L)_kurtosis',
			'EOG(R)_min','EOG(R)_max','EOG(R)_avg','EOG(R)_SD','EOG(R)_kurtosis',
			'EEG(sec)_min','EEG(sec)_max','EEG(sec)_avg','EEG(sec)_SD','EEG(sec)_kurtosis',
			'EEG_min','EEG_max','EEG_avg','EEG_SD','EEG_kurtosis',
			'ECG_min','ECG_max','ECG_avg','ECG_SD','ECG_kurtosis',
			'EMG_min','EMG_max','EMG_avg','EMG_SD','EMG_kurtosis']
		for n in range(1440):
			for i in Signal:
				s.append('e'+str(n+1)+'_'+i)
		
		with open('SignalEpoch30s.csv', 'w', newline='') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow(s)
			spamwriter.writerow(listData)
			print(File,"Save to CSV File")
########################################################################################	




#########################  Main #######################################################
if __name__ == '__main__':
	### You must create folder name = "edf" and put file .edf in folder ###
	mypath =input("Enter Directory keep EDF File: ")
	FileName = [f for f in listdir(mypath) if f.endswith(".edf")]
	for numFile in FileName:
		fullpath = mypath+"\\"+numFile
		print("-----------------"+numFile+"-----------------")
		ReadEDFFile(fullpath,numFile)
		#WriteHeaderCSV(FileName)

#########################  End Main  ##################################################