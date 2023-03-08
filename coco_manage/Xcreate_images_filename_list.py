import pycocotools.coco
import aux.paramsAnalizer as paramsAnalizer
import os

def write_images_on_file(coco: pycocotools.coco.COCO, out: str):
    """
        Extrae los nombres de todas las imágenes contenidas en el dataset e 
        imprime cada nombre en el archivo de salida con la ruta introducida
    Args:
        coco (pycocotools.coco.COCO): dataset COCO
        out (str): ruta del archivo de salida
    """
    with open(out, "w") as file:
        lista = [image["file_name"] for image in coco.dataset["images"]]
        for img in lista:
            file.write(img+"\n")

def check_arguments(input: str):
    """
        Comprueba si el nombre del dataset de entrada es válido
    Args:
        input (str): ruta del dataset de entrada
    """
    error = False
    if not os.path.isfile(input):
        print("ERROR: El archivo introducido no existe o es un directorio")
    elif not input.endswith(".json"):
        print("ERROR: El archivo de entrada no es un")
    

def main():
    input, salida = paramsAnalizer.get_args("""Script creador de un 
    fichero con la lista de imágenes que se encuentran en el dataset introducido 
    como input. El archivo será el que se introduzca como output o tomará 
    un nombre determinado por el sistema (output(x).txt)""")
    # Obtenemos un nombre de salida
    if not salida:
        salida = paramsAnalizer.generate_out_file(".txt")
    else:
        salida = paramsAnalizer.generate_out_file(".txt", name=salida)




if __name__ == '__main__':
    main()
