README for Reinforcement Learning Pong

IMPORTANT NOTE: NOT MEANT TO BE RUN ON IDE (IDE does not have a video device)

VIDEO LINK: https://youtu.be/Rs1_vVvQ4P0

The purpose of Pong is to hit the ball and get the ball past your opponent's paddle without letting the ball past your own. Our project implements a five hidden layer deep neural network that uses Deep Q Learning to play Pong. For more information on how it works, refer to DESIGN.md.

## REQUIRED PACKAGES TO INSTALL
pygame

numpy

tensorflow

cv2

## INSTALLATION
To install the required packages type the below into a terminal window:

pip install pygame

pip install numpy

pip install tensorflow

pip install opencv-python

Note: this does not install the gpu version of tensorflow, as that version requires an NVIDIA GPU that meets all of the required specifications. If you would wish to do so, refer to the documentation as it varies from system to system. On windows, you need to have NVIDIA CUDA 7.x installed and to add the install location to your local PATH variables.
Documentation for install: https://www.tensorflow.org/install/


## SETUP FOR GPU VERSION
Uncomment line 45 'with tf.device('/gpu:0'):'

Indent the rest of the block to be one indent to the right of the above code


## CONTROLS
When controlled by the user, the right paddle moves up with the up arrow key and down with the down arrow key.


## USAGE
In the samples file there are three samples for different states of the neural network. They correspond to the following.

Early stage: pass over early as filename

Middle stage: pass over middle as filename

Late stage: pass over late as filename (or do not pass a filename)

Example usage: python DQLv2.py False True early

To use these files, specify the desired filename as the last parameter or do not include a filename to use the latest model

Usage: python DQLv2.py user_playing use_model filename (optional)
	- Where user_playing is a boolean that if True lets the user control the paddle and if false uses the basic AI.
	- Where use_model is a boolean specifying whether to use the model without training. True uses the most recent checkpoint and does not train. False uses most recent checkpoint but trains while running.
	- Where filename corresponds to the filename you wish to use in saves. More details can be found above.

### Examples:
To test the neural network against a simple AI using the model:
- Navigate to the Final Project directory
- Run the following in terminal: python DQLv2.py False True

To play against the neural network:
- Navigate to the Final Project directory
- Run the following in terminal: python DQLv2.py True True

To train the neural network against AI:
- Navigate to the Final Project directory
- Run the following in terminal: python DQLv2.py False False

To personally train the neural network (very time-consuming , not recommended)
- Navigate to the Final Project directory
- Run the following in terminal: python DQLv2.py True False

This should bring up a game window with the neural network playing on the left in all instances.


REFERENCES
https://inventwithpython.com/makinggames.pdf
https://www.youtube.com/watch?v=Hqf__FlRlzg
https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf
https://www.youtube.com/watch?v=Ih8EfvOzBOY
https://github.com/hamdyaea/Daylight-Pong-python3/blob/master/DaylightPong.py
https://medium.com/@dhruvp/how-to-write-a-neural-network-to-play-pong-from-scratch-956b57d4f6e0
http://karpathy.github.io/2016/05/31/rl/

