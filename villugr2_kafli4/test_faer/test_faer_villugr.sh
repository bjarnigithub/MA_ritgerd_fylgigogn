# Template: 
# ./runallNeural.sh [model] [heldurendaellegar] [threewords] [ordflokkar] [obeygjanlegt] [greinarmerki] [train_or_split] [isl_or_faer_language] [textoutputfile] [psdoutputfile] [inputFile]

#faer_villugr_adaltengingar => leita að og/men/ella;
#faer_villugr_threewords => leita að og/men/ella; threewords -  leita að þremur orðum fyrir framan og aftan aðaltengingu; 
#faer_villugr_ordflokkar => leita að og/men/ella; ordflokkar - skoða orðflokka 
#faer_villugr_obeygjanlegt => leita að og/men/ella; obeygjanlegt - hvort orð sé óbeygjanlegt 
#faer_villugr_greinarmerki => leita að og/men/ella; greinarmerki - skoða fleiri greinarmerki 
#faer_villugr_allaruppf => allar uppfærslur

##faer_villugr_adaltengingar
#echo "fær - splitta setningum - aðaltengingar"
#./runallNeural.sh faer_villugr_adaltengingar.gz y n n n n split isl test_faer_villugr_adaltengingar.txt outputpsdfile.psd faer_test_inputfile.txt

##faer_villugr_threewords
#echo "fær - splitta setningum - aðaltengingar + þrjú orð sitthvoru megin við aðaltengingarnar"
#./runallNeural.sh faer_villugr_threewords.gz y y n n n split isl test_faer_villugr_threewords.txt outputpsdfile.psd faer_test_inputfile.txt

##faer_villugr_ordflokkar
#echo "fær - splitta setningum - aðaltengingar + orðflokkar"
#./runallNeural.sh faer_villugr_ordflokkar.gz y n y n n split isl test_faer_villugr_ordflokkar.txt outputpsdfile.psd faer_test_inputfile.txt

##faer_villugr_obeygjanlegt
#echo "fær - splitta setningum - aðaltengingar + athuga hvort orð sé óbeygjanlegt" 
#./runallNeural.sh faer_villugr_obeygjanlegt.gz y n n y n split isl test_faer_villugr_obeygjanlegt.txt outputpsdfile.psd faer_test_inputfile.txt

##faer_villugr_greinarmerki
#echo "fær - splitta setningum - aðaltengingar + skoða fleiri greinarmerki"
#./runallNeural.sh faer_villugr_greinarmerki.gz y n n n y split isl test_faer_villugr_greinarmerki.txt outputpsdfile.psd faer_test_inputfile.txt

#faer_villugr_allaruppf
echo "fær - splitta setningum - allar uppfærslur"
./runallNeural.sh faer_villugr_allaruppf.gz y y y y y split isl test_faer_villugr_allaruppf.txt outputpsdfile.psd faer_test_inputfile.txt
