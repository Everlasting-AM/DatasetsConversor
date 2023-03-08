from pycocotools.coco import COCO
import json
import aux.paramsAnalizer as paramsAnalizer
import tkinter as tk

class CheckBoxList:
    """
        Clase que representa el elemento gráfico CheckBoxList, que representa
        una ventana en la que se muestra una lista de opciones, permite 
        seleccionar múltiples opciones y en caso de que se haga click en el 
        botón de aceptar se retornará la lista de las opciones elegidas
    """
    def __init__(self, items: list[str]) -> None:
        # Gestión de los elementos de la lista
        self.items = items
        self.selected_items = []

        # Creacción del root
        self.root = tk.Tk()
        self.root.title("Lista de categorías")
        self.root.configure(bg="white")

        # Creamos los elementos de la interfaz gráfica
        self.frame = tk.Frame(self.root)
        self.scrollbar = tk.Scrollbar(self.frame)
        self.listbox = tk.Listbox(self.frame, selectmode='multiple', 
        yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.button_accept = tk.Button(self.root, text="Aceptar", 
        command=self.accept_selection)
        self.button_clear = tk.Button(self.root, text="Limpiar",
        command=self.clear_selection)
        
        # Insertamos los elementos a la lista
        for item in items:
            self.listbox.insert(tk.END, item)
        
        # Añadir los elementos a la ventana
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill='both', expand=1)
        self.frame.pack(fill='both', expand=1)
        self.button_accept.pack()
        self.button_clear.pack()
    
    def run(self) -> list[str]:
        """
            Ejecuta la ventana, y no termina hasta que esta no sea cerrada.
        Returns:
            list[str]: elementos de la lista que se han elegido
        """
        self.root.mainloop()
        return self.selected_items
    
    def accept_selection(self):
        """
            Acción realizada cuando se pulsa el botón de aceptar, almacena los 
            elementos seleccionados dentro del objeto ventana
        """
        self.selected_items = [self.listbox.get(idx) for idx in 
                               self.listbox.curselection()]
        self.root.destroy()

    def clear_selection(self):
        """
            Limpia la ventana para poder elegir nuevos elementos diferentes
        """
        self.listbox.selection_clear(0, tk.END)

def get_ann_some_cat(coco: COCO, cat_ids: list[int]) -> list:
    """
        Obtiene las anotaciones sobre las categorías concretas indicadas
    Args:
        coco (COCO): dataset del que se extrae la información
        cat_ids (list[int]): ids de las categorías de las que se quiere extraer 
        las anotaciones relacionadas
    Returns:
        list: Lista con las anotaciones encontradas
    """
    ann_ids = set()
    for id in cat_ids:
        ann_ids = ann_ids.union(coco.getAnnIds(catIds=id))
    return coco.loadAnns(ids = list(ann_ids))

def get_images_some_cat(coco: COCO, cat_ids: list[int]) -> list:
    """
        Obtiene las imágenes que contienen objetos de una serie de categorías
    Args:
        coco (COCO): dataset de entrada
        cat_ids (list[int]): ids de las categorías buscadass 

    Returns:
        list: Imágenes que contienen algún objeto de las categorías buscadas
    """
    img_ids = set()
    for id in cat_ids:
        img_ids = img_ids.union(coco.getImgIds(catIds=id))
    return coco.loadImgs(ids = list(img_ids))

def create_window_selecction(coco: COCO) -> CheckBoxList:
    """
        Crea una ventana para la selección de las categorías buscadas. Mostrará 
        como posible opción todas las categorías del dataset
    Args:
        coco (COCO): dataset de entrada

    Returns:
        CheckBoxList: ventana para la selección de categorías
    """
    lista = [cat['name'] for cat in coco.loadCats(ids=coco.getCatIds())]
    print(lista)
    ventana = CheckBoxList(lista)
    return ventana

def renombrar_categoria(anns: list, cats: list):
    """
        Busca en una lista de anotaciones todas las anotaciones sobre un
        objeto de una categoría concreta y le cambien el id. 
        Posteriormente se cambia el id de la propia cateogría, con el fín
        de que tenga sentido la numeración cuando se cree el nuevo dataset
        con número reducido de categorías
    Args:
        anns (list): lista de anotaciones que modificar
        cats (list): nueva lista de categorías 
    """
    new_tam = len(cats)
    nuevos_ids = list(range(new_tam))

    # Lista original de cats_ids
    ids = [cat['id'] for cat in cats]
    ids.sort()

    print(anns[0]['category_id'])
    for ann in anns:
        ann['category_id'] = nuevos_ids[ids.index(ann['category_id'])]
    print(anns[0]['category_id'])

    for cat in cats:
        cat['id'] = nuevos_ids[ids.index(cat['id'])]

def main():
    input, output = paramsAnalizer.get_args("""Script para filtrar de la 
    lista de anotaciones del dataset las que son relevantes para el caso
     de estudio concreto""")
    if not output:
        paramsAnalizer.generate_out_file(extent=".json")
    # Creamos el dataset COCO
    coco = COCO(input)

    # Creamos y ejecutamos la ventana de selección
    wind = create_window_selecction(coco)
    lista = wind.run()
    print("Elementos seleccionados:", lista)

    # Obtener categorías de vehículos
    cat_ids = coco.getCatIds(catNms=lista)
    print(cat_ids)
    cats = coco.loadCats(ids= cat_ids)

    # Obtenemos las anotaciones que contienen algunas de las categorías
    anns = get_ann_some_cat(coco, cat_ids)
    
    # Obtenemos las imágenes que contienen algunas de las categorías
    images = get_images_some_cat(coco, cat_ids)

    renombrar_categoria(anns, cats) 
    print(anns[0]['category_id'])

    # Imprimimos el número de imágenes
    print("Num images: ", len(images))
    
    # Guardamos las anotaciones filtradas en un nuevo archivo
    filtered_annts = {"info": coco.dataset["info"], "images": images, 
    "annotations": anns, "categories": [{"id": cat["id"], 
    "name": cat["name"]} for cat in cats]}

    # Guardamos los datos en el archivo .json
    with open(output, "w") as f:
        json.dump(filtered_annts, f)
        
if __name__ == '__main__':
    main()