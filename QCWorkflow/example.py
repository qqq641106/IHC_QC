from qc_config import QCConfig
from qc_analyzer import QCAnalyzer
from qc_reporter import QCReporter
import os

def main():
    # 创建配置
    config = QCConfig()
    
    # 添加自定义阈值（可选）
    config.add_threshold("tissue_ratio", 0.3, ">", "组织比例检测")
    
    # 更新现有阈值（可选）
    config.update_threshold("pen_markings", 0.03)
    
    # 创建分析器和报告生成器
    analyzer = QCAnalyzer(config)
    reporter = QCReporter()
    
    # 分析单张图片
    results_file = r"F:\3-workSpace2\3-lxm-GPU-new\9-HistoQC\output\mohu_pmk_1000\results.tsv"  # 替换为实际的results.tsv文件路径
    image_name = os.path.basename(results_file).replace("_results.tsv", "")
    
    try:
        # 执行QC分析
        qc_results = analyzer.analyze_single_image(results_file)
        
        # 生成报告
        report_file = reporter.generate_report(image_name, qc_results)
        print(f"QC报告已生成: {report_file}")
        
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main() 