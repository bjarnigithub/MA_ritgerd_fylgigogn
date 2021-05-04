# Template: 
# python3 ./splitter.py [model] [heldurendaellegar] [threewords] [ordflokkar] [obeygjanlegt] [greinarmerki] [train_or_split] [isl_or_faer_language] [textoutputfile] [psdoutputfile] [inputFile]

# Hér er verið að þjálfa Splitterinn á íslensku þjálfunargögnunum 

# isl_villugr_ordf_greinarm => leita að og/en/eða/heldur/enda/ellegar; skoðar orðflokkaupplýsingar; skoðar fleiri greinarmerki en bara kommu

# isl_villugr_ordf_greinarm => leita að og/en/eða/heldur/enda/ellegar; skoðar orðflokkaupplýsingar; skoðar fleiri greinarmerki en bara kommu
echo "ísl - þjálfa - orðflokkar og fleiri greinarmerki"
python3 ./splitter.py isl_villugr_ordf_greinarm.gz y n y n y train isl outputtextfile.txt outputpsdfile.psd inputfile.txt

