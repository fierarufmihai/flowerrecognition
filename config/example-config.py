# GPU
RUN_ON_GPU = 1

# IPs and PORTs
BACKEND_IP = "192.168.33.181"
BACKEND_PORT = 8802
FRONTEND_IP = "0.0.0.0"
FRONTEND_PORT = 8999
BACKEND_PORT_ON_FRONTEND = 8803

# Caffe paths
CAFFE_PATH = '/scratch/fieraru/caffe-master/'
PYTHON_CAFFE_PATH = CAFFE_PATH + "python"
MODEL_PATH = CAFFE_PATH + "models/bvlc_googlenet/"
NET_FN = MODEL_PATH + 'deploy.prototxt'
PARAM_FN = MODEL_PATH + 'bvlc_googlenet.caffemodel'

# Data paths
OUTPUT_ROOT = '../data/after/'
TMP_MODEL_FN = '../config/tmp.prototxt'
