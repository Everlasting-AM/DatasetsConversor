import pandas as pd
from .filenames import IMG_ID_COL, CAT_CODE_COL, X1_COL, X2_COL, Y1_COL, Y2_COL
import os

class OILblManager:
    def __init__(self, labels_file: str) -> None:
        self.df = pd.read_csv(labels_file, usecols=[IMG_ID_COL, CAT_CODE_COL, X1_COL
                                                    ,X2_COL, Y1_COL, Y2_COL])
     
    def remove_labels_no_image(self, images_ids: list[str]):
        self.df = self.df.loc[self.df[IMG_ID_COL].isin(images_ids)]
        
    def filter_labels(self, cats_codes: list[str]):
        """
            Filtramos aquellas etiquetas cuya cateoría esté en la lista de 
            categorías relevantes

            :params cats_codes: lista de códigos de las categorías 
        """
        self.df = self.df.loc[self.df[CAT_CODE_COL].isin(cats_codes)]
    
    def generate_lbls_files(self, outdir: str, ordered_cats: list[str]):
        """
            Extrae del dataframe para cada imagen las etiquetas relacionadas, 
            e imprime el resultado en formato YOLO en un archivo .txt cuyo nombre
            es el identificador de la imagen.

            :param outdir: ruta del directorio donde se van a generar los ficheros.
            :param ordered_cats: lista de categorías ordenadas
        """
        # Índice de cada categoría que será usado para la conversión
        name_id = {name:idx for idx, name in enumerate(ordered_cats)}

        # Agrupamos por archivo, y para cada archivo creamos un .txt e imprimimos la info de sus etiquetas
        filenames = self.df.groupby(IMG_ID_COL)
        for filename in filenames.groups:
            with open(os.path.join(outdir, filename+".txt"), 'w') as f:
                for idx, lbl in filenames.get_group(filename).iterrows():
                    f.write('{} {} {} {} {}\n'.format(name_id[lbl[CAT_CODE_COL]], lbl[X1_COL],
                                                      lbl[Y1_COL], lbl[X2_COL], lbl[Y2_COL]))
    
    def extract_to_label(self, field: str, unique: bool = False):
        """
            Retorna una serie de pandas con los valores de todas las etiquetas
            para un atributo concreto
        Args:
            field (str): campo que se quiere obtener
            unique(bool): indica si el campo debe ser de valores únicos o no
        """
        values = self.df[field]
        return values.unique() if unique else values.values
