from DatasetAdapter import DatasetAdapter
from x_cat_manager import x_cat_manager
from x_img_manager import x_img_manager
from x_lbl_manager import x_lbl_manager

class x_manager(DatasetAdapter):
    def __init__(self, out: str) -> None:
        super().__init__()
    
    def check_arguments(input: str):
        pass

    def filter_elements_category(self, cats: list[str]):
        pass
    
    def generate_anns_yolo(self, dir_out: str):
        pass
    
    def generate_cats_file(self, fileout: str):
        pass
    
    def show_cats_names(self) -> list[str]:
        pass
    
    def generate_images_filtered(self, output: str):
        pass