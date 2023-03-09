import os
from filenames import CATEGORIES_FILE, IMAGES_DIR, LABELS_DIR, LABELS_FILE
from DatasetAdapter import DatasetAdapter

def check_arguments(input:str):
    """
    Comprueba que en el dataset introducido hay una carpeta llamada images,
    donde se deben de encontrar las imágenes y una carpeta labels, donde 
    se encuentre un archivo labels.csv y otro archivo categories.csv.

    :param input (str): ruta del directorio base del dataset
    """
    if os.path.isdir(input):
        content = os.listdir(input)
        if not IMAGES_DIR in content:
            raise FileNotFoundError("No se ha encontrado la carpeta images")
        elif not LABELS_DIR in content:
            raise FileNotFoundError("No se ha encontrado la carpeta labels")
        elif LABELS_FILE in os.listdir(os.path.join(input, LABELS_DIR)):
            raise FileNotFoundError("""No se ha encontrado el archivo labels.csv
                                    dentro de {}""".format(os.path.join(input, LABELS_DIR)))
        elif CATEGORIES_FILE in os.listdir(os.path.join(input, LABELS_DIR)):
            raise FileNotFoundError("""No se ha encontrado el archivo de etiquetas
                                    dentro de {}""".format(os.path.join(input, LABELS_DIR)))
    else: 
        raise ValueError("La entrada debe ser la ruta del directorio del dataset")

class OpenImageManager(DatasetAdapter):
    def __init__(self, input: str) -> None:
        check_arguments(input)
        self.basename = input
    