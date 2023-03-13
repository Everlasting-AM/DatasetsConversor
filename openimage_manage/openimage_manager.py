import os
from filenames import CATEGORIES_FILE, IMAGES_DIR, LABELS_DIR, LABELS_FILE
from DatasetAdapter import DatasetAdapter
from oi_cat_manager import OICatManager
from oi_img_manager import OIImgManager
from oi_lbl_manager import OILblManager

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

def get_inform_files(input: str):
    return os.path.join(input, LABELS_DIR,LABELS_FILE), os.path.join(input, LABELS_DIR, CATEGORIES_FILE)

class OpenImageManager(DatasetAdapter):
    def __init__(self, input: str) -> None:
        check_arguments(input)
        self.basename = input
        self.lbls, self.cats = get_inform_files(input)
        self.cat_manager = OICatManager(self.cats)

    def filter_elements_category(self, cats: list[str]):
        codes = [self.cat_manager.get_codename_cat(cat) for cat in cats]
    
    def generate_anns_yolo(self, dir_out: str):
        pass
    
    def generate_cats_file(self, fileout: str):
        pass
    
    def show_cats_names(self) -> list[str]:
        pass
    
    def generate_images_filtered(self, output: str):
        pass
