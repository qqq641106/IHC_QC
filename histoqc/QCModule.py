import logging

# 全局控制是否写入_threshold结果
WRITE_THRESHOLD = False


def get_float_value(s, key, default=None):
    """从s中获取并转为float，含日志处理"""
    value = s.get(key)
    if value is None:
        logging.warning(f"{key} not found in metadata for {s['filename']}")
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        logging.error(f"{key} value must be numeric, got {type(value)}")
        return None


def add_qc_result(s, key, result, **kwargs):
    """添加QC结果"""
    s.addToPrintList(key, result)
    for k, v in kwargs.items():
        # 只有当WRITE_THRESHOLD为False且参数名以"_threshold"结尾时才跳过
        if not WRITE_THRESHOLD and k.endswith('_threshold'):
            continue
        s.addToPrintList(k, v)


def qc_tissue_area_ratio(s, params):
    logging.info(f"{s['filename']} - \tqc_tissue_area_ratio")
    threshold = float(params.get("threshold", 0.005))
    tissue_area_ratio = get_float_value(s, 'tissue_area_ratio')
    if tissue_area_ratio is None:
        return

    # 可以插入更多自定义前后处理
    qc_result = 1 if tissue_area_ratio >= threshold else 0
    add_qc_result(s, 'qc_tissue_area_ratio', qc_result,
                  qc_tissue_area_ratio_threshold=threshold)


def qc_pixels_to_use(s, params):
    logging.info(f"{s['filename']} - \tqc_pixels_to_use")
    threshold = float(params.get("threshold", 20000))
    pixels_to_use = get_float_value(s, 'pixels_to_use')
    if pixels_to_use is None:
        return

    qc_result = 1 if pixels_to_use >= threshold else 0
    add_qc_result(s, 'qc_pixels_to_use', qc_result,
                  qc_pixels_to_use_threshold=threshold)


def qc_pen_markings(s, params):
    logging.info(f"{s['filename']} - \tqc_pen_markings")
    threshold = float(params.get("threshold", 0.05))
    pen_markings = get_float_value(s, 'pen_markings')
    if pen_markings is None:
        return

    qc_result = 1 if 0 <= pen_markings <= threshold else 0
    add_qc_result(s, 'qc_pen_markings', qc_result,
                  qc_pen_markings_threshold=threshold)


def qc_coverslip_edge(s, params):
    logging.info(f"{s['filename']} - \tqc_coverslip_edge")
    threshold = float(params.get("threshold", 0.01))
    coverslip_edge = get_float_value(s, 'coverslip_edge')
    if coverslip_edge is None:
        return

    qc_result = 1 if 0 <= coverslip_edge <= threshold else 0
    add_qc_result(s, 'qc_coverslip_edge', qc_result,
                  qc_coverslip_edge_threshold=threshold)


def qc_background_rms_contrast(s, params):
    logging.info(f"{s['filename']} - \tqc_background_rms_contrast")
    threshold = float(params.get("threshold", 0.2581))
    value = get_float_value(s, 'background_rms_contrast')
    if value is None:
        return

    qc_result = 1 if value < threshold else 0
    add_qc_result(s, 'qc_background_rms_contrast', qc_result,
                  qc_background_rms_contrast_threshold=threshold)


def qc_background_tenenGrad_contrast(s, params):
    logging.info(f"{s['filename']} - \tqc_background_tenenGrad_contrast")
    threshold = float(params.get("threshold", 0.00122))
    value = get_float_value(s, 'background_tenenGrad_contrast')
    if value is None:
        return

    qc_result = 1 if value < threshold else 0
    add_qc_result(s, 'qc_background_tenenGrad_contrast', qc_result,
                  qc_background_tenenGrad_contrast_threshold=threshold)


def qc_background_michelson_contrast(s, params):
    logging.info(f"{s['filename']} - \tqc_background_michelson_contrast")
    threshold = float(params.get("threshold", 1))
    value = get_float_value(s, 'background_michelson_contrast')
    if value is None:
        return

    qc_result = 1 if value <= threshold else 0
    add_qc_result(s, 'qc_background_michelson_contrast', qc_result,
                  qc_background_michelson_contrast_threshold=threshold)


def qc_background_grayscale_brightness(s, params):
    logging.info(f"{s['filename']} - \tqc_background_grayscale_brightness")
    threshold = float(params.get("threshold", 0.9370))
    value = get_float_value(s, 'background_grayscale_brightness')
    if value is None:
        return

    qc_result = 1 if value >= threshold else 0
    add_qc_result(s, 'qc_background_grayscale_brightness', qc_result,
                  qc_background_grayscale_brightness_threshold=threshold)


def qc_background_grayscale_brightness_std(s, params):
    logging.info(f"{s['filename']} - \tqc_background_grayscale_brightness_std")
    threshold = float(params.get("threshold", 0.03223))
    value = get_float_value(s, 'background_grayscale_brightness_std')
    if value is None:
        return

    qc_result = 1 if value <= threshold else 0
    add_qc_result(s, 'qc_background_grayscale_brightness_std', qc_result,
                  qc_background_grayscale_brightness_std_threshold=threshold)


def qc_deconv_c0_mean(s, params):
    logging.info(f"{s['filename']} - \tqc_deconv_c0_mean")
    threshold = float(params.get("threshold", 0.0087))
    value = get_float_value(s, 'deconv_c0_mean')
    if value is None:
        return

    qc_result = 1 if value >= threshold else 0
    add_qc_result(s, 'qc_deconv_c0_mean', qc_result,
                  qc_deconv_c0_mean_threshold=threshold)


def qc_small_tissue_removed_percent(s, params):
    logging.info(f"{s['filename']} - \tqc_small_tissue_removed_percent")
    threshold = float(params.get("threshold", 0.5))
    value = get_float_value(s, 'small_tissue_removed_percent')
    if value is None:
        return

    qc_result = 1 if value <= threshold else 0
    add_qc_result(s, 'qc_small_tissue_removed_percent', qc_result,
                  qc_small_tissue_removed_percent_threshold=threshold)


def qc_mean_WSI_blur_score(s, params):
    logging.info(f"{s['filename']} - \tqc_mean_WSI_blur_score")
    threshold = float(params.get("threshold", 1000))
    value = get_float_value(s, 'mean_WSI_blur_score')
    if value is None:
        return

    qc_result = 1 if value >= threshold else 0
    add_qc_result(s, 'qc_mean_WSI_blur_score', qc_result,
                  qc_mean_WSI_blur_score_threshold=threshold)


def qc_summary(s, params):
    """
    qc结果汇总，汇总方式： 失败0，警告1，pass2
    error = [qc_pen_markings, qc_pixels_to_use, qc_deconv_c0_mean, qc_mean_WSI_blur_score]
    warning = [qc_background_rms_contrast, qc_background_tenenGrad_contrast, qc_background_michelson_contrast, qc_background_grayscale_brightness, qc_background_grayscale_brightness_std, qc_coverslip_edge, qc_small_tissue_removed_percent]

    QC_ERROR_MESSAGES = {
        'qc_pen_markings': "检测到切片上存在笔迹，建议重新制片或去除笔迹后扫描。",
        'qc_pixels_to_use': "有效组织区域过小，无法进行后续分析，请检查切片质量或扫描范围。",
        'qc_deconv_c0_mean': "染色分离C0通道信号过低，染色质量不达标，建议重染色或检查扫描仪参数。",
        'qc_mean_WSI_blur_score': "全片模糊评分过低，图像模糊，建议重新扫描。"}

    QC_WARNING_MESSAGES = {
        'qc_background_rms_contrast': "背景RMS对比度异常，图像背景复杂度较高，分析结果可能受影响，请复核切片背景或考虑重新制备。",
        'qc_background_tenenGrad_contrast': "背景TenenGrad对比度异常，背景锐度较低，建议复查切片或扫描参数。",
        'qc_background_michelson_contrast': "背景Michelson对比度异常，可能存在背景亮度不均，分析结果可靠性下降。",
        'qc_background_grayscale_brightness': "背景灰度亮度异常，可能因扫描仪设置或染色导致，请关注分析结果。",
        'qc_background_grayscale_brightness_std': "背景灰度亮度标准差异常，背景亮度分布异常，建议复查切片。",
        'qc_coverslip_edge': "检测到盖玻片边缘伪影，可能影响部分区域分析，请关注相关区域。",
        'qc_small_tissue_removed_percent': "小组织移除百分比过高，组织碎片较多，分析结果可能不完全可靠。"}

    如果error中任意一个为0，则结果为0
    如果error中没有0，那么任意一个warning为1，则结果为1
    如果error和warning中都没有0，则结果为2
    """

    error_items = [
        'qc_pen_markings', 'qc_pixels_to_use',
        'qc_deconv_c0_mean', 'qc_mean_WSI_blur_score'
    ]
    warning_items = [
        'qc_background_rms_contrast', 'qc_background_tenenGrad_contrast',
        'qc_background_michelson_contrast', 'qc_background_grayscale_brightness',
        'qc_background_grayscale_brightness_std', 'qc_coverslip_edge',
        'qc_small_tissue_removed_percent'
    ]
    QC_ERROR_MESSAGES = {
        'qc_pen_markings': "检测到切片上存在笔迹，建议重新制片或去除笔迹后扫描。",
        'qc_pixels_to_use': "有效组织区域过小，无法进行后续分析，请检查切片质量或扫描范围。",
        'qc_deconv_c0_mean': "染色分离C0通道信号过低，染色质量不达标，建议重染色或检查扫描仪参数。",
        'qc_mean_WSI_blur_score': "全片模糊评分过低，图像模糊，建议重新扫描。"}

    QC_WARNING_MESSAGES = {
        'qc_background_rms_contrast': "背景RMS对比度异常，图像背景复杂度较高，分析结果可能受影响，请复核切片背景或考虑重新制备。",
        'qc_background_tenenGrad_contrast': "背景TenenGrad对比度异常，背景锐度较低，建议复查切片或扫描参数。",
        'qc_background_michelson_contrast': "背景Michelson对比度异常，可能存在背景亮度不均，分析结果可靠性下降。",
        'qc_background_grayscale_brightness': "背景灰度亮度异常，可能因扫描仪设置或染色导致，请关注分析结果。",
        'qc_background_grayscale_brightness_std': "背景灰度亮度标准差异常，背景亮度分布异常，建议复查切片。",
        'qc_coverslip_edge': "检测到盖玻片边缘伪影，可能影响部分区域分析，请关注相关区域。",
        'qc_small_tissue_removed_percent': "小组织移除百分比过高，组织碎片较多，分析结果可能不完全可靠。"}

    QC_PASS_MESSAGE = "QC pass"

    error_values = [int(s.get(item, 0)) for item in error_items]
    for idx, v in enumerate(error_values):
        if v == 0:
            qc_field = error_items[idx]
            msg = QC_ERROR_MESSAGES.get(qc_field, f"{qc_field} 未通过QC，请检查。")
            s.setdefault("messages", []).append({"type": "error", "field": qc_field, "text": msg})

    if any(v == 0 for v in error_values):
        s.addToPrintList('qc_summary', 0)
        return 0

    warning_values = [int(s.get(item, 0)) for item in warning_items]
    for idx, v in enumerate(warning_values):
        if v == 1:
            qc_field = warning_items[idx]
            msg = QC_WARNING_MESSAGES.get(qc_field, f"{qc_field} 预警，请复核结果。")
            s.setdefault("messages", []).append({"type": "warning", "field": qc_field, "text": msg})

    if any(v == 1 for v in warning_values):
        s.addToPrintList('qc_summary', 1)
        return 1

    # 全部通过时提示
    s.setdefault("messages", []).append({
        "type": "pass",
        "field": "qc_summary",
        "text": QC_PASS_MESSAGE
    })

    s.addToPrintList('qc_summary', 2)
    return 2
