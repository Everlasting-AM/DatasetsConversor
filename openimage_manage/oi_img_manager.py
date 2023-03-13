import cv2
import shutil

class OIImgManager:
    
    def __init__(self, lbl_df) -> None:
        self.lbl_df = lbl_df
    
    def copy_files(self, indir: str, outdir: str):
        names = [name+".jpg" for name in self.lbl_df['ImageID']]

