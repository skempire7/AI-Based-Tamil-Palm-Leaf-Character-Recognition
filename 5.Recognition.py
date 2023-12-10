import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import pickle

# Define hyperparameters
image_size = (150, 150)
num_classes = 64  # Replace with the actual number of classes in your dataset

# Load the saved model
model = tf.keras.models.load_model('6.Model.h5')

# Load the class indices to class names mapping from class_labels.pkl
with open('7.class.pkl', 'rb') as file:
    class_indices = pickle.load(file)

# Define the folder containing your test images
folder_path = 'Segmented_Letters'  # Replace with the path to your test image folder

output_file_path = '14.predictions.txt'
with open(output_file_path, 'w', encoding='utf-8'):
    pass

print("file cleared")
with open(output_file_path,'w', encoding='utf-8') as output_file:
# Loop through all image files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):  # Assuming your images are in PNG format
        # Construct the full path to the image file
            image_path = os.path.join(folder_path, filename)

        # Load and preprocess a single test image
            img = load_img(image_path, target_size=image_size)
            img_array = img_to_array(img)
            img_array = img_array / 255.0  # Rescale pixel values to [0, 1]
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Make a prediction on the single test image
            prediction = model.predict(img_array)

        # Convert one-hot encoded label to class label
            predicted_class_index = np.argmax(prediction, axis=1)

        # Get the class name corresponding to the predicted class index
            predicted_class_name = list(class_indices.keys())[list(class_indices.values()).index(predicted_class_index[0])]
            output_file.write(f"{predicted_class_name} ")
            #print(f"Predicted Class Name for {filename}: {predicted_class_name}")

print(f"Predictions saved to {output_file_path}")



