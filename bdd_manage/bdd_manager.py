import ijson
import DatasetAdapter
import bdd_manage.bdd_cat_manager as bdd_cat_manager
import bdd_manage.bdd_img_manager as bdd_img_manager
import bdd_manage.bdd_label_manager as bdd_lbl_manager
import os

class BddManager(DatasetAdapter.DatasetAdapter):
    def __init__(self, input: str, val:int) -> None:
        """
            Crea un manager general encargado de gestionar el dataset BDD100k
        Args:
            input (str): archivo base del dataset
            val (int): indica si el archivo es de evaluación o de entrenamiento
        """
        # Extraemos del archivo las etiquetas
        self.input = BddManager.check_args(input, val)
        
        # Convertimos de json a lista de labels 
        self.labels = []
        with open(input) as f:
            for record in ijson.items(f, "item"):
                self.labels.append(record)
            
        # Creamos los managers auxiliares
        self.catManager = bdd_cat_manager.BddCatManager(self.labels)
        self.img_manager = bdd_img_manager.BddImgManager(self.labels)
        self.lbl_manager = bdd_lbl_manager.BDDLabelManager(self.labels, self.input)
    
    def check_args(input: str, val:int):
        """
            Comprueba que se haya introducido un archivo .json que describe un dataset,
            o la carpeta que contiene una carpeta labels y otra images.
        Args:
            input (str): ruta del dataset
            val (int): Determina si el conjunto es para evaluar o para entrenar
        """
        if not input.endswith("json") and not os.path.isdir(input):
            raise ValueError("El archivo introducido no es un .json ni un directorio")
        if os.path.isdir(input):
            if "images" not in os.listdir(input):
                raise ValueError("La carpeta introducida no tiene ningún directorio images")
            if "labels" not in os.listdir(input):
                raise ValueError("La carpeta indicada no tiene ningún directorio labels")
            filenames = os.listdir(os.path.join(input, "labels"))
            if not any("labels" and ("val" if val else "train")for name in filenames):
                raise ValueError("No se ha encontrado ningun fichero labels_{}".format(
                    "val" if val else "train"
                ))
            return input
        else:
            return os.path.dirname(os.path.dirname(input))   

    def filter_elements_category(self, cats: list[str]):
        # Filtramos imágenes y etiquetas
        self.lbl_manager.filter_labels(cats)
        self.img_manager.filter_images(cats)
        
    def generate_anns_yolo(self, dir_out: str):
        self.lbl_manager.generate_labels_files(dir_out, self.catManager.categories)
    
    def generate_cats_file(self, fileout: str):
        self.catManager.generate_cats_file(fileout)
        
    def show_cats_names(self):
        return self.catManager.extract_categories_sequential()