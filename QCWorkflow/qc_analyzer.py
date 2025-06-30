"""
QC分析器模块

该模块提供了QC（质量控制）分析的功能，用于检查图像质量是否符合预设标准。

主要组件：
- QCAnalyzer: 分析器类，用于执行图像质量检查

QCAnalyzer方法：
    __init__(): 初始化分析器，加载配置
    analyze_single_image(): 分析单张图片的质量
    _check_threshold(): 检查单个阈值条件

分析流程：
    1. 读取图片的QC数据
    2. 根据配置的阈值进行检查
    3. 生成检查结果报告

使用示例：
    config = QCConfig()
    analyzer = QCAnalyzer(config)
    results = analyzer.analyze_single_image("image1_results.tsv")
"""

import pandas as pd
from typing import Dict, List, Tuple
from .qc_config import QCConfig, QCThreshold

class QCAnalyzer:
    def __init__(self, config: QCConfig):
        self.config = config
    
    def analyze_single_image(self, results_file: str) -> List[Tuple[str, bool, str]]:
        """
        分析单张图片的QC结果
        
        Args:
            results_file: HistoQC输出的results.tsv文件路径
            
        Returns:
            List of tuples containing (field_name, passed, message)
        """
        try:
            # 读取TSV文件
            df = pd.read_csv(results_file, sep='\t')
            if len(df) != 1:
                raise ValueError("输入文件应该只包含一张图片的数据")
            
            results = []
            for threshold in self.config.get_thresholds():
                field_name = threshold.field_name
                if field_name not in df.columns:
                    results.append((field_name, False, f"字段 {field_name} 不存在"))
                    continue
                
                value = df[field_name].iloc[0]
                passed = self._check_threshold(value, threshold)
                message = self._generate_message(field_name, value, threshold, passed)
                results.append((field_name, passed, message))
            
            return results
            
        except Exception as e:
            raise Exception(f"分析过程中出现错误: {str(e)}")
    
    def _check_threshold(self, value: float, threshold: QCThreshold) -> bool:
        """检查值是否满足阈值条件"""
        if threshold.operator == ">":
            return value <= threshold.threshold
        elif threshold.operator == "<":
            return value >= threshold.threshold
        return True
    
    def _generate_message(self, field_name: str, value: float, 
                         threshold: QCThreshold, passed: bool) -> str:
        """生成QC结果消息"""
        status = "通过" if passed else "失败"
        return f"{threshold.description}: {value:.3f} {threshold.operator} {threshold.threshold:.3f} - {status}"