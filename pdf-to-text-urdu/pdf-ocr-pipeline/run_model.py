"""
Modified By : M.Zeeshan Javed
Date : Mar-09-2022
Description : Code is optimized by removing not used libraries and also did change
to do prediction on news strips so that it can be integrated with the module.
"""

import os
import time
import logging


# Import python scripts from utils and models folder
from .utils.config_utils import get_config
from .models.cnn_rnn_ctc import CNN_RNN_CTC
from .models.rnn_ctc import RNN_CTC
from .models.encoder_decoder import Encoder_Decoder
# logging.basicConfig(level=logging.INFO)


def create_and_run_model(model_config_path):
    # print("run_mode.py -> create_and_run_model")
    # if eval_path is not None and infer:
    #     raise Exception("Both infer_path and eval_path are set. But cannot infer and evaluate at the same time.")

    mappings = {'CNN_RNN_CTC': CNN_RNN_CTC, 'RNN_CTC': RNN_CTC, 'Encoder_Decoder': Encoder_Decoder}
    # Read all the configurations from config_name
    # print("    -- reading configs")
    config = get_config(model_config_path)

    eval_path = None
    # ** Loading the model for example if CNN_RNN_CTC is called the model from /models/cnn_rnn_ctc.py will be loaded
    model = mappings[config.model](config, eval_path, infer= True)

    return model, config


def _setup_logging(config, use_previous_log):
    name = config.model
    save_dir = config.save_dir

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not use_previous_log and os.path.isfile(os.path.join(save_dir, name + ".log")):
        os.remove(os.path.join(save_dir, name + ".log"))

    file_handler = logging.FileHandler(os.path.join(save_dir, name + ".log"))
    logging.getLogger().addHandler(file_handler)


def recognize_strip(model_config_path, image_strip):
    # print("run_model.py -> recognize_strip")
    # EVALUATING THE MODEL
    model, config = create_and_run_model(model_config_path)
    # tic = time.time()
    out, urdu_out = model(image_strip)
    # toc = time.time()
    # print("Inferring time: ", toc - tic)
    return out, urdu_out[0]
