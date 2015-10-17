import sys
import json
import os
import math
import numpy as np


from array import *
from collections import OrderedDict

sys.path.append("../../../config")
import config
import caffe

class FlowerRecognition(object):
    def __init__(self):
        self.device = 'CPU'
        if config.RUN_ON_GPU:
            self.device = 'GPU 0'

        self.classes = ['pink primrose', 'hard-leaved pocket orchid', 'canterbury bells', 'sweet pea', 'english marigold', 'tiger lily', 'moon orchid', 'bird of paradise', 'monkshood', 'globe thistle', 'snapdragon', "colt's foot", 'king protea', 'spear thistle', 'yellow iris', 'globe-flower', 'purple coneflower', 'peruvian lily', 'balloon flower', 'giant white arum lily', 'fire lily', 'pincushion flower', 'fritillary', 'red ginger', 'grape hyacinth', 'corn poppy', 'prince of wales feathers', 'stemless gentian', 'artichoke', 'sweet william', 'carnation', 'garden phlox', 'love in the mist', 'mexican aster', 'alpine sea holly', 'ruby-lipped cattleya', 'cape flower', 'great masterwort', 'siam tulip', 'lenten rose', 'barbeton daisy', 'daffodil', 'sword lily', 'poinsettia', 'bolero deep blue', 'wallflower', 'marigold', 'buttercup', 'oxeye daisy', 'common dandelion', 'petunia', 'wild pansy', 'primula', 'sunflower', 'pelargonium', 'bishop of llandaff', 'gaura', 'geranium', 'orange dahlia', 'pink-yellow dahlia?', 'cautleya spicata', 'japanese anemone', 'black-eyed susan', 'silverbush', 'californian poppy', 'osteospermum', 'spring crocus', 'bearded iris', 'windflower', 'tree poppy', 'gazania', 'azalea', 'water lily', 'rose', 'thorn apple', 'morning glory', 'passion flower', 'lotus', 'toad lily', 'anthurium', 'frangipani', 'clematis', 'hibiscus', 'columbine', 'desert-rose', 'tree mallow', 'magnolia', 'cyclamen ', 'watercress', 'canna lily', 'hippeastrum ', 'bee balm', 'ball moss', 'foxglove', 'bougainvillea', 'camellia', 'mallow', 'mexican petunia', 'bromelia', 'blanket flower', 'trumpet creeper', 'blackberry lily']

        caffe.set_mode_cpu()
        self.net = caffe.Net(config.CAFFE_PATH + 'models/oxford102/deploy.prototxt',
                config.CAFFE_PATH + 'models/oxford102/oxford102.caffemodel',
                caffe.TEST)

        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2,0,1))
        self.transformer.set_mean('data', np.load(config.CAFFE_PATH + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
        self.transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
        self.transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
        self.net.blobs['data'].reshape(50,3,227,227)


    def run(self, img_filename):
        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', caffe.io.load_image(img_filename))
        output = self.net.forward()
        return self.classes[(output["fc8_oxford_102"][0]).argmax()]

def main(argv):
    input_fn = argv[1]

    # Run the magic
    flowerrecognition = FlowerRecognition()

    print flowerrecognition.run(input_fn)


if __name__ == "__main__":
    main(sys.argv)


