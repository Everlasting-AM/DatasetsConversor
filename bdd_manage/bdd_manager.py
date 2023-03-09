import ijson
import DatasetAdapter
import bdd_manage.bdd_cat_manager as bdd_cat_manager
import bdd_manage.bdd_img_manager as bdd_img_manager
import bdd_manage.bdd_label_manager as bdd_lbl_manager
import os
LBLS_FOLDER_INPUT = "labels"

def extract_label_file(basedir: str):
    if os.path.isdir(basedir):
        labels_dir = os.listdir(os.path.join(basedir, LBLS_FOLDER_INPUT))
        for f in labels_dir:
            if f.endswith(".json") and "labels" in f:
                return os.path.join(basedir, LBLS_FOLDER_INPUT, f)

class BddManager(DatasetAdapter.DatasetAdapter):
    def __init__(self, input: str) -> None:
        """
            Crea un manager general encargado de gestionar el dataset BDD100k
        Args:
            input (str): archivo base del dataset
            val (int): indica si el archivo es de evaluación o de entrenamiento
        """
        # Extraemos del archivo las etiquetas
        self.input = BddManager.check_args(input)
        file = extract_label_file(self.input)
        
        # Convertimos de json a lista de labels 
        self.labels = []
        with open(file) as f:
            for record in ijson.items(f, "item"):
                self.labels.append(record)
        # Creamos los managers auxiliares
        self.catManager = bdd_cat_manager.BddCatManager(self.labels)
        self.img_manager = bdd_img_manager.BddImgManager(self.labels, self.input)
        self.lbl_manager = bdd_lbl_manager.BddLabelManager(self.labels, self.input)
    
    def check_args(input: str):
        """
            Comprueba que se haya introducido un archivo .json que describe un dataset,
            o la carpeta que contiene una carpeta labels y otra images.
        Args:
            input (str): ruta del dataset
            val (int): Determina si el conjunto es para evaluar o para entrenar
        """
        # Comprobamos si el input es un fichero que sea el json
        if not input.endswith("json") and not os.path.isdir(input):
            raise ValueError("El archivo introducido no es un .json ni un directorio")
        if os.path.isdir(input):
            # Comprobamos que input es carpeta, esté la carpeta images
            if "images" not in os.listdir(input):
                raise ValueError("La carpeta introducida no tiene ningún directorio images")
            # Comprobamos que esté la carpeta labels
            if LBLS_FOLDER_INPUT not in os.listdir(input):
                raise ValueError("La carpeta indicada no tiene ningún directorio labels")
            filenames = os.listdir(os.path.join(input, "labels"))
            
            if not any("labels" in f for f in filenames):
                raise ValueError("No se ha encontrado ningún archivo que contenga labels en su nombre")
            return input
        else:
            return os.path.dirname(os.path.dirname(input))   

    def filter_elements_category(self, cats: list[str]):
        print("Categorias:",cats)
        # Filtramos imágenes y etiquetas
        self.lbl_manager.filter_labels(cats)
        self.img_manager.filter_images(cats)
        
    def generate_anns_yolo(self, dir_out: str):
        self.lbl_manager.generate_labels_files(dir_out, self.catManager.categories)
    
    def generate_cats_file(self, fileout: str):
        salida = os.path.join(fileout, 'classes.name')
        self.catManager.generate_cats_file(salida)
        
    def show_cats_names(self):
        return self.catManager.extract_categories_sequential()
    
    def generate_images_filtered(self, output: str):
        self.img_manager.copy_images(self.input, output)
