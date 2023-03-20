from pycocotools.coco import COCO
import tkinter as tk
import os
import json

class CocoAnntManager:
    """
        Clase que se encarga de gestionar la información sobre el dataset 
        asociado
    """
    
    def __init__(self, coco: COCO) -> None:
        """
            Construye un objeto COCOAnntManager
        Args:
            coco (COCO): dataset que se va a gestionars
        """
        self.coco = coco
    
    def get_anns_contains_categories(self, cat_ids: list[int]):
        """
            Obtiene las anotaciones sobre las categorías concretas indicadas
        Args:
            cat_ids (list[int]): ids de las categorías de las que se quiere extraer 
            las anotaciones relacionadas
        Returns:
            list: Lista con las anotaciones encontradas
        """
        ann_ids = set()
        for id in cat_ids:
            ann_ids = ann_ids.union(self.coco.getAnnIds(catIds=id))
        return self.coco.loadAnns(ids = list(ann_ids))
    
    def filter_annts_cats(self, catIds: list[int]):
        # Eliminamos las anotaciones no relacionadas con esas categorías.
        for id in list(self.coco.anns):
            if self.coco.anns[id]["category_id"] not in catIds:
                del self.coco.anns[id]
        # Guardamos las anns y las devolvemos
        return self.coco.anns

    
    def convert_to_YOLO(self, dir: str):
        """
            Extrae del dataset COCO la información sobre cada anotación, y guarda en 
            para cada imagen un archivo .txt donde se encuentran las anotaciones en
            formato YOLO (id categoría, x1, y1, x2, y2), donde las coordenadas del 
            bbox se encuentran normalizadas
        Args:
            coco (COCO): Dataset COCO
            dir (str): Directorio donde se almacenarán los archivos .txt
        """
        print("Imagenes: ",len(self.coco.imgs))
        iter = 0
        for idimage in self.coco.imgs:
            image = self.coco.imgs[idimage]
            iter +=1
            # Extraemos el nombre del archivo
            filename = image["file_name"]
            name, ext = os.path.splitext(filename)
            out = name + ".txt"
            
            # Extraemos el ancho y el alto para normalizar
            alto = image['height']
            ancho = image["width"]
            
            # Escribimos en el fichero todas las notaciones
            with open(os.path.join(dir, out), 'w') as file:
                anns = [self.coco.anns[id] for id in self.coco.anns if 
                        self.coco.anns[id]["image_id"] == idimage]
                for ann in anns:
                    bbox = ann["bbox"]                
                    file.write("{} {} {} {} {}\n".format(ann["category_id"], 
                    (bbox[0]+bbox[2]/2)/ancho, (bbox[1]+bbox[3]/2)/alto, bbox[2]/ancho, bbox[3]/alto))
    
    def save_annotations(anns: list, filename: str)-> None:
        """
            Guarda las anotaciones en la ruta introducida
        Args:
            anns (list): lista de anotaciones
            filename (str): fichero .json de salida
        """
        with open(filename, "w") as f:
            json.dump(anns, f)

    def update_cat_ids(self, ori_ids: list[int], news_ids: list[int]) -> dir:
        """
            Actualiza los ids de las categorías con las que se vinculan las anotaciones,
            de forma que las anotaciones que se relacionan con una categoría con un id concreto
            actualizan este id al nuevo id de esa categoría    
        Args:
            ori_ids (list[int]): ids originales
            news_ids (list[int]): ids nuevos
        Returns:
            dir: Anotaciones modificadas
        """
        # Cambiamos para cada id antiguo las anotaciones para actualizarlas
        anns_to_change = [id for id in self.coco.anns if self.coco.anns[id]["category_id"] in ori_ids]
        for new in news_ids:
            ant = ori_ids[new]
            anns_now = [ann for ann in anns_to_change if self.coco.anns[ann] == ant]
            for id in anns_now:
                self.coco.anns[id]["category_id"] = new
        
        # Devolvemos las nuevas anotaciones
        return self.coco.anns