from pycocotools.coco import COCO

coco = COCO("../labels_train.json")
print(len(coco.imgs))