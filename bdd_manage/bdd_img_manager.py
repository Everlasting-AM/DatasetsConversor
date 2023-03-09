import os
import shutil

NAME_IMAGES_DIR = "images"

class BddImgManager:
    def __init__(self, records: list, basedir: str) -> None:
        """
            Crea un manejador específico para la gestión de las imágenes
        Args:
            records (list): lista de registros, uno por imagen
            basedir (str): directorio base del dataset
        """
        self.data = records
        self.images_dir = os.path.join(basedir, NAME_IMAGES_DIR)
    
    def filter_images(self, cats: list[int]) -> list:
        """
            Filtra las imágenes que tienen algún objeto que pertenece a alguna
            de las categorías estudiadas.
        Args:
            cats (list[int]): categorías relevantes

        Returns:
            list: lista de entradas relevantes 
        """
        # Obtenemos los registros que tienen algún elemento relevante
        filtered_records = []
        for record in self.data:
            for lbl in record["labels"]:
                if lbl["category"] in cats:
                    filtered_records.append(record)
                    break
        # Actualizamos los datos
        self.data = filtered_records
        return filtered_records
    
    def copy_images(self, basedir: str, outdir: str):
        """
            Copia las imágenes que hay en el dataset del directorio base
            en el directorio destino
        Args:
            basedir (str): directorio base donde se encuentran las imágenes
            outdir (str): directorio destino donde se copiarán las imágenes
        """
        dir_images = os.path.join(basedir, NAME_IMAGES_DIR)
        for record in self.data:
            filename = os.path.join(dir_images, record['name'])
            salida = os.path.join(outdir, NAME_IMAGES_DIR)
            shutil.copy(filename, os.path.join(salida, record['name']))
    