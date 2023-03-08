import argparse
from CocoManage import CocoManager
from graphics_items import CheckBoxList
import os

IMAGE_DIR = "images"
LABELS_DIR = "labels"

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", type=str, required=True, help="Formato del dataset")
    parser.add_argument("--dataset", type=str, required=True, help="Directorio del dataset")
    parser.add_argument("--output", type=str, required=True, help="Dataset YOLO de salida")
    parser.add_argument("--val",type=int, help="0 si el dataset se usa para entrenamiento, otro valor para validación", default=0)
    return parser.parse_args()

def check_arguments(args: argparse.Namespace):
    if os.path.isfile(args.output):
        exit("ERROR: La salida indicada ya existe y es un fichero")
    if not os.path.isdir(args.output):
        print("Creating the output dir")
        os.mkdir(args.output)
    #try:
    os.mkdir(os.path.join(args.output, IMAGE_DIR))
    os.mkdir(os.path.join(args.output, LABELS_DIR))
    #except Exception:
        
    #exit("ERROR: no se han podido crear los subdirectorios {} y {}"-format(
    #MAGE_DIR, LABELS_DIR))

def select_cats_wind(lista) -> list[str]:
    """
        Crea una ventana de selección de categoría y devuelve las categorías
        que se han seleccionado
    Returns:
        list[str]: lista las categorias seleccionadas
    """
    print(lista)
    wind = CheckBoxList(lista)
    return wind.run()
    
def main(args):
    check_arguments(args)
    # Creamos el manager
    manager = CocoManager.CocoManager(args.dataset, args.val)
    lista = select_cats_wind(manager.show_cats_names())
    manager.filter_elements_category(lista)
    manager.generate_cats_file(args.output)
    manager.generate_anns_yolo(args.output)
    manager.generate_images_filtered(args.output)

if __name__ == "__main__":
    args = get_arguments()
    main(args)