a = """#dataset:filename	comments	image_bounding_box	base_mag	type	levels	height	width	mpp_x	mpp_y	comment	pen_markings	coverslip_edge	nonwhite	dark	flat_areas	fatlike_tissue_removed_num_regions	fatlike_tissue_removed_mean_area	fatlike_tissue_removed_max_area	fatlike_tissue_removed_percent	small_tissue_filled_num_regions	small_tissue_filled_mean_area	small_tissue_filled_max_area	small_tissue_filled_percent	small_tissue_removed_num_regions	small_tissue_removed_mean_area	small_tissue_removed_max_area	small_tissue_removed_percent	blurry_removed_num_regions	blurry_removed_mean_area	blurry_removed_max_area	blurry_removed_percent	spur_pixels	areaThresh	template1_MSE_hist	template2_MSE_hist	template3_MSE_hist	template4_MSE_hist	tenenGrad_contrast	michelson_contrast	rms_contrast	grayscale_brightness	grayscale_brightness_std	chan1_brightness	chan1_brightness_std	chan2_brightness	chan2_brightness_std	chan3_brightness	chan3_brightness_std	chan1_brightness_YUV	chan1_brightness_std_YUV	chan2_brightness_YUV	chan2_brightness_std_YUV	chan3_brightness_YUV	chan3_brightness_std_YUV	deconv_c0_mean	deconv_c0_std	deconv_c1_mean	deconv_c1_std	deconv_c2_mean	deconv_c2_std	pixels_to_use	warnings"""
b = """#dataset:filename	comments	image_bounding_box	base_mag	type	levels	height	width	mpp_x	mpp_y	comment	brightestPixels	small_tissue_filled_num_regions	small_tissue_filled_mean_area	small_tissue_filled_max_area	small_tissue_filled_percent	small_tissue_removed_num_regions	small_tissue_removed_mean_area	small_tissue_removed_max_area	small_tissue_removed_percent	background_contrast	background_contrast_std	background_dissimilarity	background_dissimilarity_std	background_homogeneity	background_homogeneity_std	background_ASM	background_ASM_std	background_energy	background_energy_std	background_correlation	background_correlation_std	background_tenenGrad_contrast	background_michelson_contrast	background_rms_contrast	background_grayscale_brightness	background_grayscale_brightness_std	background_chan1_brightness	background_chan1_brightness_std	background_chan2_brightness	background_chan2_brightness_std	background_chan3_brightness	background_chan3_brightness_std	tenenGrad_contrast	michelson_contrast	rms_contrast	grayscale_brightness	grayscale_brightness_std	chan1_brightness	chan1_brightness_std	chan2_brightness	chan2_brightness_std	chan3_brightness	chan3_brightness_std	chan1_brightness_YUV	chan1_brightness_std_YUV	chan2_brightness_YUV	chan2_brightness_std_YUV	chan3_brightness_YUV	chan3_brightness_std_YUV	pen_markings	coverslip_edge	final_contrast	final_contrast_std	final_dissimilarity	final_dissimilarity_std	final_homogeneity	final_homogeneity_std	final_ASM	final_ASM_std	final_energy	final_energy_std	final_correlation	final_correlation_std	deconv_c0_mean	deconv_c0_std	deconv_c1_mean	deconv_c1_std	deconv_c2_mean	deconv_c2_std	pixels_to_use	warnings"""
c = [
    "levels", 
    "height", 
    "width", 
    "mpp_x", 
    "mpp_y", 
    "Magnification", 
    "pen_markings", 
    "coverslip_edge", 
    "bubble", 
    "nonwhite", 
    "dark", 
    "percent_small_tissue_removed", 
    "percent_small_tissue_filled", 
    "percent_blurry", 
    "spur_pixels", 
    "template1_MSE_hist", 
    "template2_MSE_hist", 
    "template3_MSE_hist", 
    "template4_MSE_hist", 
    "michelson_contrast", 
    "rms_contrast", 
    "grayscale_brightness", 
    "chan1_brightness", 
    "chan2_brightness", 
    "chan3_brightness", 
    "deconv_c0_mean", 
    "deconv_c1_mean", 
    "deconv_c2_mean", 
    "chuv1_brightness_YUV",
    "chuv2_brightness_YUV",
    "chuv3_brightness_YUV",
    "chan1_brightness_YUV",
    "chan2_brightness_YUV",
    "chan3_brightness_YUV",
    "pixels_to_use"
]

# 将字符串按制表符分割成列表
a_fields = a.strip().split('\t')
b_fields = b.strip().split('\t')

# 找出a中有但b中没有的字段
a_only = set(a_fields) - set(b_fields)
print("a中有但b中没有的字段:")
for field in sorted(a_only):
    print(f"- {field}")

print("\n" + "="*50 + "\n")

# 找出b中有但a中没有的字段
b_only = set(b_fields) - set(a_fields)
print("b中有但a中没有的字段:")
for field in sorted(b_only):
    print(f"- {field}")

# 比较c和a
c_a_only = set(c) - set(a_fields)
print("c中有但a中没有的字段:")
for field in sorted(c_a_only):
    print(f"- {field}")

print("\n" + "="*50 + "\n")

# 比较c和b
c_b_only = set(c) - set(b_fields)
print("c中有但b中没有的字段:")
for field in sorted(c_b_only):
    print(f"- {field}")

# 运行结果：
"""
========== clinical_config中有的，ihc没有 ==========
- areaThresh
- blurry_removed_max_area
- blurry_removed_mean_area
- blurry_removed_num_regions
- blurry_removed_percent
- dark
- fatlike_tissue_removed_max_area
- fatlike_tissue_removed_mean_area
- fatlike_tissue_removed_num_regions
- fatlike_tissue_removed_percent
- flat_areas
- nonwhite
- spur_pixels
- template1_MSE_hist
- template2_MSE_hist
- template3_MSE_hist
- template4_MSE_hist

========== ihc有的，clinical_config没有 ==========
- background_ASM
- background_ASM_std
- background_chan1_brightness
- background_chan1_brightness_std
- background_chan2_brightness
- background_chan2_brightness_std
- background_chan3_brightness
- background_chan3_brightness_std
- background_contrast
- background_contrast_std
- background_correlation
- background_correlation_std
- background_dissimilarity
- background_dissimilarity_std
- background_energy
- background_energy_std
- background_grayscale_brightness
- background_grayscale_brightness_std
- background_homogeneity
- background_homogeneity_std
- background_michelson_contrast
- background_rms_contrast
- background_tenenGrad_contrast
- brightestPixels
- final_ASM
- final_ASM_std
- final_contrast
- final_contrast_std
- final_correlation
- final_correlation_std
- final_dissimilarity
- final_dissimilarity_std
- final_energy
- final_energy_std
- final_homogeneity
- final_homogeneity_std

========== 前端有的，clinical_config没有 ==========
- Magnification
- bubble
- chuv1_brightness_YUV
- chuv2_brightness_YUV
- chuv3_brightness_YUV
- percent_blurry
- percent_small_tissue_filled
- percent_small_tissue_removed

========== 前端有的，ihc没有 ==========
- Magnification
- bubble
- chuv1_brightness_YUV
- chuv2_brightness_YUV
- chuv3_brightness_YUV
- percent_blurry
- percent_small_tissue_filled
- percent_small_tissue_removed

========== 前端有的，clinical_config没有 ==========
- Magnification
- bubble
- chuv1_brightness_YUV
- chuv2_brightness_YUV
- chuv3_brightness_YUV
- dark
- nonwhite
- percent_blurry
- percent_small_tissue_filled
- percent_small_tissue_removed
- spur_pixels
- template1_MSE_hist
- template2_MSE_hist
- template3_MSE_hist
- template4_MSE_hist
"""