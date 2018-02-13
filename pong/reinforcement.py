#!/home/kevin/Desktop/SelfDrivingCar/keras/bin/python
from collections import deque
import tensorflow as tf
import numpy as np
import random
import pong
# image config
from skimage.transform import resize
from skimage.filters import threshold_mean
from skimage.color import rgb2gray

# keras in tensorflow
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D, Dense, Dropout, Flatten
from tensorflow.python.keras.optimizers import Adam

# configure GPU memory
from tensorflow.python.keras.backend import set_session
gpu_options = tf.GPUOptions( per_process_gpu_memory_fraction = 0.5 )
set_session( tf.Session( config = tf.ConfigProto( gpu_options = gpu_options ) ) )

ACTION = 1
# Learning Rate
GAMMA = 0.01

BATCH = 5
IMAGE_SIZE = ( 80, 80, 1 )

# Network model
def Model():
    model = Sequential()
    model.add( Conv2D( 32, ( 8, 8 ), activation = 'relu', input_shape = IMAGE_SIZE ) )
    model.add( Conv2D( 64, ( 4, 4 ), activation = 'relu' ) )
    model.add( Conv2D( 64, ( 3, 3 ), activation = 'relu' ) )
    model.add( Flatten() )
    model.add( Dense( 784, activation = 'relu' ) )
    model.add( Dense( ACTION ) )
    model.summary()
    return model

def PlayGame( model ):

    # get init image
    reward, image, end = pong.sweet( 10 )
    image = rgb2gray( image )
    image = resize( image, ( 80, 80 ) )
    thresh = threshold_mean( image )
    binary = image > thresh
    binary = np.expand_dims( binary, axis = 2 )

    reward = 0
    policy_images = []
    policy_action = []
    while True:
        action = model.predict( np.expand_dims( binary, axis = 0 ) )
        reward_now, nextImage, end = pong.sweet( action )
        if end:
            break
        policy_images.append( binary )
        policy_action.append( action )
        if reward_now > reward:
            reward = reward_now

        nextImage = rgb2gray( nextImage )
        nextImage = resize( image, ( 80, 80 ) )
        thresh = threshold_mean( nextImage )
        binary = nextImage > thresh
        binary = np.expand_dims( binary, axis = 2 )

    return reward, np.asarray( policy_images ), np.asarray( policy_action )

def trainGraph( reward, images, labels ):
    # learning rate
    if reward < 1:
        alpha = -0.01
    else:
        alpha = reward * GAMMA
    alpha_labels = labels * alpha

    model.compile( loss = 'mean_squared_error', optimizers = Adam(1e-6), metrics = ['loss'] )

    model.fit( images, alpha_labels, batch_size = BATCH, epochs = 1, verbose = 1 )

    model.save('model-reinforcement.h5')

if __name__ == '__main__':
    model = Model()
    for i in range(100):
        reward, image, label = PlayGame( model )
        trainGraph( reward, image, label )


