import pandas as pd
from .filenames import CAT_CODE_COLUMN_NAME, CAT_NAME_COLUMN_NAME
class OICatManager:
    
    def __init__(self, input: str) -> None:
        """
        Construye un manager para controlar las etiquetas del dataset
        Args:
            input (str): ruta del archivo de categorías
        """
        self.category_file = input
        # Cargamos el dataframe con la info de las categorías
        self.df = pd.read_csv(self.category_file, header=None)
        self.df.columns = [CAT_CODE_COLUMN_NAME, CAT_NAME_COLUMN_NAME]

    def extract_categories(self):
        """
            Devuelve una lista con ĺos nombres de las categorías en formato 
            textual para la lectura de estas.
        """ 
        nombres = self.df[CAT_NAME_COLUMN_NAME]
        return nombres.tolist()

    def get_name_category(self, ident: str):
        """
            Obtiene el nombre textual de una categoría concreta
            a partir del identificador introducido
        Args:
            ident (str): cadena identificadora de la categoría
        """
        fila = self.df.loc[self.df[CAT_CODE_COLUMN_NAME] == ident]
        nombre = fila[CAT_CODE_COLUMN_NAME].values[0] if not fila.empty else None
        return nombre

    def get_codename_cat(self, name: str):
        """
            Devuelve el código asociado a una categoría a partir 
            de su nombre textual

            :params name: nombre textual de la catgoría
        """
        fila = self.df.loc[self.df[CAT_NAME_COLUMN_NAME] == name]
        code = fila[CAT_CODE_COLUMN_NAME].values[0] if not fila.empty else None
        return code

    def generate_catsfile(self, fileout: str):
        """
            Genera el archivo de salida donde se listan las categorías seleccionadas
        """
        with open(fileout, 'w') as f:
            for name in self.df[CAT_NAME_COLUMN_NAME]:
                f.write('{}\n'.format(name))
        
    
    def filter_categories(self, cats: list[str] = None, ids: list[str] = None):
        """
            Cambia el conjunto de categorías seleccionadas 
        """
        if cats is not None:
            self.df = self.df.loc[self.df[CAT_NAME_COLUMN_NAME].isin(cats)]
        if ids is not None:
            print(ids)
            self.df = self.df.loc[self.df[CAT_CODE_COLUMN_NAME].isin(ids)]
