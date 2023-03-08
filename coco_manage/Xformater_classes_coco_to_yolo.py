from pycocotools.coco import COCO
import pycocotools.coco
import os
import argparse


def get_arguments() -> tuple[str, str]:
    """
        Extrae los argumentos de input y output de la llamada al scrip.
    Returns:
        tuple[str, str]: archivo COCO de entrada y archivo de salida .txt
    """
    parser = argparse.ArgumentParser(description="""Conversor de archivo que 
        extrae del archivo COCO las clases que serán analizadas, y se almacena
        en una archivo de salida para ser usado por YOLO""")
    input_desc = """Archivo .json que contiene una descripción de los datos del servidor""" 
    parser.add_argument("--input", type=str, required=True, dest=input_desc)
    parser.add_argument("--output", type=str, required=True, dest="Archivo .names de salida")
    
    return parser.parse_args()
    
def convert(input: str, output: str):
    """
        Extrae del archivo .json las categorias existentes en un archivo .names de 
        salida
    Args:
        input (str): archivo .json que describle el dataset
        output (str): archivo .names que indica el id y nombre de cada clase de objeto del dataset
    """
    coco = COCO(input)
    cats = coco.dataset["categories"]
    print(coco.dataset.keys())
    # Agregamos la información de cada categoría al archivo
    with open(output, "w") as f:
        for cat in cats:
            f.write("{} {}\n".format(cat["name"], cat["id"]))

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
                pycocotools.coco.COCO(input)
            except Exception:
                print("""ERROR: El archivo .json introducido no cumple el formato 
                      adecuado para COCO""")
                error = True 
    assert error

def main():
    input, output = get_arguments()
    check_arguments(input, output)
    convert(input, output)

if __name__ == "__main__":
    main()
