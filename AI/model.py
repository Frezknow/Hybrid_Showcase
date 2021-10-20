!wget https://raw.githubusercontent.com/mrdbourke/tensorflow-deep-learning/main/extras/helper_functions.py
# Import helper functions we're going to use in this notebook
from helper_functions import create_tensorboard_callback, plot_loss_curves, unzip_data, walk_through_dir
# Get 10% of training data of 10 classes of Food101
!wget https://storage.googleapis.com/ztm_tf_course/food_vision/10_food_classes_10_percent.zip
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
