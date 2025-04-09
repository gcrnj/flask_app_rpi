from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import sys
from tensorflow.keras.models import load_model

# Model path based on OS
if sys.platform == "win32":
    keras_path = 'D:\\PythonProjects\\flask_app_rpi\\api\\corn_classification_model_v2.keras'
else:
    keras_path = ''  # Adjust path for other OS if necessary

# Load the model
model = models.load_model(keras_path)

# Image dimensions
img_height = 150
img_width = 150

# Labels for binary classification
labels = {0: "Healthy", 1: "Unhealthy"}

def get_growth_stage(image_path):
    # Load and preprocess the image
    img = load_img(image_path, target_size=(img_height, img_width))
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    
    # Predict the class (probabilities for binary classification)
    prediction = model.predict(img_array)
    
    # Use 0.5 threshold to classify: sigmoid output < 0.5 -> Healthy, >= 0.5 -> Unhealthy
    predicted_label = labels[int(prediction[0] > 0.5)]  # 0: Healthy, 1: Unhealthy
    
    return predicted_label

if __name__ == '__main__':
    print('No Plant:')
    print(get_growth_stage('D:\\PythonProjects\\flask_app_rpi\\captured_image.jpg'))
    print('\nHealthy Plant:')
    print(get_growth_stage('D:\\PythonProjects\\flask_app_rpi\\api\\healthy_test.jpg'))
    print('\nUnhealthy Plant:')
    print(get_growth_stage('D:\\PythonProjects\\flask_app_rpi\\api\\unhealthy_test.jpg'))
