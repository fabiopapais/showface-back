from flask import current_app
from werkzeug.utils import secure_filename
from deepface import DeepFace
import os


# locates each image in the event folder and compares it to the uploaded image using face recognition
def findImagesOnEvent(events_paths, file):
    # Ensure the folder for images exists
    images_folder = os.path.join(current_app.config['IMAGES_FOLDER'], 'find')
    os.makedirs(images_folder, exist_ok=True)

    if not (file.filename.endswith('.png') or file.filename.endswith('.jpg')):
        raise ValueError("Uploaded file must be a .png or .jpg file")

    # Sanitize and save the image file
    filename = secure_filename(file.filename)
    image_path = os.path.join(images_folder, filename)
    file.save(image_path)

    # list for matching images
    matching_images = []

    # go through each image path
    for event_image_path in events_paths:

        # TODO: fix this workaround, the event image path should be saved without the 'app' prefix by default
        event_image_path = 'app' + event_image_path
        
        try:           
            # use deepface to compare the images
            # TODO: test different models and detector backends to find the best performance
            result = DeepFace.verify(image_path, 
                                     event_image_path, 
                                     model_name="VGG-Face", 
                                     detector_backend="opencv")
                
            if result["verified"]:
                matching_images.append(event_image_path)  
        # deepFace throws an exception if it can't find a face in the image, most common type of error
        except Exception as e:
            print(f"Error processing image {event_image_path}: {e}")

    return matching_images