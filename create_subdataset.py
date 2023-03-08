import argparse
import os
import math
import shutil

NAME_IMAGES = "images"
NAME_LABELS = "labels"

def arg_parse():
    """
        Sgrega los argumentos necesarios para poder introducir el directorio de
        imágenes, etiquetas, directorio de salida donde se crearán las carpetas
        con los subdatasets y el tamaño de cada subdataset
    """
    parser = argparse.ArgumentParser(description="""Crea diferentes secciones 
                                    de un dataset, de igual tamaño cada una""")
    parser.add_argument("--images", required=True, type=str, help="""Directorio
                        que almacena las imágenes del dataset""")
    parser.add_argument("--labels", required=True, type=str, help="""Etiquetas
                        de las imágenes del dataset""")
    parser.add_argument("--output", required=True, type=str, help="""
                        Directorio donde se crearán las carpetas con los
                        diferentes subdatasets""")
    parser.add_argument("--partsz", required=True, type=int, help="""Tamaño
                        de cada subdataset resultante""")
    return parser.parse_args()

def check_arguments(args) -> bool:
    # Check images dir
    if not os.path.isdir(args.images):
        print("ERROR: el directorio de imágenes introducido no existe")
        return False
    # Check labels dir
    if not os.path.isdir(args.labels):
        print("ERROR: el directorio de etiquetas no existe")
        return False
    # Check output dir
    if not os.path.exists(args.output):
        print("WARNING: el directorio de salida no existe, se creará uno nuevo")
    # Check part size
    long = len(os.listdir(args.images))
    if args.partsz < 0:
        print("ERROR: el valor de cada subdataset debe ser al menos mayor que 0")
        return False
    if args.partsz >= long:
        print("""ERROR: el tamaño de cada subdataset debe ser menor que el
            tamaño del original""")
        return False
    return True


def create_dirs(n: int, out: str, sub_name: str ="part"):
    """
        Crea tantos directorios como indique el argumento n dentro del directorio
        out. Cada directorio tendrá asociado un nombre, que se podrá introducir 
        como argumento opcional, seguido de un valor según el orden de creación 
        E.j(dir, dir1, dir2).
        Cada directorio tendrá dentro una carpeta para introducir las imágenes y 
        otra carpeta para introducir las etiquetas asociadas a las imágenes
    """
    names = [os.path.join(out, sub_name + str(i)) if i else 
             os.path.join(out, sub_name)for i in range(1, n)]
    # Creacción directorios
    for name in names:
        os.makedirs(os.path.join(name, NAME_IMAGES),exist_ok=True)
        os.makedirs(os.path.join(name, NAME_LABELS),exist_ok=True)
    return names

def get_division_index(img_dir: str, n: int):
    """
        Dado el directorio de imágenes indica que elementos del directorio son
        en los que se debe realizar la división (desde 0 hasta n-1, n
        hasta n2-1,...)
    """
    elems = os.listdir(img_dir)
    leng = len(elems)
    slices_completed = leng//n
    indexes = [i * n for i in range(1, slices_completed)]
    return indexes

def copy_elemens_subdatasets(indexes: list[int], subdatasets: list[str], 
                             images: str, labels:str):
    """
        Copia los elementos las imágenes de images, y labels de labels en
        los subdatasets indicados, tomando como puntos límite los indicados
        por los índices introducidos
    """
    tam = indexes[0]
    # Listas de elementos
    imgs = os.listdir(images)
    imgs.sort()
    lbls = os.listdir(labels)
    lbls.sort()
    image_elems = [os.path.join(images, image) for image in imgs]
    label_elems = [os.path.join(labels, lbl) for lbl in lbls]

    
    # Para cada directorio introducimos los elementos
    begin, end = 0, 0
    for sub in subdatasets:
        end += indexes[0]
        for img in image_elems[begin:end]:
            print(sub)
            shutil.copy2(img, os.path.join(sub, NAME_IMAGES))
        for lbl in label_elems[begin:end]:
            shutil.copy2(lbl, os.path.join(sub, NAME_LABELS))
        begin = end


def main(args):
    if check_arguments(args):
        print("Argumentos correctos, se inicia la división")
        names = create_dirs(math.ceil(len(os.listdir(args.images))/args.partsz), 
                    args.output)
        index = get_division_index(args.images, args.partsz)
        copy_elemens_subdatasets(index, names, args.images, args.labels)
    
if __name__ == '__main__':
    args = arg_parse()
    main(args)