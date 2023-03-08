from pycocotools.coco import COCO 
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

class CocoImgManager:
    """
        Clase utilizada para la gestión de las imágenes con el dataset COCO.
    """
    def __init__(self, coco: COCO) -> None:
        self.coco = coco
        
    def write_images_on_file(self, out: str):
        """
            Extrae los nombres de todas las imágenes contenidas en el dataset e 
            imprime cada nombre en el archivo de salida con la ruta introducida
        Args:
            coco (pycocotools.coco.COCO): dataset COCO
            out (str): ruta del archivo de salida
        """
        with open(out, "w") as file:
            lista = [image["file_name"] for image in self.coco.dataset["images"]]
            for img in lista:
                file.write(img+"\n")

    
    def filter_images_cat(self, cat_ids: list[int]) -> list:
        """
            Filtra las imágenes que contienen un objeto de una de las categorías 
            que se indican
        Args:
            coco (COCO): dataset de entrada
            cat_ids (list[int]): ids de las categorías buscadass 

        Returns:
            list: Imágenes que contienen algún objeto de las categorías buscadas
        """
        files = set()
        for id in self.coco.anns:
            if self.coco.anns[id]['category_id'] in cat_ids:
                files.add(self.coco.anns[id]['image_id'])
        
        # Eliminamos las fotos innecesarias
        for key in self.coco.imgs.copy():
            if key not in files:
                del self.coco.imgs[key]
        return self.coco.imgs
    
    def get_filename_images(self, image_ids: list[int]) -> list[str]:
        """
            Obtiene los nombres de las imágenes contenidas en el dataset de entrada,
            y que tengan el id contenido en la lista de ids introducida.
        Args:
            coco (COCO): dataset de entrada
            image_ids (list[int]): lista de ids de las imágenes buscadas

        Returns:
            list[str]: lista con los nombres de las imágenes
        """
        images = self.coco.loadImgs(ids=image_ids)
        return [img['file_name'] for img in images]

    def copy_files_id_other_folder(self, image_ids: list[int], new_dir: str, 
                                last_dir: str) -> None:
        """
            Copia los archivos cuyo id está en la lista introducida a una carpeta 
            diferente.
        Args:
            coco (COCO): dataset de entrada
            image_ids (list[int]): ids de las imágenes buscadas
            new_dir (str): carpeta destino
            last_dir (str): carpeta origen
        """
        paths = self.get_filename_images(image_ids)
        copy_files_to_special_folder(paths, new_dir, last_dir)
    
    def get_boxes_elements(self, image_id: int, catlistAny=[]) -> list:
        """
            Obtiene los objestos boxes de cada objeto identificado en la
            imagen, de forma que se puede acceder a su posición
        Args:
            image_id (int): id de la imagen
            coco (COCO): dataset de entrada 
            catlistAny (list, optional): lista de categorías de los objetos de los 
            que queremos obtener el box. Defaults to [].

        Returns:
            list: lista de boxes de las anotaciones de la imagen y objetos buscados
        """
        # Obtenemos todas las anotaciones para la imagen concreta y la categoría 
        annot_ids = []
        for cat in catlistAny:
            annot_ids_cat = self.coco.getAnnIds(imgIds= image_id, catIds= cat)
            annot_ids += annot_ids_cat
        
        anns = self.coco.loadAnns(ids=annot_ids)    
        return [ann['bbox'] for ann in anns]
    
    def copy_files_to_special_folder(self, new_folder: str, 
                                 last_folder: str) -> None:
        """
            Copia los archivos en los paths introducidos en un directorio
            de archivos relevantes creados cuando se llama a la función
        Args:
            new_folder (str): ruta carpeta destino
            last_folder (str): ruta carpeta origen
        """
        images = [self.coco.imgs[id]['file_name']for id in self.coco.imgs]
        # Crea el directorio
        try:
            folder = new_folder
            os.mkdir(new_folder)
        except FileExistsError:
            reps = 1
            while True:
                try:
                    os.mkdir(new_folder +'(' + str(reps) + ')')
                    folder = new_folder +'(' + str(reps) + ')'
                    break
                except FileExistsError:
                    reps+=1

        for image in images:
            new_path = os.path.join(folder, image)
            shutil.copy(os.path.join(last_folder, image), new_path)
            
def copy_files_to_special_folder(images: list[str], new_folder: str, 
                                 last_folder: str) -> None:
    """
        Copia los archivos en los paths introducidos en un directorio
        de archivos relevantes creados cuando se llama a la función
    Args:
        images (list[str]): lista de imágenes que se va a copiar
        new_folder (str): ruta carpeta destino
        last_folder (str): ruta carpeta origen
    """
    for image in images:
        new_path = os.path.join(new_folder, image)
        shutil.copy(os.path.join(last_folder,image), new_path)

def print_boxes(image: Image, boxes: list) -> None:
    """
        Imprime los boxes la lista de boxes de la imagen concreta, mostrando la 
        imagen y los boxes asociados. 
    Args:
        image (Image): Imagen analizada
        boxes (list): Lista de elementos de la imagen
    """
    # Añadimos los boxes
    fig, ax = plt.subplots()
    for box in boxes:
        bb = patches.Rectangle((box[0], box[1]), box[2], box[3], linewidth=2, 
                               edgecolor="blue", facecolor="none")
        ax.add_patch(bb)
    
    # Imprimimos la imagen
    ax.imshow(image)
    plt.show()