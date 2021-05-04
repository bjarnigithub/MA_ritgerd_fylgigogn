# Template: 
# python3 ./splitter.py [model] [heldurendaellegar] [threewords] [ordflokkar] [obeygjanlegt] [greinarmerki] [train_or_split] [isl_or_faer_language] [textoutputfile] [psdoutputfile] [inputFile]

# Hér er verið að þjálfa Splitterinn á færeysku þjálfunargögnunum 

#faer_villugr_adaltengingar => leita að og/eða/heldur/enda/ellegar;
#faer_villugr_threewords => leita að og/eða/heldur/enda/ellegar; threewords -  leita að þremur orðum fyrir framan og aftan aðaltengingu; 
#faer_villugr_ordflokkar => leita að og/eða/heldur/enda/ellegar; ordflokkar - skoða orðflokka 
#faer_villugr_obeygjanlegt => leita að og/eða/heldur/enda/ellegar; obeygjanlegt - hvort orð sé óbeygjanlegt 
#faer_villugr_greinarmerki => leita að og/eða/heldur/enda/ellegar; greinarmerki - skoða fleiri greinarmerki 
#faer_villugr_allaruppf => allar uppfærslur

# faer_villugr_adaltengingar => leita að og/eða/heldur/enda/ellegar;
echo "fær - þjálfa - aðaltengingar"
python3 ./splitter.py faer_villugr_adaltengingar.gz y n n n n train faer outputtextfile.txt outputpsdfile.psd inputfile.txt

# faer_villugr_threewords => leita að og/eða/heldur/enda/ellegar; threewords -  leita að þremur orðum fyrir framan og aftan aðaltengingu; 
echo "fær - þjálfa - aðaltengingar + þrjú orð sitthvoru megin við aðaltengingarnar"
python3 ./splitter.py faer_villugr_threewords.gz y y n n n train faer outputtextfile.txt outputpsdfile.psd inputfile.txt

# faer_villugr_ordflokkar => leita að og/eða/heldur/enda/ellegar; ordflokkar - skoða orðflokka 
echo "fær - þjálfa - aðaltengingar + orðflokkar"
python3 ./splitter.py faer_villugr_ordflokkar.gz y n y n n train faer outputtextfile.txt outputpsdfile.psd inputfile.txt

# faer_villugr_obeygjanlegt => leita að og/eða/heldur/enda/ellegar; obeygjanlegt - hvort orð sé óbeygjanlegt 
echo "fær - þjálfa - aðaltengingar + athuga hvort orð sé óbeygjanlegt" 
python3 ./splitter.py faer_villugr_obeygjanlegt.gz y n n y n train faer outputtextfile.txt outputpsdfile.psd inputfile.txt

# faer_villugr_greinarmerki => leita að og/eða/heldur/enda/ellegar; greinarmerki - skoða fleiri greinarmerki 
echo "fær - þjálfa - aðaltengingar + skoða fleiri greinarmerki"
python3 ./splitter.py faer_villugr_greinarmerki.gz y n n n y train faer outputtextfile.txt outputpsdfile.psd inputfile.txt

# faer_villugr_allaruppf => allar uppfærslur
echo "fær - þjálfa - allar uppfærslur"
python3 ./splitter.py faer_villugr_allaruppf.gz y y y y y train faer outputtextfile.txt outputpsdfile.psd inputfile.txt
