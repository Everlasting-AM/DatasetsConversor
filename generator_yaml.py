import argparse
from aux_packet import params_analizer

def main():
    # Definimos el parser
    parser = argparse.ArgumentParser(description="""Generador de archivo YAML dado 
    los archivos de entrada para poder entrenar a un modelo YOLO""")
    sections_needed = ["train", "val"]
    field_needed = ["images", "annotations", "images_name"]
    for secc in sections_needed:
        for field in field_needed:
            parser.add_argument("--{}_{}".format(secc, field), type=str
            , required=True)
    parser.add_argument("--classes_file", type=str, required=True)
    parser.add_argument("--output", type=str)

    # Extraemos los argumentos
    args = parser.parse_args()
    if not args.output:
        salida = params_analizer.generate_out_file(extent=".yaml")
    else:
        salida = params_analizer.generate_out_file(".yaml", name= args.output)


    # Escribimos los argumentos introducidos en el fichero .yaml de salida
    argumentos = vars(args)
    with open(salida, 'w') as f:
        for sec in sections_needed:
            f.write("{}:\n".format(sec))
            for field in field_needed:
                key = "{}_{}".format(sec, field)
                f.write("\t{}: {}\n".format(key, argumentos[key]).expandtabs())
        f.write("names:\n\t{}".format(argumentos["classes_file"]).expandtabs())

if __name__ == "__main__":
    main()