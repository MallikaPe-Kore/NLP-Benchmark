import requests, csv, os, time,sys
TyOfUtt=[]#Reading the type of utterances from input ML_Result csv file
success=[[],[],[]]
intent=[]
matched=[[],[],[]]
precession=[0,0,0]
recall=[0,0,0]
fscore=[0,0,0]
accuracy=[0,0,0]
def main(resultsFileName):
	fr=open(resultsFileName,'r')
	try:
		reader=csv.reader(fr,delimiter=',')
		x = reader.next()
		while 1:
			try:
				x = reader.next()
				intent.append(x[0])
				TyOfUtt.append(x[2])
				matched[0].append(x[3])
				matched[1].append(x[7])
				matched[2].append(x[10])
				success[0].append(x[4])
				success[1].append(x[8])
				success[2].append(x[11])
			except StopIteration:
				break

		fr.close()
	except:
		print("File not found")


def writeCSV(fr1,currentIntent=None):
	b1=['','KORE.AI: ALL','KORE.AI: NONE','','API.AI:ALL','API.AI:NONE','','LUIS.AI:ALL','LUIS.AI:NONE','']
	b2=['TP']
	b3=['TN']
	b4=['FN']
	b5=['FP']
	c1=['','KORE.AI','','API.AI','','LUIS.AI']
	c2=['Precision']
	c3=['Recall']
	c4=['F Measure']
	c5=['Error']
	c6=['Accuracy']

	arrayD=['Type Of Utterance','Success_Kore.ai','Failure_Kore.ai','Success_Api.ai','Failure_Api.ai','Success_Luis.ai','Failure_Luis.ai','Total Utterances']
	array1=['Positive']
	array2=['Negative']
	array3=['Structurally different']
	array4=['Stemming and Lemmatization']
	array5=['Spell Error']
	'''Loop for the three platforms for result table calculation'''
	for platforms in range(3):
		totalPositives=0
		truePositives=0
		falseNegatives=0
		totalNegatives=0
		trueNegatives=0
		falsePositives=0
		truePositivesNone=0
		falsePositivesNone=0
		trueNegativesNone=0
		falseNegativesNone=0
		totalStruct=0
		strucTruePositive=0
		strucFalseNegative=0
		totalStem=0
		stemTruePositive=0
		stemFalseNeg=0
		spellTruePos=0
		spellFalseNeg=0
		totalSpell=0
		intentset = set(intent)
		lenintent = len(intentset)
		if currentIntent:
			lenintent = 1
			intentset = set([currentIntent])
		for currentintent in intentset:
		    for i in range(len(TyOfUtt)):
			if(currentintent==matched[platforms][i] and intent[i]==matched[platforms][i]):
					if currentintent =='None':
						truePositivesNone +=1
					else:
						truePositives +=1
			if(currentintent==matched[platforms][i] and intent[i]!=matched[platforms][i]):
					if currentintent == 'None':
						falsePositivesNone +=1
					else:
						falsePositives +=1
			if(currentintent!=matched[platforms][i] and currentintent != intent[i] and matched[platforms][i]==intent[i]):
					if currentintent == 'None':
						trueNegativesNone +=1
					else:
						trueNegatives +=1
			if(currentintent!=matched[platforms][i] and currentintent == intent[i]):
					if currentintent == 'None':
						falseNegativesNone +=1
					else:
						falseNegatives += 1
			if(TyOfUtt[i].lower()=='structurally different'):
				if(success[platforms][i]=='pass'):
				    if(currentintent == None or currentintent==intent[i]):
					strucTruePositive+=1
				elif(success[platforms][i]=='fail'):
				    if(currentintent == None or currentintent==intent[i]):
					strucFalseNegative+=1
				totalStruct=strucTruePositive+strucFalseNegative
			elif(TyOfUtt[i].lower()=='stemming and lemmatization'):
				if(success[platforms][i]=='pass'):
				    if(currentintent == None or currentintent==intent[i]):
					stemTruePositive+=1
				elif(success[platforms][i]=='fail'):
				    if(currentintent == None or currentintent==intent[i]):
					stemFalseNeg+=1
				totalStem=stemTruePositive+stemFalseNeg
			elif(TyOfUtt[i].lower()=='spell errors'):
				if(success[platforms][i]=='pass'):
				    if(currentintent == None or currentintent==intent[i]):
					spellTruePos+=1
				elif(success[platforms][i]=='fail'):
				    if(currentintent == None or currentintent==intent[i]):
					spellFalseNeg+=1
				totalSpell=spellTruePos+spellFalseNeg
		totalPositives=truePositives+falseNegatives+truePositivesNone+falseNegativesNone
		totalNegatives=trueNegatives+falsePositives+trueNegativesNone+falsePositivesNone
		array1.append(truePositives)
		array1.append(falseNegatives)
		array2.append(trueNegatives)
		array2.append(falsePositives)
		array3.append(strucTruePositive)
		array3.append(strucFalseNegative)
		array4.append(stemTruePositive)
		array4.append(stemFalseNeg)
		array5.append(spellTruePos)
		array5.append(spellFalseNeg)		
		try:	
			arrayB=[b1,b2,b3,b4,b5]
			arrayC=[c1,c2,c3,c4,c5,c6]
			#Calling the function for formulae calculation and result tables
			#i.e. to identify the sum of false positives, false negatives, etc
			if currentIntent == None:
				arrayC[1].append(1.0*precession[platforms]/lenintent)
				arrayC[1].append('')
				arrayC[2].append(1.0*recall[platforms]/lenintent)
				arrayC[2].append('')
				arrayC[3].append(1.0*fscore[platforms]/lenintent)
				arrayC[3].append('')
				arrayC[4].append('')
				arrayC[4].append('')
				arrayC[5].append(1.0*accuracy[platforms]/lenintent)
				arrayC[5].append('')
			calculateAndInsert( arrayC, totalPositives, truePositives+truePositivesNone, falseNegatives+falseNegativesNone, totalNegatives, trueNegatives+trueNegativesNone, falsePositives+falsePositivesNone, currentintent, lenintent, platforms)
			arrayB[1].append(truePositives)
			arrayB[1].append(truePositivesNone)
			arrayB[1].append('')
			arrayB[2].append(trueNegatives)
			arrayB[2].append(trueNegativesNone)
			arrayB[2].append('')
			arrayB[3].append(falseNegatives)
			arrayB[3].append(falseNegativesNone)
			arrayB[3].append('')
			arrayB[4].append(falsePositives)
			arrayB[4].append(falsePositivesNone)
			arrayB[4].append('')
		except Exception as e:
			print(e)
			continue
	array1.append(totalPositives)
	array2.append(totalNegatives)
	array3.append(totalStruct)
	array4.append(totalStem)
	array5.append(totalSpell)
	array=[arrayD,array1,array2,array3,array4,array5]	
	'''printing the three result tables for all the three platforms'''
	if currentIntent:
	  fr1.write(currentIntent+":\n")
	else:
	  fr1.write("All intents:\n")
	if( currentIntent == None):
	  for i in range(len(array)):
		row=''
		for j in range(len(array1)):
			row=row+str(array[i][j])+','
		fr1.write(row+"\n")
	  fr1.write("\n")
	  for i in range(len(arrayC)):
		row=''
		for j in range(len(arrayC[i])):
			row=row+str(arrayC[i][j])+','
		fr1.write(row+"\n")	
	  fr1.write("\n")
	for i in range(len(arrayB)):
		row=''
		for j in range(len(arrayB[i])):
			row=row+str(arrayB[i][j])+','
		fr1.write(row+"\n")
	fr1.write("\n")
	if not currentintent:
	  fr1.write("Individual intents:\n")

def calculateAndInsert( arrayC, totalPositives, truePositives, falseNegatives, totalNegatives, trueNegatives, falsePositives,currentintent,lenintents , platforms):
	try:
		prK=round((truePositives)/float(truePositives+falsePositives),4)#Calculating Precision
	except:
		prK=0
	try:
		rrK=round((truePositives)/float(truePositives+falseNegatives),4)#Calculating Recall
	except:
		rrK=0
	try:
		acK=round((truePositives+trueNegatives)/float(totalPositives+totalNegatives),4)#Calculating Accuracy
	except:
		acK=0
	try:
		frK=round((2*prK*rrK)/float(prK+rrK),4)#Calculating F Measure
	except:
		frK=0
	if currentintent != None:
		precession[platforms]+=prK
		recall[platforms]+=rrK
		accuracy[platforms]+=acK
		fscore[platforms]+=frK


if __name__=="__main__":
	main(sys.argv[1])
	timestr=time.strftime("%d-%m-%Y--%H-%M-%S")
	fr1=open('tmp','w')
	fr2=open('Summary-'+timestr+'.csv','w')
	fr1.write("Individual\n\n")
	for ints in set(intent):
	    if ints != 'None':
		writeCSV(fr1,ints)

	writeCSV(fr1,'None')
	fr1.close()


	writeCSV(fr2, None)
	fr2.close()
	os.system("cat "+fr1.name+" >> "+fr2.name)
	os.system("rm "+fr1.name)

