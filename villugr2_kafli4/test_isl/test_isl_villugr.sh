# Template: 
# ./runallNeural.sh [model] [heldurendaellegar] [threewords] [ordflokkar] [obeygjanlegt] [greinarmerki] [train_or_split] [isl_or_faer_language] [textoutputfile] [psdoutputfile] [inputFile]

#isl_villugr_adaltengingar => leita að og/en/eða/heldur/enda/ellegar;
#isl_villugr_threewords => leita að og/en/eða/heldur/enda/ellegar; threewords -  leita að þremur orðum fyrir framan og aftan aðaltengingu; 
#isl_villugr_ordflokkar => leita að og/en/eða/heldur/enda/ellegar; ordflokkar - skoða orðflokka 
#isl_villugr_obeygjanlegt => leita að og/en/eða/heldur/enda/ellegar; obeygjanlegt - hvort orð sé óbeygjanlegt 
#isl_villugr_greinarmerki => leita að og/en/eða/heldur/enda/ellegar; greinarmerki - skoða fleiri greinarmerki 
#isl_villugr_allaruppf => allar uppfærslur

#isl_villugr_adaltengingar
echo "ísl - splitta setningum - aðaltengingar"
./runallNeural.sh isl_villugr_adaltengingar.gz y n n n n split isl test_isl_villugr_adaltengingar.txt outputpsdfile.psd test_inputfile_fyrirallarvillugreiningar.txt

#isl_villugr_threewords
echo "ísl - splitta setningum - aðaltengingar + þrjú orð sitthvoru megin við aðaltengingarnar"
./runallNeural.sh isl_villugr_threewords.gz y y n n n split isl test_isl_villugr_threewords.txt outputpsdfile.psd test_inputfile_fyrirallarvillugreiningar.txt

#isl_villugr_ordflokkar
echo "ísl - splitta setningum - aðaltengingar + orðflokkar"
./runallNeural.sh isl_villugr_ordflokkar.gz y n y n n split isl test_isl_villugr_ordflokkar.txt outputpsdfile.psd test_inputfile_fyrirallarvillugreiningar.txt

#isl_villugr_obeygjanlegt
echo "ísl - splitta setningum - aðaltengingar + athuga hvort orð sé óbeygjanlegt" 
./runallNeural.sh isl_villugr_obeygjanlegt.gz y n n y n split isl test_isl_villugr_obeygjanlegt.txt outputpsdfile.psd test_inputfile_fyrirallarvillugreiningar.txt

#isl_villugr_greinarmerki
echo "ísl - splitta setningum - aðaltengingar + skoða fleiri greinarmerki"
./runallNeural.sh isl_villugr_greinarmerki.gz y n n n y split isl test_isl_villugr_greinarmerki.txt outputpsdfile.psd test_inputfile_fyrirallarvillugreiningar.txt

#isl_villugr_allaruppf
echo "ísl - splitta setningum - allar uppfærslur"
./runallNeural.sh isl_villugr_allaruppf.gz y y y y y split isl test_isl_villugr_allaruppf.txt outputpsdfile.psd test_inputfile_fyrirallarvillugreiningar.txt
