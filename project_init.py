"""
项目初始化 - 极简版本
"""

import sys
import os

# 自动设置当前目录为根目录
sys.path.insert(0, os.path.dirname(__file__))

print("Project Genesis 初始化完成")
print(f"工作目录: {os.path.dirname(__file__)}")
