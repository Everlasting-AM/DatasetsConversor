from pycocotools.coco import COCO
import os

class CocoCatManager:
    """
        Manager para controlar las categorías de un dataset de COCO.
    """
    
    def __init__(self, coco: COCO) -> None:
        """
            Construye un manager asociado a  un dataset COCO concreto
        Args:
            coco (COCO): dataset
        """
        self.coco = coco
        
    def get_cat_names(self) -> list[str]:
        """
            Método de consulta de los nombres de las categorías disponibles en 
            el dataset.
        """
        return [self.coco.cats[cat]["name"] for cat in self.coco.cats]
        
    def generate_classes_file(self, output: str):
        """
            Extrae del dataset las categorias existentes en un archivo .names de 
            salida
        Args:
            input (str): archivo .json que describle el dataset
            output (str): archivo .names que indica el id y nombre de cada clase de objeto del dataset
        """
        ids = list(self.coco.cats)
        ids.sort()
        # Agregamos la información de cada categoría al archivo
        with open(output, "w") as f:
            for id in ids:
                f.write("{}\n".format(self.coco.cats[id]["name"]))

    def check_arguments(input:str, output:str):
        """Comprueba si el input introducido es 
            un archivo .json que se puede procesar 
            con COCO, y si el archivo introducido como output tiene el formato 
            correcto
        Args:
            input: archivo .json con la definición del dataset
            output: archivo de salida que indica las clases del dataset    
        """
        error = False
        if not input:
            print("ERROR: No se ha introducido el archivo de entrada")
            error = True
        else:
            if not os.path.exists(input):
                print("ERROR: El archivo introducido como input no existe")
                error = True
            if not input.endswith(".json"):
                print("ERROR: El archivo introducido no está en formato .json")
                error = True
            else:
                try:
                    COCO(input)
                except Exception:
                    print("""ERROR: El archivo .json introducido no cumple el formato 
                        adecuado para COCO""")
                    error = True 
        assert error

    def get_cat_ids(self, catNames: list[str])->list[int]:
        """
            Consulta lis ids de las categorías cuyo nombre se ha indicado
        Args:
            catNames (list[str]): lista de nombres de categorías

        Returns:
            list[int]: lista de identificadores 
        """
        return self.coco.getCatIds(catNms=catNames)
    
    def filter_cats(self, catIds: list[int]) -> list:
        """
            Filtra las categorías para dejar en el dataset únicamente las que se 
            introducen como argumento
        Args:
            catIds (list[int]): categgorías que queremos estudiar

        Returns:5
            list: listas de tuplas(clave, características) de cada categoría
            final  
        """
        new_cats = filter(lambda k: k in catIds, self.coco.cats)
        self.coco.dataset["categories"] = new_cats
        return new_cats

    def rename_cats(self) -> tuple[list[int], list[int]]:
        """
            Cambia los identificadores de las categorías del dataset,
            de forma que mantiene los ids en el mismo orden en el que se 
            encontraban originalmente, pero cambiando sus ids para que sean 
            contiguos y empiecen desde 0    
        Returns:
            tuple(list[int], list[int]): lista con los nuevos ids y lista 
            con los antiguos ids
        """
        # Obtenemos los nuevos ids y los antiguos
        new_cats = list(range(0, len(self.coco.cats)))
        sorted_cat_ids = list(self.coco.cats)
        sorted_cat_ids.sort()
        
        # Actualizamos la entrada de la nueva categoría si es necesario
        for new_id in new_cats:
            antiguo = sorted_cat_ids[new_id]
            if not new_id == antiguo:
                self.coco.cats[new_id] = self.coco.cats[antiguo]
                del self.coco.cats[antiguo]
        return (new_cats, sorted_cat_ids)
        
        