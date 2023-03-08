import abc

class DatasetAdapter(abc.ABC):
    @abc.abstractclassmethod
    def filter_elements_category(self, cats: list[str]):
        pass
    
    @abc.abstractclassmethod
    def generate_anns_yolo(self, dir_out: str):
        pass
    
    @abc.abstractclassmethod
    def generate_cats_file(self, fileout: str):
        pass
    
    @abc.abstractclassmethod
    def show_cats_names(self) -> list[str]:
        pass