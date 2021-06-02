from tensorflow.keras.models import load_model
import pickle

def load_vgg_model():
    model_path = "D:/MyPrograms/Clothes2U/functions/服飾圖片分類器/Cloth Image Classifier/result/003_0320/cloth_classifier.model"
    model = load_model(model_path)
    return model