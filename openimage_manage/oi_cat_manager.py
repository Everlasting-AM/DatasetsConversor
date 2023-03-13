import pandas as pd

class OICatManager:
    def __init__(self, input: str) -> None:
        """
        Construye un manager para controlar las etiquetas del dataset
        Args:
            input (str): ruta del archivo de categorías
        """
        self.category_file = input
        # Cargamos el dataframe con la info de las categorías
        self.df = pd.read_csv(self.category_file, header=None, names=['LabelName', 'Category'])

    def extract_categories(self):
        """
            Devuelve una lista con ĺos nombres de las categorías en formato 
            textual para la lectura de estas.
        """ 
        nombres = self.df['Category']
        return nombres.tolist()

    def get_name_category(self, ident: str):
        """
            Obtiene el nombre textual de una categoría concreta
            a partir del identificador introducido
        Args:
            ident (str): cadena identificadora de la categoría
        """
        fila = self.df.loc[self.df['LabelName'] == ident]
        nombre = fila['Category'].values[0] if not fila.empty else None
        return nombre

    def get_codename_cat(self, name: str):
        """
            Devuelve el código asociado a una categoría a partir 
            de su nombre textual

            :params name: nombre textual de la catgoría
        """
        fila = self.df.loc[self.df['Category'] == name]
        code = fila['LabelName'].values[0] if not fila.empty else None
        return code
