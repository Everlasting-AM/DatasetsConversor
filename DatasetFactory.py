import importlib
import DatasetAdapter


class DatasetFactory:
    """Factoría de adaptadores para los datasets"""
    _instace = None
    
    # Singleton class
    def __new__(cls):
        if cls._instace is None:
            cls._instace = super().__new__(cls)
        return cls._instace
    
    def get_adapter(self, format :str, input: str) -> DatasetAdapter:
        """
            Obtiene un adaptador para el formato indicado y con la 
            ruta del dataset de entrada
        Args:
            format (str): formato del dataset
            input (str): ruta de la carpeta de dataset
        Returns:
            DatasetAdapter: adaptador de dataset 
        """
        # Classname == modulename
        classname = format + "Manager"
        package = format + "Manage"
        
        # Extraemos el módulo y la clase
        module = importlib.import_module(classname, package)
        Adaptador = getattr(module, classname)
        return Adaptador(input)
        
        