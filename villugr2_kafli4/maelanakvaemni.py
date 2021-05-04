import copy
import sys

# ./maelanakvaemni.py [ísl_eða_faer_aðaltengingar] [gullstaðall] [úttak_úr_splitter] [niðurstöður_úttak]

ISL_EDA_FAER_ADALTENGINGAR = sys.argv[1]

if ISL_EDA_FAER_ADALTENGINGAR == "isl": 
  CURRENT_ADALTENGINGAR = ["og", "en", "eða", "heldur", "enda", "ellegar"]
elif ISL_EDA_FAER_ADALTENGINGAR == "faer": 
  CURRENT_ADALTENGINGAR = ["og", "men", "ella"]

def getdata(filename):
  filestream = open(filename,"r",encoding="utf-8")
  datastrfromfile = filestream.read()
  datalistfromfile = datastrfromfile.split("\n")
  return datalistfromfile

def processdata(listcontainingsentences):
  aðaltengingar = CURRENT_ADALTENGINGAR 
  
  assembled_list = []
  for line in listcontainingsentences: 
    current_line = line.split()
    if current_line[0] not in aðaltengingar: 
      # setning er í upphafi heildarsetningar og byrjar ekki á aðaltengingu
      if listcontainingsentences.index(line) > 0: 
        assembled_list.append(current_list)  
      current_list = []
      current_list.append(current_line) 
    elif current_line[0] in aðaltengingar: 
      # setning byrjar á aðaltengingu og er inni í heildarsetningu
      current_list.append(current_line) 

    if listcontainingsentences.index(line) == len(listcontainingsentences) - 1: # ef forritið er á síðustu línunni, þá á það að bæta current_list-anum við assembled_listann
      assembled_list.append(current_list)
    
  return assembled_list

def compareoutputs(humanoutput,computeroutput):
  # bera saman úttök og skila lista af setningum sem hafa verið ranglega greindar af splitter.py

  # initialize and define variables 
  index_of_current_sentence_in_computeroutput = 0 
  list_of_incorrect_sentences = [] 

  true_positive_in_compareoutputs = 0
  for sentence in computeroutput:
    if not sentence == humanoutput[index_of_current_sentence_in_computeroutput]: 
      list_of_incorrect_sentences.append((humanoutput[index_of_current_sentence_in_computeroutput], sentence)) # tuple template: (rétt_setning, röng_setning)
    else: 
      # finna fjölda true_positives í setningum sem hafa ekki villur
      true_positive_in_compareoutputs += len(humanoutput[index_of_current_sentence_in_computeroutput]) - 1 
    index_of_current_sentence_in_computeroutput += 1
  
  deep_copy_of_list_of_incorrect_sentences = copy.deepcopy(list_of_incorrect_sentences)

  return list_of_incorrect_sentences, deep_copy_of_list_of_incorrect_sentences, true_positive_in_compareoutputs

def findtptnfpandfn(list_of_incorrect_sentences, true_positive_in_compareoutputs):
  # initialize variables: 
  true_positive = true_positive_in_compareoutputs
  true_negative = 0
  false_positive = 0
  false_negative = 0

  list_of_false_positive_examples = [] 
  list_of_false_negative_examples = []  

  adaltengingar = CURRENT_ADALTENGINGAR 

  for tuple in list_of_incorrect_sentences: 
    # process tuple
    correct_sentence = tuple[0]
    splitter_sentence = tuple[1]

    new_correct_sentence = []
    for element in correct_sentence:
      if correct_sentence.index(element) == 0: 
        new_correct_sentence.append(element)
        continue
      else: 
        element[0] = "BOUNDARY"
        new_correct_sentence.append(element)

    newer_correct_sentence = []
    for element in new_correct_sentence: 
      for adalsetn in element: 
        newer_correct_sentence.append(adalsetn)

    new_splitter_sentence = []
    for element in splitter_sentence:
      if splitter_sentence.index(element) == 0: 
        new_splitter_sentence.append(element)
        continue
      else: 
        element[0] = "BOUNDARY"
        new_splitter_sentence.append(element)

    newer_splitter_sentence = []
    for element in new_splitter_sentence: 
      for adalsetn in element: 
        newer_splitter_sentence.append(adalsetn) 
    
    # get boundary elements 
    list_of_correct_sentence_boundary_elements = []
    counter = 0
    for element in newer_correct_sentence: 
      if element == "BOUNDARY": 
        correct_sentence_boundary_element = [newer_correct_sentence[counter-2], newer_correct_sentence[counter-1], element, newer_correct_sentence[counter+1], newer_correct_sentence[counter+2]] 
        
        ############################# UPPFÆRSLA #############################
        if correct_sentence_boundary_element[0] in adaltengingar:
          correct_sentence_boundary_element[0] = "BOUNDARY"
        elif correct_sentence_boundary_element[1] in adaltengingar: 
          correct_sentence_boundary_element[1] = "BOUNDARY"
        elif correct_sentence_boundary_element[3] in adaltengingar: 
          correct_sentence_boundary_element[3] = "BOUNDARY"
        elif correct_sentence_boundary_element[4] in adaltengingar: 
          correct_sentence_boundary_element[4] = "BOUNDARY"
        ############################# UPPFÆRSLA #############################
        
        list_of_correct_sentence_boundary_elements.append(correct_sentence_boundary_element)
      counter += 1

    list_of_splitter_sentence_boundary_elements = []
    counter = 0
    for element in newer_splitter_sentence: 
      if element == "BOUNDARY": 
        splitter_sentence_boundary_element = [newer_splitter_sentence[counter-2], newer_splitter_sentence[counter-1], element, newer_splitter_sentence[counter+1], newer_splitter_sentence[counter+2]] 
        
        ############################# UPPFÆRSLA #############################
        # þetta er til þess að það komi ekki upp villa ef það er aðaltenging 
        # í nærumhverfi þess sem hefur verið greint sem aðasetningamark
        if splitter_sentence_boundary_element[0] in adaltengingar:
          splitter_sentence_boundary_element[0] = "BOUNDARY"
        elif splitter_sentence_boundary_element[1] in adaltengingar: 
          splitter_sentence_boundary_element[1] = "BOUNDARY"
        elif splitter_sentence_boundary_element[3] in adaltengingar: 
          splitter_sentence_boundary_element[3] = "BOUNDARY"
        elif splitter_sentence_boundary_element[4] in adaltengingar: 
          splitter_sentence_boundary_element[4] = "BOUNDARY"
        ############################# UPPFÆRSLA #############################
        
        list_of_splitter_sentence_boundary_elements.append(splitter_sentence_boundary_element) 
      counter += 1
    
    # check if tp, tn, fp or fn
    for element in list_of_splitter_sentence_boundary_elements:
      for stak in list_of_correct_sentence_boundary_elements:
        if stak == element: 
          true_positive += 1
          
          stak_index = list_of_correct_sentence_boundary_elements.index(stak)
          list_of_correct_sentence_boundary_elements[stak_index] = "!!!BÚIÐAÐASKOÐA!!!"
          element_index = list_of_splitter_sentence_boundary_elements.index(element)
          list_of_splitter_sentence_boundary_elements[element_index] = "!!!BÚIÐAÐASKOÐA!!!"          
          break

    for element in list_of_splitter_sentence_boundary_elements: 
      if element == "!!!BÚIÐAÐASKOÐA!!!": 
        continue
      else: 
        list_of_false_positive_examples.append(element)
        false_positive += 1

    for element in list_of_correct_sentence_boundary_elements: 
      if element == "!!!BÚIÐAÐASKOÐA!!!": 
        continue
      else: 
        list_of_false_negative_examples.append(element)  
        false_negative += 1

  return true_positive, true_negative, false_positive, false_negative, list_of_false_positive_examples, list_of_false_negative_examples  

def calculatescore(true_positive, true_negative, false_positive, false_negative): 
  # reikna precision, recall og f-measure út frá true-positive, false-positive og false-negative

  # eftirfarandi var tekið úr þessari grein: https://machinelearningmastery.com/precision-recall-and-f-measure-for-imbalanced-classification/
  # Precision = TruePositives / (TruePositives + FalsePositives) 
  # Recall = TruePositives / (TruePositives + FalseNegatives) 
  # F-Measure = (2 * Precision * Recall) / (Precision + Recall)

  precision = true_positive / (true_positive + false_positive) # nákvæmni
  recall = true_positive / (true_positive + false_negative) # heimt
  f_measure = (2 * precision * recall) / (precision + recall) # f-mæling

  return precision, recall, f_measure

def displayresults(deep_copy_of_list_of_incorrect_sentences, precision, recall, f_measure, list_of_false_positive_examples, list_of_false_negative_examples): 
  
  set_of_false_positive_examples = set(tuple(x) for x in list_of_false_positive_examples)
  set_of_false_negative_examples =set(tuple(x) for x in list_of_false_negative_examples)

  results_filename = sys.argv[4] # input("Hvað á skráin með niðurstöðunum að heita? ")
  with open(results_filename, "w", encoding="utf-8") as resultsfile: 
    resultsfile.write("----------------------------------------------------------------------------------------------\n")
    resultsfile.write("Nákvæmni forritsins er: {:.2%}\n".format(precision))
    resultsfile.write("Heimt forritsins er: {:.2%}\n".format(recall))
    resultsfile.write("F-measure: {:.2%}\n".format(f_measure))
    resultsfile.write("----------------------------------------------------------------------------------------------\n")
    resultsfile.write("Eftirfarandi eru setningar textans sem voru rangt greindar samanbornar við rétta greiningu: \n")
    resultsfile.write("(Ath. það gæti verið að sumar aðalsetningar séu rétt greindar en aðrar ekki.)\n")
    resultsfile.write("\n")
    for element in deep_copy_of_list_of_incorrect_sentences:
      resultsfile.write("Rétt greining: {}\n".format(element[0])) 
      resultsfile.write("Röng greining: {}\n".format(element[1]))  
      resultsfile.write("\n")   
    resultsfile.write("----------------------------------------------------------------------------------------------\n")
    ########################################## UPPFÆRSLA ##########################################
    resultsfile.write("Hér er mengi af tilvikum sem voru merkt sem ósannur-jákvæður (e. false-positive):\n\n")
    for element in set_of_false_positive_examples:
      string_element = str(element) + "\n"
      resultsfile.write(string_element)
    resultsfile.write("----------------------------------------------------------------------------------------------\n")
    resultsfile.write("Hér er mengi af tilvikum sem voru merkt sem ósannur-neikvæður (e. false-negative):\n\n")
    for element in set_of_false_negative_examples: 
      string_element = str(element) + "\n"
      resultsfile.write(string_element)
    resultsfile.write("----------------------------------------------------------------------------------------------\n")
    ########################################## UPPFÆRSLA ##########################################

def main(): 
  correct_version_filename = sys.argv[2] # input("Hvað heitir skráin með gullstaðlinum? ")
  splitter_version_filename = sys.argv[3] # input("Hvað heitir skráin sem inniheldur úttakið úr splitter.py? ")
  
  correct_version_list = getdata(correct_version_filename)
  splitter_version_list = getdata(splitter_version_filename)
  
  correct_sentences_assembled = processdata(correct_version_list)
  splitter_sentences_assembled = processdata(splitter_version_list)
  
  list_of_incorrect_sentences, deep_copy_of_list_of_incorrect_sentences, true_positive_in_compareoutputs = compareoutputs(correct_sentences_assembled, splitter_sentences_assembled)
  true_positive, true_negative, false_positive, false_negative, list_of_false_positive_examples, list_of_false_negative_examples = findtptnfpandfn(list_of_incorrect_sentences, true_positive_in_compareoutputs)  

  precision, recall, f_measure = calculatescore(true_positive, true_negative, false_positive, false_negative)

  displayresults(deep_copy_of_list_of_incorrect_sentences, precision, recall, f_measure, list_of_false_positive_examples, list_of_false_negative_examples)

main()