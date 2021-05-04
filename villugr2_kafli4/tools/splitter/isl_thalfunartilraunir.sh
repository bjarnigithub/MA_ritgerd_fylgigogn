# Template: 
# python3 ./splitter.py [model] [heldurendaellegar] [threewords] [ordflokkar] [obeygjanlegt] [greinarmerki] [train_or_split] [isl_or_faer_language] [textoutputfile] [psdoutputfile] [inputFile]

# Hér er verið að þjálfa Splitterinn á íslensku þjálfunargögnunum

#isl_villugr_adaltengingar => leita að og/en/eða/heldur/enda/ellegar;
#isl_villugr_threewords => leita að og/en/eða/heldur/enda/ellegar; threewords -  leita að þremur orðum fyrir framan og aftan aðaltengingu; 
#isl_villugr_ordflokkar => leita að og/en/eða/heldur/enda/ellegar; ordflokkar - skoða orðflokka 
#isl_villugr_obeygjanlegt => leita að og/en/eða/heldur/enda/ellegar; obeygjanlegt - hvort orð sé óbeygjanlegt 
#isl_villugr_greinarmerki => leita að og/en/eða/heldur/enda/ellegar; greinarmerki - skoða fleiri greinarmerki 
#isl_villugr_allaruppf => allar uppfærslur

# isl_villugr_adaltengingar => leita að og/en/eða/heldur/enda/ellegar;
echo "ísl - þjálfa - aðaltengingar"
python3 ./splitter.py isl_villugr_adaltengingar.gz y n n n n train isl outputtextfile.txt outputpsdfile.psd inputfile.txt

# isl_villugr_threewords => leita að og/en/eða/heldur/enda/ellegar; threewords -  leita að þremur orðum fyrir framan og aftan aðaltengingu; 
echo "ísl - þjálfa - aðaltengingar + þrjú orð sitthvoru megin við aðaltengingarnar"
python3 ./splitter.py isl_villugr_threewords.gz y y n n n train isl outputtextfile.txt outputpsdfile.psd inputfile.txt

# isl_villugr_ordflokkar => leita að og/en/eða/heldur/enda/ellegar; ordflokkar - skoða orðflokka 
echo "ísl - þjálfa - aðaltengingar + orðflokkar"
python3 ./splitter.py isl_villugr_ordflokkar.gz y n y n n train isl outputtextfile.txt outputpsdfile.psd inputfile.txt

# isl_villugr_obeygjanlegt => leita að og/en/eða/heldur/enda/ellegar; obeygjanlegt - hvort orð sé óbeygjanlegt 
echo "ísl - þjálfa - aðaltengingar + athuga hvort orð sé óbeygjanlegt" 
python3 ./splitter.py isl_villugr_obeygjanlegt.gz y n n y n train isl outputtextfile.txt outputpsdfile.psd inputfile.txt

# isl_villugr_greinarmerki => leita að og/en/eða/heldur/enda/ellegar; greinarmerki - skoða fleiri greinarmerki 
echo "ísl - þjálfa - aðaltengingar + skoða fleiri greinarmerki"
python3 ./splitter.py isl_villugr_greinarmerki.gz y n n n y train isl outputtextfile.txt outputpsdfile.psd inputfile.txt

# isl_villugr_allaruppf => allar uppfærslur
echo "ísl - þjálfa - allar uppfærslur"
python3 ./splitter.py isl_villugr_allaruppf.gz y y y y y train isl outputtextfile.txt outputpsdfile.psd inputfile.txt
