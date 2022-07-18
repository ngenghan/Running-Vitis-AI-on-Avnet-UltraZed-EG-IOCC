from tensorflow_model_optimization.quantization.keras import vitis_quantize
from tensorflow.keras.models import load_model

from dataset_utils import input_fn_quant

# Path to pre-trained model
PRETRAINED_MODEL_PATH='float_model/f_model.h5'
# Path to save quantised model.
QUANTISED_MODEL_PATH='q_model.h5'
# Path to tf-Records.
TF_RECORD_PATH='tfrecords'
BATCHSIZE=50

# Load the pre-trained model
PRETRAINED_MODEL_PATH = load_model(PRETRAINED_MODEL_PATH)

# get input dimensions of the floating-point model
height = PRETRAINED_MODEL_PATH.input_shape[1]
width = PRETRAINED_MODEL_PATH.input_shape[2]

# Use dataset_utils.py provided to pre-process dataset
quant_dataset = input_fn_quant(TF_RECORD_PATH, BATCHSIZE, height, width)

# Quantization using vai_q_tensorflow2
quantizer = vitis_quantize.VitisQuantizer(PRETRAINED_MODEL_PATH)
quantized_model = quantizer.quantize_model(calib_dataset=quant_dataset)

# Save quantized model in specified path.
quantized_model.save(QUANTISED_MODEL_PATH)
