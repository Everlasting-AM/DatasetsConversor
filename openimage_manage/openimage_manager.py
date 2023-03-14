import os
from filenames import (CATEGORIES_INPUT_FILE, IMAGES_INPUT_DIR, 
                       LABELS_INPUT_DIR, LABELS_INPUT_FILE, 
                       CATS_FILENAME, IMAGES_OUT_DIR)
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
        if not IMAGES_INPUT_DIR in content:
            raise FileNotFoundError("No se ha encontrado la carpeta images")
        elif not LABELS_INPUT_DIR in content:
            raise FileNotFoundError("No se ha encontrado la carpeta labels")
        elif LABELS_INPUT_FILE in os.listdir(os.path.join(input, LABELS_INPUT_DIR)):
            raise FileNotFoundError("""No se ha encontrado el archivo labels.csv
                                    dentro de {}""".format(os.path.join(input, LABELS_INPUT_DIR)))
        elif CATEGORIES_INPUT_FILE in os.listdir(os.path.join(input, LABELS_INPUT_DIR)):
            raise FileNotFoundError("""No se ha encontrado el archivo de etiquetas
                                    dentro de {}""".format(os.path.join(input, LABELS_INPUT_DIR)))
    else: 
        raise ValueError("La entrada debe ser la ruta del directorio del dataset")

def get_inform_files(input: str):
    """
        Devuelve la ruta de los archivos de etiquetas "labels.csv" y de categorías, "categories.csv"
    """
    return os.path.join(input, LABELS_INPUT_DIR,LABELS_INPUT_FILE), os.path.join(input, LABELS_INPUT_DIR, CATEGORIES_INPUT_FILE)

class OpenImageManager(DatasetAdapter):
    def __init__(self, input: str) -> None:
        check_arguments(input)
        self.basename = input
        self.lbls, self.cats = get_inform_files(input)
        self.cat_manager = OICatManager(self.cats)
        self.img_manager = OIImgManager(os.path.join(self.basename, IMAGES_INPUT_DIR))
        self.lbl_manager = OILblManager(self.lbls)


    def filter_elements_category(self, cats: list[str]):
        """
            Filtra los elementos del dataset para quedar solo con los 
            relacionados con la detección de objetos de una categoría 
            de la lista introducida.
        """
        self.cat_manager.filter_categories(cats)
        self.codes = [self.cat_manager.get_codename_cat(cat) for cat in cats]
        
        # Filtramos las etiquetas e imágenes
        self.lbl_manager.filter_labels(self.codes)
        self.img_manager.insert_imgs(self.lbl_manager.df)
        

    def generate_anns_yolo(self, dir_out: str):
        """
            Generamos el archivo de anotaciones en el formato YOLO
        """
        self.lbl_manager.generate_lbls_files(dir_out, self.codes)
    
    def generate_cats_file(self, basedir_out: str):
        """
            Genera el archivo de categorías dentro del directorio de salida.

            :param basedir_out: directorio donde se creará el fichero
        """
        fileout = os.path.join(basedir_out, CATS_FILENAME)
        self.cat_manager.generate_catsfile(fileout)
    
    def show_cats_names(self) -> list[str]:
        """
            Devuelve la lista de categorías del dataset
        """
        return self.cat_manager.extract_categories()
    
    def generate_images_filtered(self, output: str):
        """
            Genera las imágenes que contienen objetos pertenecientes
            a las categorías introducidas por el usuario.

            :param output: directorio donde se copiarán las imágenes filtradas
        """
        input_images = os.join(self.basename, IMAGES_INPUT_DIR)
        output_dir = os.join(output, IMAGES_OUT_DIR)
        self.img_manager.copy_files(input_images, output_dir)
    

    