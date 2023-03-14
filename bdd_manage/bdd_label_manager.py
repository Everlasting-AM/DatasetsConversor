import os
import cv2

NAME_LABELS_DIR = "labels"
NAME_IMAGE_DIR = "images"

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
    
class BddLabelManager:
    def __init__(self, labels: list[str], basedir: str) -> None:
        """
            Crea un manager para gestionar las etiquetas
        Args:
            labels (list[str]): lista de etiquetas
            basedir (str): directorio base del dataset
        """
        self.data = labels
        self.basedir = basedir
    
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
            for lbl in record['labels']:
                if lbl['category'] in cats:
                    lbls.append(lbl)
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
            if not record['labels']:
                continue
            filename = os.path.splitext(record['name'])[0]
            fileroute = os.path.join(self.basedir, NAME_IMAGE_DIR, record['name'])
            with open(os.path.join(outdir, NAME_LABELS_DIR,filename+".txt"), "w") as f:
                for lbl in record['labels']:
                    x1, x2 = lbl['box2d']['x1'], lbl['box2d']['x2']
                    y1, y2 = lbl['box2d']['y1'], lbl['box2d']['y2']
                    bbox = get_normalized_bbox((x1, y1, x2, y2), fileroute)
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
        print("IMAGEN: ",image)
        imagen = cv2.imread(image)
        ancho, alto, _ = imagen.shape
        # Devolvemos el bbox normalizado
        return (bbox[0]/ancho, bbox[1]/alto, bbox[2]/ancho, bbox[3]/alto)
        
        
    
            
                
        