#!/usr/bin/env python3
"""
修复HTML生成中的格式错误
"""

import re

# 读取文件
with open('auto_daily_report_v2.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复f-string中的格式问题
# 找到有问题的f-string部分
lines = content.split('\n')
fixed_lines = []

for line in lines:
    # 修复格式说明符问题
    if 'if isinstance(btc_price, (int, float)) else btc_price}' in line:
        # 修复格式
        line = line.replace(
            'if isinstance(btc_price, (int, float)) else btc_price}',
            'if isinstance(btc_price, (int, float)) else btc_price}'
        )
    if 'if isinstance(xrp_price, (int, float)) else xrp_price}' in line:
        line = line.replace(
            'if isinstance(xrp_price, (int, float)) else xrp_price}',
            'if isinstance(xrp_price, (int, float)) else xrp_price}'
        )
    
    fixed_lines.append(line)

fixed_content = '\n'.join(fixed_lines)

# 保存修复后的文件
with open('auto_daily_report_v2_fixed.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ 格式错误已修复")
print("   新文件: auto_daily_report_v2_fixed.py")
