import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from deepface import DeepFace
from deepface.modules import verification
from deepface.models.FacialRecognition import FacialRecognition
from deepface.commons.logger import Logger


logger = Logger()

# ----------------------------------------------
# build face recognition model

model_name = "VGG-Face"

model: FacialRecognition = DeepFace.build_model(task="facial_recognition", model_name=model_name)

target_size = model.input_shape

def load_faces_from_folder(folder_path):
    face_embeddings = {}
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder_path, file_name)
            try:
                # Extract face
                img = DeepFace.extract_faces(img_path=img_path)[0]["face"]
                img = cv2.resize(img, target_size)
                img = np.expand_dims(img, axis=0)  # Reshape to (1, target_size)
                
                # Get embedding
                embedding = model.forward(img)
                face_embeddings[file_name] = np.array(embedding)
                
                logger.info(f"Processed: {file_name}")
            except Exception as e:
                logger.error(f"Error processing {file_name}: {e}")
    return face_embeddings

def compare_face_with_embeddings(embeddings_list, photo_path):
    """
    Compare a given photo with a list of precomputed face embeddings.

    Args:
        embeddings_list (dict): Dictionary containing file names as keys and their embeddings as values.
        photo_path (str): Path to the photo to compare.
        model: The preloaded facial recognition model.
        model_name (str): The name of the model used to determine the threshold.

    Returns:
        dict: A dictionary with distances and match results.
    """
    # Load and preprocess the input photo
    try:
        img = DeepFace.extract_faces(img_path=photo_path)[0]["face"]
        img = cv2.resize(img, model.input_shape)
        img = np.expand_dims(img, axis=0)  # Reshape to (1, target_size)
        
        # Get embedding of the input photo
        photo_embedding = np.array(model.forward(img))

        # Find threshold
        threshold = verification.find_threshold(model_name=model_name, distance_metric="euclidean")

        # Initialize the result dictionary
        results = {}

        for file_name, embedding in embeddings_list.items():
            # Calculate Euclidean distance
            distance_vector = np.square(photo_embedding - embedding)
            distance = np.sqrt(distance_vector.sum())

            match = distance < threshold
            results[file_name] = {
                "distance": distance,
                "match": match
            }

        return results

    except Exception as e:
        print(f"Error processing the photo: {e}")
        return None