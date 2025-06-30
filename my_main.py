run = \
    """
    启动命令：
    nohup python -m histoqc ./data/*.svs --outdir ./output/ --config ./histoqc/config/my_qc_ihc.ini --force --nprocesses 16 &
    多个输入路劲：
    nohup python -m histoqc ./data1/*.svs ./data2/*.svs --outdir ./output/ --config ./histoqc/config/my_qc_ihc.ini --force --nprocesses 16 &
    """

weib = \
    """
    UI web可视化结果:
    python -m histoqc.ui /AmoyDx/USER/lixiaoming/workSpace/9-HistoQC/output/1-IHC_LJ_v2.1/results.tsv
    """

ui = """
1-IHC_LJ:
python -m histoqc.ui /AmoyDx/USER/lixiaoming/workSpace/9-HistoQC/output/1-IHC_LJ/results.tsv

SDZL_batch2_kfb2svs:
python -m histoqc.ui /AmoyDx/USER/lixiaoming/workSpace/9-HistoQC/output/SDZL_batch2_kfb2svs/results.tsv

SDZL_batch2_ndpi:
python -m histoqc.ui /AmoyDx/USER/lixiaoming/workSpace/9-HistoQC/output/SDZL_batch2_ndpi/results.tsv

val_SDZL_ndpi_20x:
python -m histoqc.ui /AmoyDx/USER/lixiaoming/workSpace/9-HistoQC/output/val_SDZL_ndpi_20x/results.tsv

val_SDZL_ndpi_40x:
python -m histoqc.ui /AmoyDx/USER/lixiaoming/workSpace/9-HistoQC/output/val_SDZL_ndpi_40x/results.tsv
"""

print("启动命令:")
print(f"{run}{weib}")
print(f"UI web可视化结果: {ui}")
