"""
    Speech-To-Text class handling for AVA

    STT: We are using CMUSphinx opensource library
    CMUSphinx:
        - English language model
        - Customize dictionnary
"""

from os import path
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "/usr/local/share/pocketsphinx/model/"
HMM_DIR = MODELDIR + "en-us/en-us"


class STT_Engine_Offline():
    """
    PocketSphinx Speech-To-Text implementation
    """

    def __init__(self):
        # Checking if Hidden Markov Model directory exists
        if not path.exists(HMM_DIR):
            print("hmm_dir in '%s' does not exist!"%HMM_DIR)
            raise EnvironmentError

        # Checking for missing files in hmm directory
        missing_hmm_files = []
        for missing_file in ('feat.params', 'mdef', 'means', 'noisedict',
                      'transition_matrices', 'variances'):
            if not path.exists(path.join(HMM_DIR, missing_file)):
                missing_hmm_files.append(missing_file)
        ## plus files we are partially dependent
        mixweights = path.exists(path.join(HMM_DIR, 'mixture_weights'))
        sendump = path.exists(path.join(HMM_DIR, 'sendump'))

        if not mixweights and not sendump:
            missing_hmm_files.append('mixture_weights or sendump')
        if missing_hmm_files:
            print("[Warning] %s : hmm files are missing in hmm directory.", ', '.join(missing_hmm_files))

        # Decoding configuration instance and config if everything is OK
        self.config = Decoder.default_config()
        self.config.set_string('-hmm', path.join(HMM_DIR))
        self.config.set_string('-lm', path.join(MODELDIR , 'en-us/en-us.lm.bin'))
        self.config.set_string('-dict', path.join('ava/static/custom.dict'))
        self.config.set_string('-logfn', '/dev/null')
