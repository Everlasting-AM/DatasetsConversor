import DatasetAdapter
from . import CocoImgManager, CocoAnntManager, CocoCatManager
from pycocotools.coco import COCO
import os

ANNOTATIONS_FOLDER = "annotations"
    
class CocoManager(DatasetAdapter.DatasetAdapter):
    """
        Principal gestor del dataset, encargado de comprobar que sea correcto y 
        de dirigir el funcionamiento de los diferentes manager.
    """
    def __init__(self, dataset: str) -> None:
        self.basedir = self.check_arguments(dataset)
        data = CocoManager.find_dataset(self.basedir)
        if data:
            self.coco = COCO(data)
            self.anntManager: CocoAnntManager.CocoAnntManager = CocoAnntManager.CocoAnntManager(self.coco)
            self.catManager: CocoCatManager.CocoCatManager = CocoCatManager.CocoCatManager(self.coco)
            self.imgManager: CocoImgManager.CocoImgManager = CocoImgManager.CocoImgManager(self.coco)
        else:
            exit("Dataset incorrecto")
    
    def find_dataset(dir_input: str) -> str|None:
        """Busca dentro del directorio del dataset donde se encuentra el archivo
            de entrenamiento o validación, y retorna la ruta del archivo .json
            que representa el dataset en caso de localizarlo.
        Args:
            dir_input (str): directorio base del dataset
        Returns:
            str|None: ruta del directorio.json o None si no se ha encontrado
        """
        items = os.listdir(dir_input)
        if "annotations" in items:
            anotaciones = os.path.join(dir_input, ANNOTATIONS_FOLDER)
            for elem in os.listdir(anotaciones):
                print(elem)
                if elem.endswith(".json"):
                    return os.path.join(anotaciones, elem)
        raise ValueError("ERROR: no se ha encontrado ningún archivo .json en la carpeta ")


    def check_arguments(self, input: str):
        """
            Comprueba si el nombre del dataset de entrada es válido
        Args:
            input (str): ruta del dataset de entrada
        Returns:
            str: directorio base del dataset
        """
        base_dir = input 
        if not os.path.exists(input) :
            raise ValueError("ERROR: El archivo introducido no existe o es un directorio")
        # Nos han introducido un archivo, debe ser .json
        elif os.path.isfile(input):
            if not input.endswith(".json"):
                raise ValueError("ERROR: El archivo de entrada no es un .json")
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(input)))
        # Nos han metido una carpeta, puede ser la base del dataset o la de 
        # anotaciones
        else:
            if input == ANNOTATIONS_FOLDER:
                base_dir = os.path.dirname(os.path.abspath(input))
            elif not filter(lambda e: e.startswith("images"), os.listdir(input)):
                raise ValueError("""ERROR: No se ha encontrado ninguna carpeta 
                                 images en el directorio indicado""")
            elif not ANNOTATIONS_FOLDER in os.listdir(input):
                raise FileNotFoundError("""ERROR: No se ha encontrado la carpeta
                                        annotations en el directorio introducido""")
        return base_dir
            
        

    def filter_elements_category(self, cats: list[str]):
        """
            Realiza el filtrado de los elementos del dataset COCO, de forma que 
            se actualiza el dataset para que solo contenga la información 
            necesaria sobre los elementos que se van a estudiar.
        Args:
            cats (list[str]): categorías que se quieren analizar
        """
        ids = self.catManager.get_cat_ids(cats)
        self.anntManager.filter_annts_cats(ids)
        self.imgManager.filter_images_cat(ids)
        self.catManager.filter_cats(ids)
        renamed_cats, original_cats = self.catManager.rename_cats()
        self.anntManager.update_cat_ids(original_cats, renamed_cats)

    def generate_anns_yolo(self, dir_out: str):
        """
            Genera un directorio donde se almacenan todas las anotaciones en formato
            YOLO (un archivo por imagen donde aparece la información de todas 
            las anotaciones sobre esa imagen)
        Args:
            dir_out (str): Directorio donde se crearán las anotaciones en formato YOLO.
        """
        labels = os.path.join(dir_out, "labels")
        self.anntManager.convert_to_YOLO(labels)
    
    def generate_cats_file(self, fileout: str):
        """
            Genera un archivo donde aparecen todas las categorías del dataset
            ordenadas por su ID
        Args:
            fileout (str): directorio de salida
        """
        self.catManager.generate_classes_file(os.path.join(fileout,"classes.names"))
    
    def generate_images_filtered(self, outdir: str):
        """
            Copia las imágenes filtradas en la carpeta destino
        Args:
            outdir (str): carpeta donde se guardan las imágenes filtradas
        """
        filtered = filter(lambda x: x.startswith("images"), os.listdir(self.basedir))
        elem = next(filtered, None)
        self.imgManager.copy_files_to_special_folder(os.path.join(outdir, "images"), os.path.join(self.basedir, elem))
        
    def show_cats_names(self) -> list[str]:
        """
            Obtiene la lista de nombres de categorías de objetos que hay 
            definidas en el dataset.    
        Returns:
            list[str]: lista de nombres de categorías
        """
        return self.catManager.get_cat_names()