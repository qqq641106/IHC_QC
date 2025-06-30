import logging
import os
from histoqc.BaseImage import printMaskHelper

# 组织面积比计算：(pixels_to_use/height*width)
def calc_tissue_area_ratio(s, params):
    mask = s["img_mask_use"]
    pixels_to_use = len(mask.nonzero()[0])
    height = int(s["height"])
    width = int(s["width"])
    tissue_area_ratio = pixels_to_use / (height * width) if height > 0 and width > 0 else 0
    s["tissue_area_ratio"] = tissue_area_ratio
    s.addToPrintList("tissue_area_ratio", str(tissue_area_ratio))
    return tissue_area_ratio 