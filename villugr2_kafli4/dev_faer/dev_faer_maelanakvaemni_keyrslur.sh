# Template: 
# ./maelanakvaemni.py [ísl_eða_faer_aðaltengingar] [gullstaðall] [úttak_úr_splitter] [niðurstöður_úttak]

#echo "villugreining - aðaltengingar"
#python3 ./maelanakvaemni.py faer faer_dev_correctoutput.txt dev_faer_villugr_adaltengingar.txt dev_faer_nidurstodur_adaltengingar.txt

#echo "villugreining - aðaltengingar + þrjú orð sitthvoru megin við aðaltengingarnar"
#python3 ./maelanakvaemni.py faer faer_dev_correctoutput.txt dev_faer_villugr_threewords.txt dev_faer_nidurstodur_threewords.txt

#echo "villugreining - aðaltengingar + orðflokkar"
#python3 ./maelanakvaemni.py faer faer_dev_correctoutput.txt dev_faer_villugr_ordflokkar.txt dev_faer_nidurstodur_ordflokkar.txt

#echo "villugreining - aðaltengingar + athuga hvort orð sé óbeygjanlegt" 
#python3 ./maelanakvaemni.py faer faer_dev_correctoutput.txt dev_faer_villugr_obeygjanlegt.txt dev_faer_nidurstodur_obeygjanlegt.txt

#echo "villugreining - aðaltengingar + skoða fleiri greinarmerki"
#python3 ./maelanakvaemni.py faer faer_dev_correctoutput.txt dev_faer_villugr_greinarmerki.txt dev_faer_nidurstodur_greinarmerki.txt

echo "villugreining - allar uppfærslur"
python3 ./maelanakvaemni.py faer faer_dev_correctoutput.txt dev_faer_villugr_allaruppf.txt dev_faer_nidurstodur_allaruppf.txt