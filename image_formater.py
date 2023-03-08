import argparse
from PIL import Image

def get_args():
    parser = argparse.ArgumentParser("""Formatea las imágenes utilizadas 
    para asignarle el tamaño introducido como argumento, y crea una 
    copia de la imagen original con estas dimensiones""")
    parser.add_argument("--input", required=True, help="imagen de entrada")
    parser.add_argument("--output", required=True, help="imagen de salida")
    parser.add_argument("--new_size", required=True, help="Tamaño de la nueva imagen (anchoxalto o n para nxn)")
    return parser.parse_args()

def generate_new_image_resize(input: str, output: str, new_size: tuple[int, int]):
    x, y = new_size
    imagen = Image.open(args.input)
    imagen_salida = imagen.resize((int(x), int(y)))
    imagen_salida.save(args.output)

def main(args):
    if args.new_size.count("x"):
        x, y = args.new_size.split("x")
    else:
        x, y = args.new_size, args.new_size
    generate_new_image_resize(args.input, args.output, (x, y))

if __name__ == '__main__':
    args = get_args()
    main(args)
