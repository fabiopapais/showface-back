from flask import current_app
from werkzeug.utils import secure_filename
from deepface import DeepFace
import pandas as pd
import os


# locates each image in the event folder and compares it to the uploaded image using face recognition
def findImagesOnEvent(eventId, file):
    # Ensure the folder for images exists
    images_folder = os.path.join(current_app.config['IMAGES_FOLDER'], 'find')
    os.makedirs(images_folder, exist_ok=True)

    if not (file.filename.endswith('.png') or file.filename.endswith('.jpg') or file.filename.endswith('.jpeg')):
        raise ValueError("Uploaded file must be a .png or .jpg file")

    # Sanitize and save the image file
    filename = secure_filename(file.filename)
    image_path = os.path.join(images_folder, filename)
    file.save(image_path)

    # event images path (images folder + eventid)
    event_image_path = os.path.join(current_app.config['IMAGES_FOLDER'], str(eventId))

    image_paths = []
        
    try:           
        # use deepface to compare the images
        # TODO: test different models and detector backends to find the best performance
        result = DeepFace.find(image_path, 
                               event_image_path, 
                               model_name="VGG-Face", 
                               detector_backend="opencv")
                
        # convert the result pandas dataframe to a dictionary
        # append matching image links
        dataframe = result[0]
        dataframe_dict = dataframe.to_dict(orient='records')
        for dict in dataframe_dict:
            image_paths.append(dict['identity'].split('app')[1])
        
    # deepFace throws an exception if it can't find a face in the image, most common type of error
    except Exception as e:
        print(f"Error processing image {event_image_path}: {e}")

    print(image_paths)
    return image_paths

def preGenerateRepresentations(eventId, imagesPaths):
    print("Generating representations for event ", eventId)

    event_image_path = os.path.join(current_app.config['IMAGES_FOLDER'], str(eventId))
    image_path = "app/" + imagesPaths[0] # select random image to generate representations

    print(image_path)

    DeepFace.find(image_path, 
                    event_image_path, 
                    model_name="VGG-Face", #TODO: configure same model in env file
                    detector_backend="opencv")