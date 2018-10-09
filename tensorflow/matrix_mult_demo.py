# import tensorflow library with alias tf
import tensorflow as tf

# Define two random matrices of 2X2 dimension
matrix1 = tf.constant([[1, 2], [4, 5]], name="Matrix1")
matrix2 = tf.constant([[7, 8], [1, 2]], name="Matrix2")

# Multiply two matrices
result = tf.matmul(matrix1, matrix2)

# Get session and execute above operation in Session
session = tf.Session()
print session.run(result)

# Serialize graph to current directory to visualize into Tensorboard
writer = tf.summary.FileWriter('.')
writer.add_graph(tf.get_default_graph())
