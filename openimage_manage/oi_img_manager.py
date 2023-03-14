import pandas as pd
import os
import shutil
from filenames import IMG_ID_COL

class OIImgManager:
    def __init__(self, images_dir: str) -> None:
        self.imgs = os.listdir(images_dir)
    
    def insert_imgs(self, df: pd.DataFrame):
        """
            Extrae del dataframe el nombre de 
            las imágenes localizadas
        """
        self.imgs = list(df[IMG_ID_COL].unique())


    def copy_files(self, indir: str, outdir: str):
        """
            Copia aquellas imágenes que tienen etiquetas en el dataset
            en el directorio de salida indicado
        """
        names = [name for name in self.imgs]
        imagenes = os.listdir(indir)
        for img in imagenes:
            name, ext = os.path.splitext(img)
            if name in names:
                shutil.copy(os.path.join(indir, img), os.path.join(outdir, img))
