from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
from keras.preprocessing import image
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
import tensorflow as tf
import json
import os
import csv

img_height, img_width = 224, 224

# Update the path to your model and ImageNet classes file
model_path = 'Models\Simple_CNN_model.h5'

# Define labelInfo
labelInfo = {
    '0': 'Downdog',
    '1': 'Goddess',
    '2': 'Plank',
    '3': 'Tree',
    '4': 'Warrior',
    # Add more labels as needed
}

model_graph = tf.Graph()
tf_session = None  # Initialize the session variable outside the context manager

with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model = load_model(model_path)

def index(request):
    context = {'a': 1}
    return render(request, 'index.html', context)

def predictImage(request):
    try:
        fileObj = request.FILES['filePath']
    except MultiValueDictKeyError:
        return HttpResponse("Error: File not found", status=400)

    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    testimage = '.' + filePathName

    # Adjust the target size to match your model's input size
    img = image.load_img(testimage, target_size=(170, 170))
    x = image.img_to_array(img)
    x = x / 255
    x = x.reshape(1, 170, 170, 3)

    with model_graph.as_default():
        with tf_session.as_default():
            predi = model.predict(x)

    import numpy as np
    predictedLabel = labelInfo[str(np.argmax(predi[0]))]

    output_image_path = generate_output_image_path(testimage)

    # Set the predicted label in the session
    request.session['predictedLabel'] = predictedLabel
    request.session.save()

    context = {'filePathName': filePathName, 'predictedLabel': predictedLabel, 'outputImagePath': output_image_path}
    return render(request, 'index.html', context)

def generate_output_image_path(input_image_path):
    # Modify this function to process the input image and return the output image path
    # For example, you can save the output image and return its path
    # Here's a simple example using the same FileSystemStorage
    output_fs = FileSystemStorage()
    output_image_path = output_fs.save('output_image.jpg', open(input_image_path, 'rb'))
    return output_fs.url(output_image_path)
    
def generate_output_image_path(input_image_path):
    # Modify this function to process the input image and return the output image path
    # For example, you can save the output image and return its path
    # Here's a simple example using the same FileSystemStorage
    output_fs = FileSystemStorage()
    output_image_path = output_fs.save('output_image.jpg', open(input_image_path, 'rb'))
    return output_fs.url(output_image_path)

def viewDataBase(request):
    listOfImages = os.listdir('./media/')
    listOfImagesPath = ['./media/' + i for i in listOfImages]
    context = {'listOfImagesPath': listOfImagesPath}
    return render(request, 'viewDB.html', context)


# views.py

# ... (your existing imports)

# views.py

# ... (your existing imports)

def view_pose_description(request):
    csv_file_path = 'C:\Pose_Detection\static\Images\CsvFiles\yoga_poses_descriptions.csv'

    # Fetch the predicted label from the session (assumes you store it in the session in your prediction view)
    predicted_label = request.session.get('predictedLabel', None)

    # Read the CSV file and get the description for the predicted label
    description = None
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if row['Yoga Pose'].lower() == predicted_label.lower():
                    description = row['Description']
                    break
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        # Add additional error handling if needed

    # Pass the description to the template
    context = {'predicted_label': predicted_label, 'description': description}
    return render(request, 'pose_description.html', context)


