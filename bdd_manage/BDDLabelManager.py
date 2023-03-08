import os
import cv2

NAME_LABELS_DIR = "labels"

def get_normalized_bbox(bbox: tuple[int, int, int, int], image: str):
    """
        Genera el bbox normalizado a las dimensiones de la imagen
    Args:
        bbox (tuple[int, int, int, int]): bbox original
        image (str): ruta de la imagen
    """
    # Obtenemos las dimensiones de la imagen
    imagen = cv2.imread(image)
    ancho, alto, _ = imagen.shape
        
    # Devolvemos el bbox normalizado
    return (bbox[0]/ancho, bbox[1]/alto, bbox[2]/ancho, bbox[3]/alto)
    
class BDDLabelManager:
    def __init__(self, labels: list[str], basedir: str) -> None:
        """
            Crea un manager para gestionar las etiquetas
        Args:
            labels (list[str]): lista de etiquetas
            basedir (str): directorio base del dataset
        """
        self.data = labels
        self.basedir = os.join(basedir, NAME_LABELS_DIR)
    
    def filter_labels(self, cats: list[str]):
        """
            FIltramos las etiquetas del dataset para quedarnos únicamente 
            con las etiquetas referentes a elementos de las categorías indicadas
        Args:
            cats (list[str]): categorías de las que queremos estudiar los objetos
        """
        # Para cada registro, extraemos las etiquetas que nos interesan y las 
        # guardamos en la lista
        for record in self.data:
            lbls = []
            lbls.append(lbl for lbl in lbls if lbl['category'] in cats)
            record['labels'] = lbls
    
    def generate_labels_files(self, outdir: str, cats: list[str]):
        """
            Genera en el directorio que se indique un archivo por cada imagen 
            donde se indican las etiquetas de cada imagen
        Args:
            outdir (str): directorio de salida
        """
        # Obtenemos los ids de las categorías 
        ids = list(range(0, len(cats)))
        # Para cada registro, creamos un archivo .txt y guardamos la info
        for record in self.data:
            filename = os.path.join(self.basedir, 
                                    os.path.splitext(record['name'])[0])
            with open(os.path.join(outdir, filename+".txt"), "w") as f:
                for lbl in record['labels']:
                    bbox = get_normalized_bbox(lbl['box2d'])
                    f.write("{} {} {} {} {}".format(
                         ids[cats.index(lbl['category'])], bbox[0], bbox[1], 
                         bbox[2], bbox[3]
                    ))
    
    def get_normalized_bbox(bbox: tuple[int, int, int, int], image: str):
        """
            Genera el bbox normalizado a las dimensiones de la imagen
        Args:
            bbox (tuple[int, int, int, int]): bbox original
            image (str): ruta de la imagen
        """
        # Obtenemos las dimensiones de la imagen
        imagen = cv2.imread(image)
        ancho, alto, _ = imagen.shape
        
        # Devolvemos el bbox normalizado
        return (bbox[0]/ancho, bbox[1]/alto, bbox[2]/ancho, bbox[3]/alto)
        
        
    
            
                
        