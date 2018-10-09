import collections
# Import TensorFlow library
import tensorflow as tf


# Define CSV column data types.
# Since CSV readers are sensitive to ordering of columns, OrderedDict is used
column_types = collections.OrderedDict([
    ("date", [""]),
    ("Appliances", [0]),
    ("lights", [0]),
    ("T1", [0.0]),
    ("RH_1", [0.0]),
    ("T2", [0.0]),
    ("RH_2", [0.0]),
    ("T3", [0.0]),
    ("RH_3", [0.0]),
    ("T4", [0.0]),
    ("RH_4", [0.0]),
    ("T5", [0.0]),
    ("RH_5", [0.0]),
    ("T6", [0.0]),
    ("RH_6", [0.0]),
    ("T7", [0.0]),
    ("RH_7", [0.0]),
    ("T8", [0.0]),
    ("RH_8", [0.0]),
    ("T9", [0.0]),
    ("RH_9", [0.0]),
    ("T_out", [0.0]),
    ("Press_mm_hg", [0.0]),
    ("RH_out", [0.0]),
    ("Windspeed", [0.0]),
    ("Visibility", [0.0]),
    ("Tdewpoint", [0.0]),
    ("rv1", [0.0]),
    ("rv2", [0.0])
])


def map_line_to_dict(line):
    """
    Converts input line to CSV and then to Dictionary.

    :param line: to parse as CSV and to be converted to dict
    :return: Dictionary of CSV header names and their values
    """
    mapped_values = tf.decode_csv(line, column_types.values())
    return dict(zip(column_types.keys(), mapped_values))


# Path to dataset
URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/00374/energydata_complete.csv"
path = tf.contrib.keras.utils.get_file(URL.split("/")[-1], URL)

# Following line does not read data yet, it is more
dataset = (tf.data
           .TextLineDataset(path)   # Create text line Dataset from file URL
           .skip(1)     # Skip first header line
           .map(map_line_to_dict)   # Convert line to dictionary
           .cache()     # Cache conversion of line to dictionary for optimized read
           )

# Make one shot iterator to get all data
iterator = dataset.make_one_shot_iterator()
next_element = iterator.get_next()

# Get TensorFlow session to get next element
session = tf.Session()

try:
    while True:     # Running an infinite loop to read all the data from iterator
        data_dict = session.run(next_element)
        print data_dict
except tf.errors.OutOfRangeError as oore:   # Error will be thrown once we reach end of iterator
    pass
