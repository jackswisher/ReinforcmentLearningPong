DESIGN Document:
pong.py:
Sizes of our window, paddle and ball, and initial speeds for our ball and paddle were declared at the top in the form of constants. This was so that later in the code they can be referred to by their name and not by some number that would not be obvious what it would be for. The ball, paddle, and screen are all white and black to keep it in line with the original pong game (example at ponggame.org) as well as to keep the computer vision fairly simple.

Separate functions for drawing each of the paddles and the ball were defined. This was done so that when called later to update the position of a certain paddle or the ball, they could be called to be drawn in the new position based on the movement that occurred.

The function updateBall was defined to update the position of the ball based on whether a collision had occurred or not. If a collision did indeed occur between a paddle and the ball, different scores were assigned based on which paddle hit it and which let it in. If the ball hits the paddle, the speed of the ball increases by a constant declared at the start (1.1) as if to emulate an increase in difficulty as the game progresses. If a ball gets past the paddle, the ball would restart from the middle of the page and move in a random direction.

The function updatePaddle1 is passed an array of possible actions where the array contains the value 1 in only one of its 3 indices. The first index, action[0], corresponds to no movement, action[1] refers to moving up and, action[2] refers to moving it down.

The function updatePaddle2 would check to see whether a user is playing the role of the second paddle (on the right) or whether it is a CPU. If a CPU is playing, the code therein specifies that the paddle just moves to the top of the page if the ball is there and the bottom of the page if the ball is there (it essentially follows the ball). However, for the user controlled paddle the arrow "up" and "down" keys are used to control the paddle's movement.

Within a class called Ponggame, two functions, getCurrentFrame and getNextFrame, are defined which are very self explanatory. The function getCurrentFrame gets the current frame of the game by drawing the paddles, ball and gets the pixels and returns them. The function getNextFrame just gets the next frame after the current frame by first applying any updates to the position of the ball and the paddle and then updating the frame to show the new data by calling getCurrentFrame again (after the updates are made). Lastly, a quit button is added so that the user can exit the game by clicking the “X” on the top right corner of the game’s page.

Another design decision that was made was whether we would call x and y positions of the paddle and ball as separate variables or refer to them as elements of an array. For example, instead of ballPosition = [x-coordinate, y-coordinate], where ballPosition[0] would be what we called ballXPosition and ballPosition[1] would be what we called ballYPosition, we named two separate variables, ballXPosition and ballYposition as it seemed like more of a hassle without much benefit. Another possibility would to store them as tuples. This might be a good improvement for the future.


DQLv2.py:
At the most general level, we decided to use Deep Q learning for our network. The architecture of the network was modeled after Google’s Deepmind (https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf). It uses a 5 hidden layer neural network with three convolutional layers, a max pooling layer, and a fully connected layer. The shape of network is fairly well defined given our inputs and mirrors the Deepmind network in many ways. The input tensor is constructed by stacking the previous four frames using numpy with 2 axises. The reason for the 4-D input is so the network can see the movement of the ball, otherwise it would be impossible to infer which direction the ball was moving and how quickly. The first layer is a convolutional layer with a 6x6 patch that moves along the input tensor and produces 32 features. The second layer is a max pooling layer that moves along the image in a 2x2 patch and chooses the max value from the patch. The third layer is a convolutional layer with a 4x4 patch that moves along the features from the max pooling layer and generates 64 features. Following this, a convolutional layer with a 3x3 patch evaluates the output of the second convolutional layer and generates 64 features. The purpose of these stacked convolutional layers is to generate multiple features and refine the feature map. Different neurons are connected to different parts of the feature map, this allows for the neural net to learn where the ball is and where the paddle is and control the paddle to maximize reward. Following the last convolutional layer, the layer is flattened using numpy with 1024 neurons. A fully connected layer is made by applying our ReLu activation function on the result of the matrix multiplication of the flattened layer with the weights for the fully connected layer. Each of these layers (besides the pooling layer) has a bias vector due to the use of the ReLu activation function which does not do well with really small inputs. Finally, the output is calculated by multiplying the last layer with its weights and has a shape of ACTIONS (which is 3 for this problem).

The idea behind training is to minimize the cost, which we define as a simple quadratic cost function and use the Adam optimizer included with TensorFlow to minimize the cost. If a random number is less than epsilon, the program will perform a weighted random action. Otherwise, the action taken is determined by calculating which output in the output tensor is the largest and creating an array where that index is 1 and the rest are 0s. The purpose of this is to begin with random actions and slowly begin relying more and more on the neural net as the neural net is being trained. The reward tensor is retrieved by getting the next frame given the calculated argmax tensor and the necessary info to display. A tuple of the input tensor, the argmax tensor, reward tensor, and the following frame’s tensor is added to a queue for later training.

For the first OBSERVE frames, the program simply stores these experiences in the queue. Following the OBSERVE period, the neural network is trained by retrieving a random sample of size BATCH_SIZE from the queue and calculating the ground truth (what the network should have chosen) based on the result of the next frame. The formula for the ground truth is defined as reward + learning rate * Qmax(output of next frame). Qmax is simply the max value in the output tensor. To train the net, the action chosen (argmax tensor), the ground truth, and the input are fed into the Adam optimizer we defined earlier. This is done using TensorFlow’s feed_dict which puts the tensors into the places of what previously were placeholders. The reason for training this way is a result of the type of problem we are solving. Pong has a delayed reward system, meaning we don’t know whether the action we took was right at the time or not. This is where Deep Q learning comes in. By storing past experiences in a queue and using these to train the neural net through backpropagation, we are able to discourage the actions that led to a negative reward and encourage the actions that led to a positive reward given the input. Epsilon decreases from INITAL_EPSILON to FINAL_EPSILON by even increments during the following OBSERVE frames. The purpose of this is to give the network time to explore what random actions will do and how they influence the reward. On that note, we decided to reward the network one point if it hit the ball or beat the opponent and had it lose a point if the ball hit the wall behind its paddle. Originally, there was no reward for hitting the ball, but training times were quite slow as the network did not receive many positive rewards and actions were rarely encouraged and often discouraged by the proportionally great negative rewards.

We used the inbuilt saver in TensorFlow to save the neural network weights, bias vectors, and the current gobal_time. We decided to save the global variables every SAVE_STEP iterations. Each of the hyperparameters could probably be optimized to improve training time and performance, however the current configuration seems to approach a functional AI given a couple hours of training time. We also implemented command line arguments that must be passed when the program is run called user_playing and use_model. User_playing designates whether the neural network should play against a player or a basic AI that moves up if the ball is in the top part of the paddle and down if it is in the lower part. This allows the network to be trained without human supervision and then demoed with real people playing against the neural network. The second parameter details whether to use the network model without training. This allows for it to be demoed at full speed without being bogged down with constant training. Additionally, the program calculates the time passed between each frame being presented, which we use to cap the framerate by using the time.sleep() function. We encountered an issue where the game would run too quickly when not training, so this is a way to cap the framerate and keep the game running. Another option would have to been to use the FPS library, but it would have been more complicated to calculate how long had passed and only delay by the right time to get FPS (designated above the hyper parameters) number of frames a second.