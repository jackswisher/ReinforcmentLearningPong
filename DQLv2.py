import tensorflow as tf
import cv2
import pong
import numpy as np
import random
import os
import time
import sys
from collections import deque
from numpy.random import choice

# Based off: https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf
# and https://www.youtube.com/watch?v=Hqf__FlRlzg (this was in python 2 and nonfunctional)

# how many FPS the game should maximally run at
FPS = 60

# define hyper paramaters for neural net
ACTIONS = 3

# learning rate
GAMMA = 0.99

# how much to rely on the neural net
INITIAL_EPSILON = 1.0
FINAL_EPSILON = 0.05

# define how many frames to observe/train
EXPLORE = 10000
OBSERVE = 1000

# how often to save the state of the neural net
SAVE_STEP = 10000

# how many experiences to store
REPLAY_MEMORY = 200000

# how large the batches should be to train on
BATCH_SIZE = 60


def createNetwork():
    # with tf.device('/gpu:0'):
    # want a 5 hidden layer neural net, 3 convolutional layers (Shape from Google's Deep Mind)
    inp = tf.placeholder("float", [None, 60, 60, 4])

    # given 6 x 6 patch and 4 channels => 32 features
    conv1_W = tf.Variable(tf.truncated_normal([6, 6, 4, 32], stddev=0.02))
    conv1_b = tf.Variable(tf.constant(0.1, shape=[32]))

    # given 4 x 4 patch and 32 channels (features) => 64 features
    conv2_W = tf.Variable(tf.truncated_normal([4, 4, 32, 64], stddev=0.02))
    conv2_b = tf.Variable(tf.constant(0.1, shape=[64]))

    # given 3 x 3 patch and 64 channels => 64 features
    conv3_W = tf.Variable(tf.truncated_normal([3, 3, 64, 64], stddev=0.02))
    conv3_b = tf.Variable(tf.constant(0.1, shape=[64]))

    # first fully connected layer, will follow the conversion to a flat layer of 1024
    fc4_W = tf.Variable(tf.truncated_normal([1024, 512], stddev=0.02))
    fc4_b = tf.Variable(tf.constant(0.1, shape=[512]))

    # second fully connected layer, will act as our output layer
    out_W = tf.Variable(tf.truncated_normal([512, ACTIONS], stddev=0.02))
    out_b = tf.Variable(tf.constant(0.1, shape=[ACTIONS]))

    # create input layer, first convolutional layer
    conv1 = tf.nn.relu(tf.nn.conv2d(inp, conv1_W, strides=[1, 4, 4, 1], padding="SAME") + conv1_b)

    # create first pooling layer
    pool1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

    # second convolutional layer
    conv2 = tf.nn.relu(tf.nn.conv2d(pool1, conv2_W, strides=[1, 2, 2, 1], padding="SAME") + conv2_b)

    # third convolutional layer
    conv3 = tf.nn.relu(tf.nn.conv2d(conv2, conv3_W, strides=[1, 1, 1, 1], padding="SAME") + conv3_b)

    # flatten the layer
    conv3_flat = tf.reshape(conv3, [-1, 1024])

    # fully connected layer
    fc4 = tf.nn.relu(tf.matmul(conv3_flat, fc4_W) + fc4_b)

    # output layer
    out = tf.matmul(fc4, out_W) + out_b

    return inp, out


def trainNetwork(inp, out, user_playing, use_model, filename):
    # initialize global variables
    argmax = tf.placeholder("float", [None, ACTIONS])

    # define ground truth
    gt = tf.placeholder("float", [None])

    # globally define a variable to store how many iterations have been done
    global_time = tf.Variable(0, name='global_time')

    # define optimization and cost functions (simple quadratic cost function)
    action = tf.reduce_sum(tf.multiply(out, argmax), reduction_indices=1)
    cost = tf.reduce_mean(tf.square(action - gt))
    train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)

    # initialize game and replay queue
    game = pong.PongGame(user_playing)
    replay = deque()

    # given the frame data, want to convert it to greyscale and crop to 60 x 60
    frame = game.getCurrentFrame()
    frame = cv2.cvtColor(cv2.resize(frame, (60, 60)), cv2.COLOR_BGR2GRAY)
    ret, frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)

    # create input tensor using numpy to stack four frames
    inp_t = np.stack((frame, frame, frame, frame), axis=2)

    # implement saver
    sess = tf.InteractiveSession(config=tf.ConfigProto(log_device_placement=True))
    saver = tf.train.Saver(tf.global_variables(), max_to_keep=None)

    # If filename specified, try and load that
    if filename is not None:
        checkpoint = './saves/' + filename
    else:
        # try and restore latest checkpoint
        checkpoint = tf.train.latest_checkpoint('./saves')

    if checkpoint != None:
        # was able to retrieve save
        saver.restore(sess, checkpoint)
    else:
        # no checkpoint found, initialize new neural network
        init = tf.global_variables_initializer()
        sess.run(init)

    t = global_time.eval()
    numIterations = 0
    epsilon = INITIAL_EPSILON

    while True:
        starttime = time.time()
        # feed the input tensor into the neural network (only one index)
        out_t = out.eval(feed_dict={inp: [inp_t]})[0]

        # create an empty tensor of size ACTIONS
        argmax_t = np.zeros([ACTIONS])

        # if < epsilon then random action, otherwise predicted action
        if random.random() <= epsilon and not use_model:
            index = choice((0, 1, 2), p=(0.9, 0.05, 0.05))
        else:
            index = np.argmax(out_t)

        # update epsilon
        if epsilon > FINAL_EPSILON:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        # set the corresponding position to 1 corresponding to the desired action
        argmax_t[index] = 1

        if use_model:
            mode = 'Model Only'
        elif numIterations > OBSERVE:
            mode = 'Exploring'
        else:
            mode = 'Observing'

        # retrieve next frame
        reward_t, frame = game.getNextFrame(argmax_t, [t, np.max(out_t), epsilon, mode])
        frame = cv2.cvtColor(cv2.resize(frame, (60, 60)), cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(frame, 1, 255, cv2.THRESH_BINARY)
        frame = np.reshape(frame, (60, 60, 1))

        # create a new input tensor by adding the new frame and keeping previous three frames
        newinp_t = np.append(frame, inp_t[:, :, 0:3], axis=2)

        # store experience in queue for later
        replay.append((inp_t, argmax_t, reward_t, newinp_t))

        # if we run out of memory, pop the oldest one and add new experience
        if len(replay) > REPLAY_MEMORY:
            replay.popleft()

        if numIterations > OBSERVE and not use_model:
            # have stored enough experiences, time to train using stored memories!!!!
            training_batch = random.sample(replay, BATCH_SIZE)

            # break it up into seperate lists and create a batch for ground truths
            inp_batch, argmax_batch, reward_batch, newinp_batch, gt_batch = [], [], [], [], []

            for current in training_batch:
                inp_batch.append(current[0])
                argmax_batch.append(current[1])
                reward_batch.append(current[2])
                newinp_batch.append(current[3])

            # create a batch for the outputs (will be used to train)
            out_batch = out.eval(feed_dict={inp: newinp_batch})

            # the ground truth is found using the formula gt = reward + gamma * Qmax (of next frame)
            for i in range(len(training_batch)):
                gt_batch.append(reward_batch[i] + GAMMA * np.max(out_batch[i]))

            # training time, feed the batches to the train_step we defined earlier (will go where placeholders were)
            train_step.run(feed_dict={argmax: argmax_batch, gt: gt_batch, inp: inp_batch})

        # update the input tensor and increment t and numIterations
        inp_t = newinp_t
        t += 1
        numIterations += 1

        # if it is time to save the state, do so
        if t % SAVE_STEP == 0 and not use_model:
            sess.run(global_time.assign(t))
            saver.save(sess, './saves/model.ckpt', global_step=t)

        endtime = time.time()
        difference = endtime - starttime
        if use_model and difference < (1 / FPS):
            time.sleep((1 / FPS) - difference)

        print("TIMESTEP", t, "/ EPSILON", epsilon, "/ ACTION", index,
              "/ REWARD", reward_t, "/ Q_MAX %e" % np.max(out_t))


def main():
    # input layer and output layer by creating graph
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python DQLv2.py user_playing use_model filename (optional)")
        exit(1)

    user_playing = sys.argv[1]
    use_model = sys.argv[2]

    # try making them booleans, if it fails print an error
    if user_playing == 'True':
        user_playing = True
    elif user_playing == 'False':
        user_playing = False
    else:
        print("Arguments could not be parsed as booleans")
        exit(1)

    # try and make use_model a boolean
    if use_model == 'True':
        use_model = True
    elif use_model == 'False':
        use_model = False
    else:
        print("Arguments could not be parsed as booleans")
        exit(1)

    inp, out = createNetwork()

    # if they specify a filename use it, otherwise pass over None
    if len(sys.argv) == 3:
        filename = None
    else:
        filename = sys.argv[3]

    # train our graph on input and output with session variables
    trainNetwork(inp, out, user_playing, use_model, filename)


if __name__ == "__main__":
    main()