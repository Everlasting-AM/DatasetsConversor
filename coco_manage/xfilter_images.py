import json
from pycocotools.coco import COCO
from PIL import Image
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os 
import shutil
from sys import path
import json
import argparse
import aux.paramsAnalizer as paramsAnalizer


def copy_files_to_special_folder(images: list[str], new_folder: str, 
                                 last_folder: str) -> None:
    """
        Copia los archivos en los paths introducidos en un directorio
        de archivos relevantes creados cuando se llama a la función
    Args:
        images (list[str]): lista de imágenes que se va a copiar
        new_folder (str): ruta carpeta destino
        last_folder (str): ruta carpeta origen
    """
    # Crea el directorio
    try:
        folder = new_folder
        os.mkdir(new_folder)
    except FileExistsError:
        reps = 1
        while True:
            try:
                os.mkdir(new_folder +'(' + str(reps) + ')')
                folder = new_folder +'(' + str(reps) + ')'
                break
            except FileExistsError:
                reps+=1

    for image in images:
        new_path = os.path.join(folder, image)
        shutil.copy(last_folder + image, new_path)
    
def get_boxes_elements(image_id: int, coco:COCO, catlistAny=[]) -> list:
    """
        Obtiene los objestos boxes de cada objeto identificado en la
        imagen, de forma que se puede acceder a su posición
    Args:
        image_id (int): id de la imagen
        coco (COCO): dataset de entrada 
        catlistAny (list, optional): lista de categorías de los objetos de los 
        que queremos obtener el box. Defaults to [].

    Returns:
        list: lista de boxes de las anotaciones de la imagen y objetos buscados
    """
    # Obtenemos todas las anotaciones para la imagen concreta y la categoría 
    annot_ids = []
    for cat in catlistAny:
        annot_ids_cat = coco.getAnnIds(imgIds= image_id, catIds= cat)
        annot_ids += annot_ids_cat
    
    anns = coco.loadAnns(ids=annot_ids)
    return [ann['bbox'] for ann in anns]

def print_boxes(image: Image, boxes: list) -> None:
    """
        Imprime los boxes la lista de boxes de la imagen concreta, mostrando la 
        imagen y los boxes asociados. 
    Args:
        image (Image): Imagen analizada
        boxes (list): Lista de elementos de la imagen
    """
    # Añadimos los boxes
    fig, ax = plt.subplots()
    for box in boxes:
        bb = patches.Rectangle((box[0], box[1]), box[2], box[3], linewidth=2, 
                               edgecolor="blue", facecolor="none")
        ax.add_patch(bb)
    
    # Imprimimos la imagen
    ax.imshow(image)
    plt.show()

def get_filename_images(coco: COCO, image_ids: list[int]) -> list[str]:
    """
        Obtiene los nombres de las imágenes contenidas en el dataset de entrada,
        y que tengan el id contenido en la lista de ids introducida.
    Args:
        coco (COCO): dataset de entrada
        image_ids (list[int]): lista de ids de las imágenes buscadas

    Returns:
        list[str]: lista con los nombres de las imágenes
    """
    images = coco.loadImgs(ids=image_ids)
    return [img['file_name'] for img in images]

def copy_files_id_other_folder(coco: COCO, image_ids: list[int], new_dir: str, 
                               last_dir: str) -> None:
    """
        Copia los archivos cuyo id está en la lista introducida a una carpeta 
        diferente.
    Args:
        coco (COCO): dataset de entrada
        image_ids (list[int]): ids de las imágenes buscadas
        new_dir (str): carpeta destino
        last_dir (str): carpeta origen
    """
    paths = get_filename_images(coco, image_ids)
    copy_files_to_special_folder(paths, new_dir, last_dir)

def filter_annotations(coco: COCO, cat_ids:list[int]) -> list:
    """
        FIltra las anotaciones del dataset que hacen referencia a una categoría
        concreta.
    Args:
        coco (COCO): dataset de entrada
        cat_ids (list[int]): ids de las categorías buscadas
    Returns:
        list: lista de las anotaciones buscadas
    """
    anns = set()
    for id in cat_ids:
        anns = anns.union(coco.getAnnIds(catIds=id))
    return coco.loadAnns(ids = anns)

def save_annotations(anns: list, filename: str)-> None:
    """
        Guarda las anotaciones en la ruta introducida
    Args:
        anns (list): lista de anotaciones
        filename (str): fichero .json de salida
    """
    with open(filename, "w") as f:
        json.dump(anns, f)

def tratar_argumentos()->None:
    """
        Tratamiento de los argumentos principales que recibe el script.
    """
    # Añadimos el parser y los argumentos 
    parser = argparse.ArgumentParser(description="""Programa que realiza 
    un filtrado de las imágenes de un dataset para extraer las que 
    cumplen una condición concreta (inicialmente las que contienen 
    vehículos)""")
    parser.add_argument("--input_anns", required=True, type=str)
    parser.add_argument("--input_files", required=True, type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    # Asignamos un output
    if not args.output:
        output = paramsAnalizer.generate_out_dir_name("filtered-images")
    else:
        output = args.output

    # Devolvemos los tres atributos relevantes
    return (args.input_anns, args.input_files, output)

def main():
    anns_file, files_dir, output = tratar_argumentos()
    coco = COCO(anns_file)

    # Get list of category_ids, here [2] for bicycle
    print("Categorías con ese nombre:")
    category_ids = coco.getCatIds()
    print(category_ids)

    # Get list of image_ids which contain bicycles:
    image_ids_total = set()
    for cad in category_ids:
        image_ids_cad = coco.getImgIds(catIds=cad)
        image_ids_total = image_ids_total.union(image_ids_cad)

    print("Tamaño total:",len(image_ids_total))
    
    # Filtrado de imágenes
    copy_files_id_other_folder(coco, image_ids_total, output, files_dir)
    

if __name__ == '__main__':
    main()