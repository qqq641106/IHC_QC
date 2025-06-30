"""
QC配置模块

该模块提供了QC（质量控制）配置的功能，用于管理和设置图像质量检查的阈值。

主要组件：
- QCThreshold: 数据类，用于存储单个QC阈值配置
- QCConfig: 配置管理类，用于管理所有QC阈值

QCThreshold属性：
    field_name (str): 字段名称
    threshold (float): 阈值数值
    operator (str): 比较运算符 ('>' 或 '<')
    description (str): 阈值描述

QCConfig方法：
    __init__(): 初始化配置，设置默认阈值
    add_threshold(): 添加新的QC阈值
    get_thresholds(): 获取所有阈值配置
    update_threshold(): 更新特定字段的阈值

默认阈值配置：
    - pen_markings: 笔迹标记检测 (>0.05)
    - blur: 模糊检测 (>0.1)
    - brightness: 亮度检测 (<0.8)

使用示例：
    config = QCConfig()
    config.add_threshold("tissue_ratio", 0.3, ">", "组织比例检测")
    config.update_threshold("pen_markings", 0.03)
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class QCThreshold:
    field_name: str
    threshold: float
    operator: str  # '>' or '<'
    description: str

class QCConfig:
    def __init__(self):
        self.thresholds = []
        self._initialize_default_thresholds()
    
    def _initialize_default_thresholds(self):
        # 默认阈值配置
        self.add_threshold("pen_markings", 0.05, ">", "笔迹标记检测")
        self.add_threshold("blur", 0.1, ">", "模糊检测")
        self.add_threshold("brightness", 0.8, "<", "亮度检测")
    
    def add_threshold(self, field_name: str, threshold: float, operator: str, description: str):
        """添加新的QC阈值"""
        self.thresholds.append(QCThreshold(field_name, threshold, operator, description))
    
    def get_thresholds(self) -> list:
        """获取所有阈值配置"""
        return self.thresholds
    
    def update_threshold(self, field_name: str, new_threshold: float):
        """更新特定字段的阈值"""
        for threshold in self.thresholds:
            if threshold.field_name == field_name:
                threshold.threshold = new_threshold
                break 