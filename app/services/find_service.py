from flask import current_app
from werkzeug.utils import secure_filename
import zipfile
import os

from app.models import Event, User
from app import db


def findImagesOnEvent(events_paths, file):
    # Ensure the folder for images exists
    images_folder = os.path.join(current_app.config['IMAGES_FOLDER'], '/find')
    os.makedirs(images_folder, exist_ok=True)

    if not (file.filename.endswith('.png') or file.filename.endswith('.jpg')):
        raise ValueError("Uploaded file must be a .png or .jpg file")

    # Sanitize and save the image file
    filename = secure_filename(file.filename)
    image_path = os.path.join(images_folder, filename)
    file.save(image_path)

    # TODO:
    # The file path is at image_path
    # use the file path to find the images in the events_paths