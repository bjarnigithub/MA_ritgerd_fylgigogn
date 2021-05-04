# Pipeline to parse plain text files using the Berkeley neural parser
# and a model trained on IcePaHC.

# ----------------------------------------------------------------------------
# NÝJAR LEIÐBEININGAR: 
# Usage: ./runallNeural.sh [model] [heldurendaellegar] [threewords] [ordflokkar] [obeygjanlegt] [greinarmerki] [train_or_split] [isl_or_faer_language] [txtOutputFile] [outputFile] [inputFile]

# model: nafn á módeli (.gz skrá)

# heldurendaellegar: skoða aðaltengingarnar heldur/enda/ellegar ásamt því að skoða og/en/eða; y/n 
# threewords: skoða þrjú orð fyrir framan og aftan aðaltenginguna; y/n 
# ordflokkar: skoða orðflokka; y/n 
# obeygjanlegt: athuga hvort orð sé óbeygjanlegt; y/n 
# greinarmerki: skoða fleiri greinarmerki en bara kommur beint til vinstri við aðaltenginguna; y/n 

# train_or_split: þjálfa splitter.py (train) eða splitta setningum (split)
# isl_or_faer_language: hvort er verið að vinna með íslensku (isl) eða færeysku (faer)

# txtOutputFile: úttak, texta skipt í aðalsetningar, (.txt skrá)
# outputFile: þáttað úttak (.psd skrá)
# inputFile: inntakstexti (.txt skrá)

# ELDRI LEIÐBEININGAR: 
# Usage: ./runall.sh inputfile.txt textOutputfile.txt outputfile.psd
#
# file1: plain text input
# file2: plain text output, split into matrix clauses
# file3: parsed .psd file formatted like IcePaHC
# ----------------------------------------------------------------------------

# Dependencies:
# python3
# -- package detectormorse (pip3 install detectormorse)
# java
# -- package tokenizer (pip3 install tokenizer)
# Cython (pip3 install cython)
# numpy (pip3 install numpy)
#

#model = $1 # nafnámódeli.gz nafn á módeli # þetta er notað þegar verið er að splitta setningum og þegar verið er að þjálfa splitterinn

#heldurendaellegar = $2 # y/n 
#threewords = $3 # y/n 
#ordflokkar = $4 # y/n # 
#obeygjanlegt = $5 # y/n 
#greinarmerki = $6 # y/n

#train_or_split = $7 # train/split 
#isl_or_faer_language = $8 # isl/faer

txtOutputFile= $9 # var $2 # nafnátextaúttaksskrá.txt
outputFile= ${10} # var $3 # nafnápsdúttaksskrá.psd
inputFile= ${11} # var $1 # nafnátextainntaksskrá.txt

tempfile=${inputFile%.txt}.temp
temppsd=${tempfile%.txt}.psd

# Command to run CorpusSearch (used for formatting trees)
CS="java -classpath ./tools/cs/CS_2.002.75.jar csearch/CorpusSearch"

# STEP 1: Use Greynir's tokenizer for punctuation splitting.
#echo 'Splitting sentences based on punctuation.'
#tokenize $1 > $tempfile # þegar ég er að mæla nákvæmni forritsins þá þarf að sleppa þessari skipun vegna þess að það er þegar búið að aðskilja heildarsetningar frá öðrum heildarsetningum (þ.e. setningatokenize-a) setningarnar/textann í IcePaHC

# STEP 2: Matrix clause splitter developed by Anton Karl Ingason
# based on Kyle Gorman's design of Detector Morse)
echo 'Splitting matrix clauses.'

# var upphaflega ==> python3 ./tools/splitter/splitter.py ./tools/splitter/model heldurendaellegar threewords ordflokkar obeygjanlegt greinarmerki train_or_split isl_or_faer_language txtOutputFile outputFile ${11} > $tempfile.out
python3 ./tools/splitter/splitter.py ./tools/splitter/$1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} > $tempfile.out # upphaflega voru ekki slaufusvigar utan um þetta

:"
#python3 ./tools/splitter/splitter.py ./tools/splitter/villugr7_dev.gz $1 > $tempfile.out # $tempfile breytt í $1 - og tokenizer skipunin kommentuð út # muna að uppfæra þessa skipun þegar tokenizer-skipunni er sleppt (þ.e. breyta tempfile í $1) # líkaninu breytt úr iceconj yfir í villugreining1.gz
mv -f $tempfile.out $tempfile # muna að uppfæra þessa skipun þegar tokenizer-skipunni er sleppt 
# Save txt output file (fully tokenized but not parsed)
mv $tempfile $txtOutputFile # muna að uppfæra þessa skipun þegar tokenizer-skipunni er sleppt 
"



:"
# STEP 3: Run Berkeley Neural Parser
echo 'Running Berkeley Neural Parser (this may take a while)'
python3 ./tools/neuralParser/src/main.py parse --model-path-base ./tools/neuralParser/_dev=84.91.pt --input-path $txtOutputFile --output-path $temppsd

# STEP 4: Restore dashes in phrase labels and tags and remove extra labels
python3 ./tools/scripts/postprocess.py $temppsd $temppsd.dashed
./tools/scripts/postprocessNeural.sh $temppsd.dashed
mv -f $temppsd.dashed $temppsd

# STEP 5: Make output pretty
# This runs a structure changing CorpusSearch query that does
# nothing but reformat the output.
echo 'Formatting output'
./tools/cs/formatpsd.sh $temppsd $temppsd.pretty
mv -f $temppsd.pretty $temppsd

# STEP 6:  Saving output file
echo 'Saving output file'
mv -f $temppsd $outputFile
"

# Done
echo 'Done!'
