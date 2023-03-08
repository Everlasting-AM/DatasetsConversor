from pycocotools.coco import COCO
import os
from aux import paramsAnalizer

EXTENSION_FILE = ".txt"
RUTA_DIR_SALIDA = "annotations-files"

def main():
    # Obtención de los argumentos
    input, output = paramsAnalizer.get_args("""Convertidor de las 
    anotaciones que se encuentran en el formato .json de COCO al formato
     YOLO de coordenadas normalizadas""")
    
    # Creación del directorio donde se almacenan los ficheros
    print("OUTPUT:", output)
    if output:
        name = paramsAnalizer.generate_out_dir_name(output)
    else:
        name = paramsAnalizer.generate_out_dir_name(RUTA_DIR_SALIDA)
    print(name)
    os.mkdir(name)
    
    # Creación del dataset
    coco = COCO(input)
    convert_to_YOLO(coco, name)

if __name__ == "__main__":
    main()