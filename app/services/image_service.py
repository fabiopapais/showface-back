import os
import shutil
import zipfile
from werkzeug.utils import secure_filename
from flask import current_app

from app.models import Event, Image
from app import db

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def saveEventImages(file, eventId):
    # Ensure the folder for images exists
    images_folder = os.path.join(current_app.config['IMAGES_FOLDER'], str(eventId))
    os.makedirs(images_folder, exist_ok=True)

    # Check if the file is a .zip
    if not file.filename.endswith('.zip'):
        raise ValueError("Uploaded file must be a .zip file")

    # Sanitize and save the .zip file
    zip_filename = secure_filename(file.filename)
    zip_path = os.path.join(images_folder, zip_filename)
    file.save(zip_path)

    saved_image_paths = []

    try:
        # Extract the .zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            extract_folder = os.path.join(images_folder, "extracted")
            os.makedirs(extract_folder, exist_ok=True)
            zip_ref.extractall(extract_folder)

        # Iterate and save images
        for root, _, files in os.walk(extract_folder):
            for filename in files:
                if allowedFile(filename):
                    file_path = os.path.join(root, filename)
                    
                    # secure filename
                    secure_name = secure_filename(filename)
                    target_path = os.path.join(images_folder, secure_name)
                    
                    # Save the valid image to the target path
                    with open(file_path, 'rb') as src_file, open(target_path, 'wb') as dest_file:
                        dest_file.write(src_file.read())
                    
                    # remove "app" from path
                    target_path = target_path.split('app')[1]

                    saved_image_paths.append(target_path)

        return saved_image_paths

    except zipfile.BadZipFile:
        raise ValueError("Invalid .zip file")

    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)
        if os.path.exists(extract_folder):
            shutil.rmtree(extract_folder)

def registerImagesOnDatabase(event_id, user_id, image_paths):
    for image_path in image_paths:
        image = Image(link=image_path, description='', eventId=event_id, userId=user_id)
        db.session.add(image)

    db.session.commit()

def getImages(event_id):
    images = Image.query.filter_by(eventId=event_id).all()
    image_dicts = []
    for image in images:
        image_dict = {
            'id': image.id,
            'link': image.link,
            'description': image.description,
            'eventId': image.eventId,
            'userId': image.userId
        }
        image_dicts.append(image_dict)
    return image_dicts

def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
