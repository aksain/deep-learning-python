import tensorflow as tf
import numpy as np
import collections


# Define CSV column data types
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

# Path to dataset
URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/00374/energydata_complete.csv"
path = tf.contrib.keras.utils.get_file(URL.split("/")[-1], URL)

base_dataset = tf.data.TextLineDataset(path)

print base_dataset

#def get_train_test_dataset():
    


def main(argv):
  """Builds, trains, and evaluates the model."""



  # Build the training input_fn.
  def input_train():
    return (
        # Shuffling with a buffer larger than the data set ensures
        # that the examples are well mixed.
        train.shuffle(1000).batch(128)
        # Repeat forever
        .repeat().make_one_shot_iterator().get_next())

  feature_columns = [
      # "curb-weight" and "highway-mpg" are numeric columns.
      tf.feature_column.numeric_column(key="curb-weight"),
      tf.feature_column.numeric_column(key="highway-mpg"),
  ]

  # Build the Estimator.
  model = tf.estimator.LinearRegressor(feature_columns=feature_columns)

  # Train the model.
  # By default, the Estimators log output every 100 steps.
  model.train(input_fn=input_train, steps=1000)

  # Run the model in prediction mode.
  input_dict = {
      "curb-weight": np.array([2000, 3000]),
      "highway-mpg": np.array([30, 40])
  }
  predict_input_fn = tf.estimator.inputs.numpy_input_fn(
      input_dict, shuffle=False)
  predict_results = model.predict(input_fn=predict_input_fn)

  # Print the prediction results.
  print("\nPrediction results:")
  for i, prediction in enumerate(predict_results):
    msg = ("Curb weight: {: 4d}lbs, "
           "Highway: {: 0d}mpg, "
           "Prediction: ${: 9.2f}")
    msg = msg.format(input_dict["curb-weight"][i], input_dict["highway-mpg"][i],
                     PRICE_NORM_FACTOR * prediction["predictions"][0])

    print("    " + msg)
  print()


# if __name__ == "__main__":
#   tf.logging.set_verbosity(tf.logging.INFO)
#   tf.app.run(main=main)

