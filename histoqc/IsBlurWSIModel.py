import numpy as np
import cv2
import random


def isWSIblur(s, params):
    """
    判断WSI是否模糊。最高分辨率下基于Tenengrad算法，参考WSIBlurEvaluator原理。
    结果通过s.addToPrintList输出。
    支持参数同demo。
    """
    tile_size = int(params.get("tile_size", 512))
    num_tiles = int(params.get("num_tiles", 10))
    stride = int(params.get("stride", 512))
    min_fg_ratio = float(params.get("min_fg_ratio", 0.01))
    min_tile_coverage = float(params.get("min_tile_coverage", 0.5))
    cutoff = float(params.get("cutoff", 1000))
    tissue_level = int(params.get("tissue_level", 2))

    # 1. 用低倍缩略图生成掩码
    osh = s["os_handle"]
    dims = osh.level_dimensions[tissue_level]
    img = np.array(osh.read_region((0, 0), tissue_level, dims))[:, :, :3]
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
    mask_bin = (mask > 0).astype(np.uint8)
    h, w = mask_bin.shape

    # 2. 计算level 0与mask层的缩放率
    level0_dims = osh.level_dimensions[0]
    rescale_rate_w = level0_dims[0] / w
    rescale_rate_h = level0_dims[1] / h
    rescale_rate = (rescale_rate_w + rescale_rate_h) / 2

    scale_tile_size = int(tile_size / rescale_rate)
    scale_stride = int(stride / rescale_rate)

    tile_coords = []
    fg_ratios = []

    # 3. 在低倍mask上滑窗，找到组织tile
    for x in range(0, h - scale_tile_size + 1, scale_stride):
        for y in range(0, w - scale_tile_size + 1, scale_stride):
            tile_mask = mask_bin[x:x + scale_tile_size, y:y + scale_tile_size]
            fg_ratio = np.sum(tile_mask) / (scale_tile_size ** 2)
            if fg_ratio >= min_fg_ratio:
                x0 = int(y * rescale_rate)
                y0 = int(x * rescale_rate)
                tile_coords.append((x0, y0))
                fg_ratios.append(fg_ratio)

    if not tile_coords:
        s.addToPrintList("mean_WSI_blur_score", -100)
        # s.addToPrintList("is_blur", "NA")
        # s.addToPrintList("tile_scores", "NA")
        s["warnings"].append(f"{s['filename']} - isWSIblur: No valid tiles found for blur evaluation.")
        return

    fg_ratios = np.array(fg_ratios)
    tile_coords = np.array(tile_coords)
    sort_idx = np.argsort(-fg_ratios)
    tile_coords_sorted = tile_coords[sort_idx]

    N = len(tile_coords_sorted)
    top_n = max(int(N * 0.5), num_tiles)
    candidate_tiles = tile_coords_sorted[:top_n]

    if len(candidate_tiles) < num_tiles:
        selected_tiles = candidate_tiles
    else:
        indices = random.sample(range(len(candidate_tiles)), num_tiles)
        selected_tiles = candidate_tiles[indices]

    def calc_tenengrad(img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        grad_sq = gx ** 2 + gy ** 2
        return np.mean(grad_sq)

    scores = []
    for (x, y) in selected_tiles:
        tile = osh.read_region((x, y), 0, (tile_size, tile_size))
        tile = np.array(tile.convert("RGB"))
        roi_mask = mask_bin[int(y / rescale_rate):int(y / rescale_rate) + scale_tile_size,
                   int(x / rescale_rate):int(x / rescale_rate) + scale_tile_size]
        fg = np.sum(roi_mask) / (scale_tile_size ** 2)
        if fg < min_tile_coverage:
            continue
        score = calc_tenengrad(tile)
        scores.append(score)

    # 如果scores为空，强行用组织最多的前num_tiles个tile，不再过滤
    if not scores and len(selected_tiles) > 0:
        scores = []
        for (x, y) in selected_tiles:
            tile = osh.read_region((x, y), 0, (tile_size, tile_size))
            tile = np.array(tile.convert("RGB"))
            score = calc_tenengrad(tile)
            scores.append(score)
        s["warnings"].append(f"{s['filename']} - isWSIblur: No tile passed min_tile_coverage, using all candidate tiles as fallback.")

    if not scores:
        s.addToPrintList("mean_WSI_blur_score", -100)
        # s.addToPrintList("is_blur", "NA")
        # s.addToPrintList("tile_scores", "NA")
        s["warnings"].append(f"{s['filename']} - isWSIblur: No valid tiles passed min_tile_coverage for blur evaluation.")
        return

    mean_score = float(np.mean(scores))
    s.addToPrintList("mean_WSI_blur_score", mean_score)
    # s.addToPrintList("tile_scores", ",".join(f"{v:.1f}" for v in scores))
    # is_blur = mean_score >= cutoff
    # s.addToPrintList("is_blur", int(is_blur))
    # if not is_blur:
    #     s["warnings"].append(f"{s['filename']} - isWSIblur: mean_score={mean_score:.1f} < cutoff={cutoff}, likely blurry.")

    return
