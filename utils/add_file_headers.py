#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
该文件为项目中所有python文件添加文件头
"""

import os

def add_header_to_file(file_path):
    header = '#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n\n'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查文件是否已经包含这些头部信息
    lines = content.split('\n')
    existing_headers = []
    
    for line in lines[:2]:
        if any(h in line for h in ['#!/usr/bin/env python', '# -*- coding']):
            existing_headers.append(line)
    
    # 如果没有完整的头部信息，则添加缺失的部分
    if len(existing_headers) < 2:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header + content)
        print(f"Added headers to {file_path}")
    else:
        print(f"Headers already exist in {file_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                add_header_to_file(file_path)

# 使用示例
if __name__ == '__main__':
    # 获取当前文件所在目录的上级目录作为项目根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    process_directory(project_root) 