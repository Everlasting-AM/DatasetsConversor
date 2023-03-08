import concurrent.futures
import threading
import queue

class BddCatManager:
    
    def __init__(self, data:list[str]) -> None:
        """
            Crea un manager específico para la gestión de las categorías de 
            objetos identificados en el dataset
        Args:
            data (list[str]): lista de registros del dataset introducido
        """
        self.data = data
        self.categories = []
    
    
    def _extract_categories_subelements(entries: list, results: queue.Queue) -> set[str]:
        """
            Extrae las categorías de una sublista de elementos tomada de la 
            lista original 
        Args:
            entries (list): lista de entradas del dataset    
        Returns:
            set[str]: conjunto de categorías del dataset
        """
        cats = set()
        for entry in entries:
            for label in entry['labels']:
                cats.add(label['category']) 
        results.put(cats)
    
    def extract_categories(self) -> list[str]:
        """
            Extrae los del dataset las categorías existentes
        Returns:
            list[str]: lista de categorías
        """
        num_workers = 6
        threads = []
        results = queue.Queue()
        size = len(self.data) // num_workers
        # Lanzamos los procesos
        for i in range(num_workers):
            t = threading.Thread(target=BddCatManager._extract_categories_subelements,
                                 args=(self.data[i*size:i*(size+1)], results))
            t.start()
            threads.append(t)
            
        # Comprobamos si queda una parte sin tratar
        if num_workers * size < len(self.data):
            BddCatManager._extract_categories_subelements(self.data[num_workers * size: len(self.data)], results)
        
        # Unimos los resultados
        for t in threads: 
            t.join()
        categorias = set()
        while not results.empty():
            categorias |= results.get()
        self.categories = list(categorias)
        return self.categories
    
    def extract_categories_sequential(self) -> list[str]:
        """
            Extrae los del dataset las categorías existentes
        Returns:
            list[str]: lista de categorías
        """
        categorias = set()
        for entry in self.data:
            for label in entry["labels"]:
               categorias.add(label['category']) 
        self.categories = list(categorias)
        return self.categories
    
    def generate_cats_file(self, fileout: str) -> None:
        """
            Genera el archivo de categorías en con la ruta indicada
        Args:
            fileout (str): ruta del archivo de categorías que se va a crear
        """
        with open(fileout, "w") as f:
            for cat in self.categories:
                f.write("{}\n".format(cat))


