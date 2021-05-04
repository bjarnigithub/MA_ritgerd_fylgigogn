# Template: 
# ./maelanakvaemni.py [ísl_eða_faer_aðaltengingar] [gullstaðall] [úttak_úr_splitter] [niðurstöður_úttak]

echo "villugreining - aðaltengingar"
python3 ./maelanakvaemni.py isl test_correctoutput_fyrirvillugr_eftiruppf.txt test_isl_villugr_adaltengingar.txt test_isl_nidurstodur_adaltengingar.txt

echo "villugreining - aðaltengingar + þrjú orð sitthvoru megin við aðaltengingarnar"
python3 ./maelanakvaemni.py isl test_correctoutput_fyrirvillugr_eftiruppf.txt test_isl_villugr_threewords.txt test_isl_nidurstodur_threewords.txt

echo "villugreining - aðaltengingar + orðflokkar"
python3 ./maelanakvaemni.py isl test_correctoutput_fyrirvillugr_eftiruppf.txt test_isl_villugr_ordflokkar.txt test_isl_nidurstodur_ordflokkar.txt

echo "villugreining - aðaltengingar + athuga hvort orð sé óbeygjanlegt" 
python3 ./maelanakvaemni.py isl test_correctoutput_fyrirvillugr_eftiruppf.txt test_isl_villugr_obeygjanlegt.txt test_isl_nidurstodur_obeygjanlegt.txt

echo "villugreining - aðaltengingar + skoða fleiri greinarmerki"
python3 ./maelanakvaemni.py isl test_correctoutput_fyrirvillugr_eftiruppf.txt test_isl_villugr_greinarmerki.txt test_isl_nidurstodur_greinarmerki.txt

echo "villugreining - allar uppfærslur"
python3 ./maelanakvaemni.py isl test_correctoutput_fyrirvillugr_eftiruppf.txt test_isl_villugr_allaruppf.txt test_isl_nidurstodur_allaruppf.txt