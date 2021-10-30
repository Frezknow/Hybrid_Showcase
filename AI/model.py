import wget
import zipfile

def unzip_data(filename):
  """
  Unzips filename into the current working directory.

  Args:
    filename (str): a filepath to a target zip folder to be unzipped.
  """
  zip_ref = zipfile.ZipFile(filename, "r")
  zip_ref.extractall()
  zip_ref.close()
# Get 10% of training data of 10 classes of Food101
def load_and_prep_image(filename, img_shape=224, scale=True):
  """
  Reads in an image from filename, turns it into a tensor and reshapes into
  (224, 224, 3).

  Parameters
  ----------
  filename (str): string filename of target image
  img_shape (int): size to resize target image to, default 224
  scale (bool): whether to scale pixel values to range(0, 1), default True
  """
  # Read in the image
  img = tf.io.read_file(filename)
  # Decode it into a tensor
  img = tf.image.decode_jpeg(img)
  # Resize the image
  img = tf.image.resize(img, [img_shape, img_shape])
  if scale:
    # Rescale the image (get all values between 0 and 1)
    return img/255.
  else:
    return img

wget.download("https://storage.googleapis.com/ztm_tf_course/food_vision/10_food_classes_10_percent.zip","10_food_classes_10_percent.zip")
unzip_data("10_food_classes_10_percent.zip")
dir = "10_food_classes_10_percent"

train_dir = dir+"/train"
test_dir = dir+"/test"
import tensorflow as tf

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
train_data_10_percent = tf.keras.preprocessing.image_dataset_from_directory(directory=train_dir, 
                                                                            image_size=IMG_SIZE,
                                                                            label_mode="categorical",
                                                                            batch_size=BATCH_SIZE)
test_data = tf.keras.preprocessing.image_dataset_from_directory(directory=test_dir,
                                                                image_size=IMG_SIZE,
                                                                label_mode="categorical",
                                                                batch_size=BATCH_SIZE)
train_data_10_percent.class_names

# Create the Base model
base_model = tf.keras.applications.efficientnet.EfficientNetB0(include_top=False)
# Make the Base model non-trainable, this basically doesn't allow for anything before (base line) to be touched in terms of the Models previously trained layers/weights
base_model.trainable = False
# Create inputs into our model
inputs = tf.keras.layers.Input(shape=(224,224,3), name="input_layer")
# Pass the inputs to the base model 
x = base_model(inputs)
print(f"Shape after passing inputs through the base model: {x.shape}")
# Average pool the outputs of the base model (aggregate all the most important information)
x = tf.keras.layers.GlobalAveragePooling2D(name="global_average_pooling_layer")(x)
print(f"Shape after GlobalAveragePooling2D: {x.shape}")
# Create the output activation layer
outputs = tf.keras.layers.Dense(10, activation="softmax", name="output_layer")(x)
transfer_model = tf.keras.Model(inputs,outputs)
# Compile the model
transfer_model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(),metrics=["accuracy"])
# Create a callback that saves the models weights
checkpoint_path = "training_1/cp.ckpt"
import os
checkpoint_dir = os.path.dirname(checkpoint_path)
saveWeights = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
history = transfer_model.fit(train_data_10_percent,
                             epochs=5,
                             steps_per_epoch=len(train_data_10_percent),
                             validation_data=test_data,
                             validation_steps=int(0.25 * len(test_data)),
                             callbacks=[saveWeights]
                             )


builder = transfer_model.save(filepath="transferModel1",save_format="tf")
