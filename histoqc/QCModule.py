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


def parse_item_list(item_str):
    """
    解析 error_items/warning_items 配置项为 [(字段, 提示), ...]
    支持多行、逗号分隔、分号分隔
    """
    result = []
    if not item_str:
        return result
    for line in item_str.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # 按分号或逗号拆分
        parts = [p.strip() for p in line.replace(';', '\n').replace(',', '\n').split('\n')]
        for part in parts:
            if not part:
                continue
            # 按第一个冒号分割
            if ':' in part:
                field, msg = part.split(':', 1)
                result.append((field.strip(), msg.strip()))
            else:
                result.append((part.strip(), ''))
    return result


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
    qc结果汇总，字段和提示信息全部由配置文件传递
    """
    # 读取配置
    error_items = parse_item_list(params.get('error_items', ''))
    warning_items = parse_item_list(params.get('warning_items', ''))
    pass_message = params.get('pass_message', 'QC pass')

    # 字段名列表
    error_fields = [k for k, _ in error_items]
    warning_fields = [k for k, _ in warning_items]
    error_msgs = dict(error_items)
    warning_msgs = dict(warning_items)

    # 判断 error
    error_values = [int(s.get(item, 0)) for item in error_fields]
    for idx, v in enumerate(error_values):
        if v == 0:
            qc_field = error_fields[idx]
            msg = error_msgs.get(qc_field, f"{qc_field} 未通过QC，请检查。")
            s.setdefault("messages", []).append({"type": "error", "field": qc_field, "text": msg})
    if any(v == 0 for v in error_values):
        s.addToPrintList('qc_summary', 0)
        return 0

    # 判断 warning
    warning_values = [int(s.get(item, 0)) for item in warning_fields]
    for idx, v in enumerate(warning_values):
        if v == 1:
            qc_field = warning_fields[idx]
            msg = warning_msgs.get(qc_field, f"{qc_field} 预警，请复核结果。")
            s.setdefault("messages", []).append({"type": "warning", "field": qc_field, "text": msg})
    if any(v == 1 for v in warning_values):
        s.addToPrintList('qc_summary', 1)
        return 1

    # 全部通过时提示
    s.setdefault("messages", []).append({
        "type": "pass",
        "field": "qc_summary",
        "text": pass_message
    })
    s.addToPrintList('qc_summary', 2)
    return 2
