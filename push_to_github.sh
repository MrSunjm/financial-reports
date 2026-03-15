#!/bin/bash
# 推送报告到GitHub

cd "$(dirname "$0")"

echo "📤 推送报告到GitHub..."
git add .
git commit -m "每日报告更新: $(date '+%Y-%m-%d %H:%M')"
git push origin main

echo "✅ 推送完成"
echo "🌐 访问: https://linghucong001.github.io/financial-reports/"
