import logging
import sys
import re
from collections import namedtuple
from re import finditer, match, search
from detectormorse.ptbtokenizer import word_tokenize

from nlup import listify, BinaryAveragedPerceptron, BinaryConfusion, JSONable

# Forritið notar gögn úr Sigrúnarsniðinu (Beygingarlýsing íslensks nútímamáls. Stofnun Árna Magnússonar í íslenskum fræðum. Höfundur og ritstjóri Kristín Bjarnadóttir) (https://bin.arnastofnun.is/). 
# Gögn úr Sigrúnarsniðinu voru sameinuð í skrá ásamt gögnum úr IcePaHC. Í þessari nýju skrá hafa allar beygingarmyndirnar úr Sigrúnarsniðinu verið skrifaðar með lágstöfum. 

# þessi útgáfa af splitternum var notuð í villugreiningu 2 (kafli 4) - hér er búið að innleiða uppfærslur á þann hátt að hægt er að keyra nokkrar tilraunir með shell skriftum

# í staðinn fyrir nöfnin á uppfærslubreytunun skal setja annað hvort y eða n 

# þegar verið er að þjálfa splitter.py þá skal bara keyra splitter.py, en ekki runallNeural.sh
  # dæmi um þjálfunarskipun (inntaks- og úttaksskrárnar eru reyndar ekkert 
  # notaðar í þessari keyrslu, en forritið myndi mögulega crash-a ef ekkert 
  # er sett í þessi hólf í skipuninni): 

  # python3 ./splitter.py [model] [heldurendaellegar] [threewords] [ordflokkar] [obeygjanlegt] [greinarmerki] [train_or_split] [isl_or_faer_language] [txtOutputFile] [psdoutputFile] [inputFile]

# þegar verið er að splitta setningum þá skal keyra runallNeural.sh
  # dæmi um keyrslu-skipun - þetta er skipun sem væri notuð til að keyra
  # runallNeural.sh (þannig að það væri hægt að hafa nokkrar svona skipanir 
  # til að keyra mismunandi útgáfur af villugreiningu í einni shell-script-skrá)

  # ./runallNeural.sh [model] [heldurendaellegar] [threewords] [ordflokkar] [obeygjanlegt] [greinarmerki] [train_or_split] [isl_or_faer_language] [txtOutputFile] [psdoutputFile] [inputFile]

# input from terminal/shell scripts
MODEL_NAME = sys.argv[1] # sys.argv[] 

heldurendaellegar = sys.argv[2] # y/n # sys.argv[] 
threewords = sys.argv[3] # y/n # sys.argv[] 
ordflokkar = sys.argv[4] # y/n # sys.argv[] 
obeygjanlegt = sys.argv[5] # y/n # sys.argv[] 
greinarmerki = sys.argv[6] # y/n # sys.argv[] 

train_or_split = sys.argv[7] # train/split # sys.argv[] 
isl_or_faer_language = sys.argv[8] # isl/faer # sys.argv[] 

if train_or_split == "train": 
  WORDTAGS_LOCATION = ""
elif train_or_split == "split": 
  WORDTAGS_LOCATION = "tools/splitter/"

if isl_or_faer_language == "isl": 
  WORDTAGS_FILENAME = WORDTAGS_LOCATION + "isl_wordtags_sigrunarsnid_sameinad_lowercase.tsv"
  TRAIN_FILE = "train.txt"
elif isl_or_faer_language == "faer": 
  WORDTAGS_FILENAME = WORDTAGS_LOCATION + "faer_wordtags_bbfn_sameinad_lowercase.tsv"
  TRAIN_FILE = "faer_train.txt"

# defaults
EPOCHS = 20     # number of epochs (iterations for classifier training)
BUFSIZE = 32    # breytt úr 32 í 42 (þ.e. +10) og svo 64 (þ.e. *2) til að athuga hvort forritið leiti að t.d. 3 orðum í staðinn fyrir 2 á undan og eftir samtengingunni. Niðurstöður: engin breyting ef talan var 42, engin breyting ef talan er 64, forritið crash-ar ef breytingin er 16 (þ.e. 32/2)  # for reading in left and right contexts...see below

# regexes

if heldurendaellegar == "n" and isl_or_faer_language == "isl": 
  TARGET = r"(\s+)(og|eða|en)(\s+)"
elif heldurendaellegar == "y" and isl_or_faer_language == "isl": 
  TARGET = r"(\s+)(og|eða|en|heldur|enda|ellegar)(\s+)" # UPPFÆRSLA
elif isl_or_faer_language == "faer": 
  TARGET = r"(\s+)(og|men|ella)(\s+)" # UPPFÆRSLA

if threewords == "n": 
  # LTOKEN = r"(\S+)\s*$"
  LTOKEN = r"(\S+)\s*(\S+)\s*$"
  #RTOKEN = r"^\s*(\S+)"
  RTOKEN = r"^\s*(\S+)\s*(\S+)"
elif threewords == "y": 
  ######################UPPFÆRSLA######################
  # Í þessari uppfærslu er verið að skoða 3 orð sitthvoru megin við aðaltenginguna
  # LTOKEN = r"(\S+)\s*$"
  LTOKEN = r"(\S+)\s*(\S+)\s*(\S+)\s*$" # \s = bilstafur; \S = eitthvað sem er ekki bilstafur; $ = endir á streng
  #RTOKEN = r"^\s*(\S+)"
  RTOKEN = r"^\s*(\S+)\s*(\S+)\s*(\S+)" # \s = bilstafur; \S = eitthvað sem er ekki bilstafur; ^ (caret eða hattur) = byrjun á streng
  ######################UPPFÆRSLA######################


NEWLINE = r"^\s*[\r\n]+\s*$"

# other

Observation = namedtuple("Observation", ["left","conjunction","right","boundary","end"])


class IceTags():

    def __init__(self):
        self.wordtags = self.load_wordtags()

    def is_finite(self, word):
        if not word.lower() in self.wordtags:
            return False
                
        for tag in self.wordtags[word.lower()]:
            #if match(r"(VB|HV|DO|RD|MD|BE)[PD][IS]",tag):
            if match(r"(VB|HV|DO|RD|MD|BE)[PD][IS]",tag) or "FH" in tag or "VH" in tag or "BH" in tag or "ST" in tag: # UPPFÆRSLA
                return True
        return False

    def is_nonfinite(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            #if match(r"(VB|HV|DO|RD|MD|BE|VA|DA|RA)[N]?",tag):
            if match(r"(VB|HV|DO|RD|MD|BE|VA|DA|RA)[N]?",tag) or "NH" in tag or "LHNT" in tag or "LHÞT" in tag: # UPPFÆRSLA
                return True
        return False

    def is_nominative(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            #if match("(\S+)\-N", tag):
            if match("(\S+)\-N", tag) or "NF" in tag: # UPPFÆRSLA
                return True
        return False

    def is_oblique(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            #if match("(\S+)\-[ADG]", tag):
            if match("(\S+)\-[ADG]", tag) or "ÞF" in tag or "ÞGF" in tag or "EF" in tag: # UPPFÆRSLA
                return True
        return False

    def load_wordtags(self):
        with open(WORDTAGS_FILENAME) as f: # breytt í breytuheiti # var upphaflega: tools/splitter/wordtags.tsv
            wordtags = dict()
            lines = f.read().splitlines()
            for line in lines:
                key, values = line.split('\t')
                wordtags[key] = values.split()

        return wordtags

    ######################UPPFÆRSLA######################
    # athuga hvort orðið sé óbeygjanlegt
    def is_OBEYGJANLEGT(self, word):
        if not word.lower() in self.wordtags:
            return False
        # fyrir íslensku skal skoða strenginn "OBEYGJANLEGT"
        if isl_or_faer_language == "isl": 
          obeygjanlegt_strengur = "OBEYGJANLEGT"
        # fyrir færeysku skal skoða strenginn "OBENDILIGT"
        elif isl_or_faer_language == "faer": 
          obeygjanlegt_strengur = "OBENDILIGT"
        for tag in self.wordtags[word.lower()]:
            if obeygjanlegt_strengur == tag: 
                return True
        return False
    ######################UPPFÆRSLA######################

    ######################UPPFÆRSLA######################
    # skoða orðflokka
    def is_nafnord(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "hk" == tag or "kk" == tag or "kvk" == tag: 
                return True
        return False

    def is_forsetning(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "fs" == tag: 
                return True
        return False

    def is_personufornafn(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "pfn" == tag: 
                return True
        return False

    def is_onnurfornofn(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "fn" == tag: 
                return True
        return False

    def is_sagnord(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "so" == tag: 
                return True
        return False

    def is_samtenging(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "st" == tag: 
                return True
        return False

    def is_atviksord(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "ao" == tag: 
                return True
        return False

    def is_lysingarord(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "lo" == tag: 
                return True
        return False

    def is_nafnhattarmerki(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "nhm" == tag: 
                return True
        return False

    def is_upphropanir(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "uh" == tag: 
                return True
        return False

    def is_toluord(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "to" == tag: 
                return True
        return False

    def is_radtolur(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "rt" == tag: 
                return True
        return False

    def is_greinir(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "gr" == tag: 
                return True
        return False

    def is_afturbfornafn(self, word):
        if not word.lower() in self.wordtags:
            return False

        for tag in self.wordtags[word.lower()]:
            if "afn" == tag: 
                return True
        return False
    ######################UPPFÆRSLA######################

def slurp(filename, encoding='utf-8'):
    """
    Given a `filename` string, slurp the whole file into a string
    """
    with open(filename, encoding=encoding) as source:
        return source.read()
    

class TreeSplitter(JSONable):

    def __init__(self, text=None, epochs=EPOCHS,
                 classifier=BinaryAveragedPerceptron, **kwargs):
        self.classifier = classifier(**kwargs)
        self.icetags = IceTags()

        if text:

            text = text.replace(',', ' ,')
            text = text.replace(':', ' :')
            text = text.replace('.', ' .')
            self.fit(text, epochs)

    def __repr__(self):
        return "{}(classifier={!r})".format(self.__class__.__name__,
                                            self.classifier)

    @staticmethod
    def candidates(text):
        """
        Given a `text` string, get candidates and context for feature
        extraction and classification
        """

        for Cmatch in finditer(TARGET, text):
            # the conjunction itself
            conjunction = Cmatch.group(2)
            boundary = bool(match(NEWLINE,Cmatch.group(1)))

            # L & R
            start = Cmatch.start()
            end = Cmatch.end()
            Lmatch = search(LTOKEN, text[max(0, start - BUFSIZE):start])
            if not Lmatch:  # this happens when a line begins with '.'
                continue
            left = word_tokenize(Lmatch.group())
            # left = Lmatch.group()

            Rmatch = search(RTOKEN, text[end:end + BUFSIZE])
            if not Rmatch:  # this happens at the end of the file, usually
                continue

            #right = word_tokenize(Rmatch.group(1) + " ")[0]    
            right = word_tokenize(Rmatch.group())  

            # complete observation
            yield Observation(left, conjunction, right, boundary, end)     

    @listify
    def extract_one(self, left, conjunction, right):
        """
        Given left context, conjunction, and right context, 
        extract features. Probability distributions for any
        quantile-based features will not be modified.
        """
        yield "*bias*"
    
        if greinarmerki == "n": 
          if left[1] == ',':
            yield 'L1comma'
        ######################UPPFÆRSLA######################
        # skoða fleiri greinarmerki - skoða greinarmerki á fleiri stöðum en beint fyrir framan aðaltenginguna (þ.e. left[1])
        elif greinarmerki == "y": 
          for element in left:
            element_index = left.index(element)
            element_index_str = str(element_index)
            current_side = "L"

            if element == ";": 
              yield_string = current_side + element_index_str + "semikomma"
              yield yield_string
            if element == ":": 
              yield_string = current_side + element_index_str + "tvipunktur"
              yield yield_string
            if element == "-": 
              yield_string = current_side + element_index_str + "bandstrik"
              yield yield_string
            if element == "?": 
              yield_string = current_side + element_index_str + "spurningamerki"
              yield yield_string
            if element == ".": 
              yield_string = current_side + element_index_str + "punktur"
              yield yield_string
            if element == ",": 
              yield_string = current_side + element_index_str + "komma"
              yield yield_string
            if element == "!": 
              yield_string = current_side + element_index_str + "upphropunarmerki"
              yield yield_string
            if element == "“": 
              yield_string = current_side + element_index_str + "gæsalopp1" # gæsalöpp uppi tvöföld
              yield yield_string
            if element == "\"": 
              yield_string = current_side + element_index_str + "gæsalopp2" # gæsalöpp uppi tvöföld
              yield yield_string
            if element == "„": 
              yield_string = current_side + element_index_str + "gæsaloppnidri" # gæsalöpp niðri
              yield yield_string
            if element == "'": 
              yield_string = current_side + element_index_str + "gæsalopp3" # gæsalöpp uppi einföld
              yield yield_string
          
          for element in right: 
            element_index = right.index(element)
            element_index_str = str(element_index)
            current_side = "R"

            if element == ";": 
              yield_string = current_side + element_index_str + "semikomma"
              yield yield_string
            if element == ":": 
              yield_string = current_side + element_index_str + "tvipunktur"
              yield yield_string
            if element == "-": 
              yield_string = current_side + element_index_str + "bandstrik"
              yield yield_string
            if element == "?": 
              yield_string = current_side + element_index_str + "spurningamerki"
              yield yield_string
            if element == ".": 
              yield_string = current_side + element_index_str + "punktur"
              yield yield_string
            if element == ",": 
              yield_string = current_side + element_index_str + "komma"
              yield yield_string
            if element == "!": 
              yield_string = current_side + element_index_str + "upphropunarmerki"
              yield yield_string
            if element == "“": 
              yield_string = current_side + element_index_str + "gæsalopp1" # gæsalöpp uppi tvöföld
              yield yield_string
            if element == "\"": 
              yield_string = current_side + element_index_str + "gæsalopp2" # gæsalöpp uppi tvöföld
              yield yield_string
            if element == "„": 
              yield_string = current_side + element_index_str + "gæsaloppnidri" # gæsalöpp niðri
              yield yield_string
            if element == "'": 
              yield_string = current_side + element_index_str + "gæsalopp3" # gæsalöpp uppi einföld
              yield yield_string
          ######################UPPFÆRSLA######################

        # finiteness

        for element in left:

          element_index = left.index(element)
          element_index_str = str(element_index)
          current_side = "L"

          if self.icetags.is_finite(element):
            yield_string = current_side + element_index_str + "finite"
            yield yield_string

        for element in right:
          element_index = right.index(element)
          element_index_str = str(element_index)
          current_side = "R"

          if self.icetags.is_finite(element):
            yield_string = current_side + element_index_str + "finite"
            yield yield_string

        # non-finiteness

        for element in left:

          element_index = left.index(element)
          element_index_str = str(element_index)
          current_side = "L"

          if self.icetags.is_nonfinite(element):
            yield_string = current_side + element_index_str + "nonfinite"
            yield yield_string

        for element in right:

          element_index = right.index(element)
          element_index_str = str(element_index)
          current_side = "R"

          if self.icetags.is_nonfinite(element):
            yield_string = current_side + element_index_str + "nonfinite"
            yield yield_string

        # nominative

        for element in left:

          element_index = left.index(element)
          element_index_str = str(element_index)
          current_side = "L"

          if self.icetags.is_nominative(element):
            yield_string = current_side + element_index_str + "nom"
            yield yield_string

        for element in right:

          element_index = right.index(element)
          element_index_str = str(element_index)
          current_side = "R"

          if self.icetags.is_nominative(element):
            yield_string = current_side + element_index_str + "nom"
            yield yield_string

        # oblique

        for element in left:

          element_index = left.index(element)
          element_index_str = str(element_index)
          current_side = "L"

          if self.icetags.is_oblique(element):
            yield_string = current_side + element_index_str + "obl"
            yield yield_string

        for element in right:

          element_index = right.index(element)
          element_index_str = str(element_index)
          current_side = "R"

          if self.icetags.is_oblique(element):
            yield_string = current_side + element_index_str + "obl"
            yield yield_string
        
          ######################UPPFÆRSLA######################
          # skoða orðflokka
        if ordflokkar == "y": 
          for element in left:

            element_index = left.index(element)
            element_index_str = str(element_index)
            current_side = "L"

            if self.icetags.is_nafnord(element):
              yield_string = current_side + element_index_str + "nafnord"
              yield yield_string
            if self.icetags.is_forsetning(element):
              yield_string = current_side + element_index_str + "forsetning"
              yield yield_string
            if self.icetags.is_personufornafn(element): 
              yield_string = current_side + element_index_str + "personufornafn"
              yield yield_string
            if self.icetags.is_onnurfornofn(element): 
              yield_string = current_side + element_index_str + "onnurfornofn"
              yield yield_string
            if self.icetags.is_sagnord(element): 
              yield_string = current_side + element_index_str + "sagnord"
              yield yield_string
            if self.icetags.is_samtenging(element): 
              yield_string = current_side + element_index_str + "samtenging"
              yield yield_string
            if self.icetags.is_atviksord(element): 
              yield_string = current_side + element_index_str + "atviksord"
              yield yield_string
            if self.icetags.is_lysingarord(element): 
              yield_string = current_side + element_index_str + "lysingarord"
              yield yield_string
            if self.icetags.is_nafnhattarmerki(element):
              yield_string = current_side + element_index_str + "nafnhattarmerki"
              yield yield_string
            if self.icetags.is_upphropanir(element):
              yield_string = current_side + element_index_str + "upphropanir"
              yield yield_string
            if self.icetags.is_toluord(element):
              yield_string = current_side + element_index_str + "toluord"
              yield yield_string
            if self.icetags.is_radtolur(element):
              yield_string = current_side + element_index_str + "radtolur"
              yield yield_string
            if self.icetags.is_greinir(element):
              yield_string = current_side + element_index_str + "greinir"
              yield yield_string
            if self.icetags.is_afturbfornafn(element):
              yield_string = current_side + element_index_str + "afturbfornafn"
              yield yield_string

          for element in right:

            element_index = right.index(element)
            element_index_str = str(element_index)
            current_side = "R"

            if self.icetags.is_nafnord(element):
              yield_string = current_side + element_index_str + "nafnord"
              yield yield_string
            if self.icetags.is_forsetning(element):
              yield_string = current_side + element_index_str + "forsetning"
              yield yield_string
            if self.icetags.is_personufornafn(element): 
              yield_string = current_side + element_index_str + "personufornafn"
              yield yield_string
            if self.icetags.is_onnurfornofn(element): 
              yield_string = current_side + element_index_str + "onnurfornofn"
              yield yield_string
            if self.icetags.is_sagnord(element): 
              yield_string = current_side + element_index_str + "sagnord"
              yield yield_string
            if self.icetags.is_samtenging(element): 
              yield_string = current_side + element_index_str + "samtenging"
              yield yield_string
            if self.icetags.is_atviksord(element): 
              yield_string = current_side + element_index_str + "atviksord"
              yield yield_string
            if self.icetags.is_lysingarord(element): 
              yield_string = current_side + element_index_str + "lysingarord"
              yield yield_string
            if self.icetags.is_nafnhattarmerki(element):
              yield_string = current_side + element_index_str + "nafnhattarmerki"
              yield yield_string
            if self.icetags.is_upphropanir(element):
              yield_string = current_side + element_index_str + "upphropanir"
              yield yield_string
            if self.icetags.is_toluord(element):
              yield_string = current_side + element_index_str + "toluord"
              yield yield_string
            if self.icetags.is_radtolur(element):
              yield_string = current_side + element_index_str + "radtolur"
              yield yield_string
            if self.icetags.is_greinir(element):
              yield_string = current_side + element_index_str + "greinir"
              yield yield_string
            if self.icetags.is_afturbfornafn(element):
              yield_string = current_side + element_index_str + "afturbfornafn"
              yield yield_string
          ######################UPPFÆRSLA######################

          ######################UPPFÆRSLA######################
          # skoða hvort orð sé óbeygjanlegt
        if obeygjanlegt == "y": 
          for element in left:
            element_index = left.index(element)
            element_index_str = str(element_index)
            current_side = "L"
  
            yield_string = current_side + element_index_str + "OBEYGJANLEGT"
            if self.icetags.is_OBEYGJANLEGT(element):
                yield yield_string

          for element in right:
            element_index = right.index(element)
            element_index_str = str(element_index)
            current_side = "R"
  
            yield_string = current_side + element_index_str + "OBEYGJANLEGT"
            if self.icetags.is_OBEYGJANLEGT(element):
                yield yield_string
          ######################UPPFÆRSLA######################


    def fit(self, text, epochs=EPOCHS):
        """
        Given a string `text`, use it to train the segmentation classifier
        for `epochs` iterations.
        """
        logging.debug("Extracting features and classifications.")
        Phi = []
        Y = []
        for (left, conjunction, right, gold, _) in self.candidates(text):
            Phi.append(self.extract_one(left, conjunction, right))
            Y.append(gold)
        self.classifier.fit(Y, Phi, epochs)
        logging.debug("Fitting complete.")
    

    def predict(self, left, conjunction, right):
        """
        Given an left context `L`, punctuation mark `P`, and right context
        `R`, return True iff this observation is hypothesized to be a
        sentence boundary.
        """
        phi = self.extract_one(left, conjunction, right)
        return self.classifier.predict(phi)


    def segments(self, text, strip=True):
        """
        Given a string of `text`, return a generator yielding each
        hypothesized sentence string
        """
        start = 0
        for (L, conjunction, R, B, end) in self.candidates(text):
            if self.predict(L, conjunction, R):
                sent = text[start:end-len(conjunction)-2]
                if strip:
                    sent = sent.rstrip()
                yield sent
                start = end-len(conjunction)-1
            # otherwise, there's probably not a sentence boundary here
        sent = text[start:]
        if strip:
            sent = sent.rstrip()
        yield sent

    def evaluate(self, text):
        """
        Given a string of `text`, compute confusion matrix for the
        classification task.
        """
        cx = BinaryConfusion()
        for (L, P, R, gold, _) in self.candidates(text):
            guess = self.predict(L, P, R)
            cx.update(gold, guess)
            if not gold and guess:
                logging.debug("False pos.: L='{}', R='{}'.".format(L, R))
            elif gold and not guess:
                logging.debug("False neg.: L='{}', R='{}'.".format(L, R))
        return cx
        
placeholder_output_txtfile = sys.argv[9] 
placeholder_output_psdfile = sys.argv[10] 
INPUT_FILE = sys.argv[11] # þetta er nafnið á textaskránni sem inniheldur setningarnar sem á að splitta í aðalsetningar

if train_or_split == "train": 
  # Kóði til að þjálfa Splitterinn
  tsplitter = TreeSplitter(slurp(TRAIN_FILE))
  tsplitter.dump(MODEL_NAME)
elif train_or_split == "split": 
  # Kóði til að keyra splitterinn (þ.e. til að splitta setningum í aðalsetningar)
  tsplitter = TreeSplitter.load(MODEL_NAME) # í .load() skipuninni er verið að lesa inn módelið # var upphaflega sys.argv[1]
  output = "\n".join(tsplitter.segments(slurp(INPUT_FILE))) # INPUT_FILE var upphaflega sys.argv[2]
  output = re.sub(r'\n+','\n',output).strip()
  #print(output)
  with open(placeholder_output_txtfile,"w",encoding="utf-8") as fileforoutput: 
    fileforoutput.write(output)
