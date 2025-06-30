"""
QC报告生成模块

该模块提供了生成QC（质量控制）报告的功能，用于记录和展示图像质量检查的结果。

主要组件：
- QCReporter: 报告生成类，用于创建和管理QC报告

QCReporter方法：
    __init__(): 初始化报告生成器，设置输出目录
    generate_report(): 生成QC分析报告

报告内容：
    - 图片名称
    - 生成时间
    - 总体通过率
    - 详细检查结果

使用示例：
    reporter = QCReporter()
    report_file = reporter.generate_report("image1", qc_results)
"""


from typing import List, Tuple
import os
from datetime import datetime

class QCReporter:
    def __init__(self, output_dir: str = "qc_reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_report(self, image_name: str, qc_results: List[Tuple[str, bool, str]]) -> str:
        """
        生成QC报告
        
        Args:
            image_name: 图片名称
            qc_results: QC分析结果列表
            
        Returns:
            报告文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.output_dir, f"qc_report_{image_name}_{timestamp}.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"QC分析报告 - {image_name}\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 50 + "\n\n")
            
            # 写入总体结果
            total_checks = len(qc_results)
            passed_checks = sum(1 for _, passed, _ in qc_results if passed)
            f.write(f"总体结果: {passed_checks}/{total_checks} 项通过\n\n")
            
            # 写入详细结果
            f.write("详细结果:\n")
            for field_name, passed, message in qc_results:
                status = "✓" if passed else "✗"
                f.write(f"{status} {message}\n")
        
        return report_file 