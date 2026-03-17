#!/bin/bash
# 设置每日定时任务

echo "🔧 配置每日定时任务..."
echo "========================"

# 获取脚本绝对路径
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/auto_complete_analysis.py"

echo "脚本路径: $SCRIPT_PATH"

# 检查Python路径
PYTHON_PATH=$(which python3)
echo "Python路径: $PYTHON_PATH"

# 创建cron任务（每日08:00北京时间 = 00:00 UTC）
CRON_JOB="0 0 * * * cd $SCRIPT_DIR && $PYTHON_PATH $SCRIPT_PATH >> $SCRIPT_DIR/cron.log 2>&1"

echo ""
echo "定时任务配置:"
echo "$CRON_JOB"
echo ""
echo "执行时间: 每日00:00 UTC = 08:00 北京时间"
echo "日志文件: $SCRIPT_DIR/cron.log"

# 添加到crontab
echo ""
echo "添加到crontab..."
(crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH"; echo "$CRON_JOB") | crontab -

# 验证
echo ""
echo "验证定时任务..."
crontab -l | grep -i "auto_complete_analysis"

echo ""
echo "✅ 定时任务配置完成！"
echo "   下次执行: 明日08:00 (北京时间)"
echo "   日志文件: cron.log"
echo ""
echo "📋 手动测试命令:"
echo "   cd $SCRIPT_DIR && $PYTHON_PATH $SCRIPT_PATH"
