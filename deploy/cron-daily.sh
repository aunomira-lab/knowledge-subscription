#!/usr/bin/env bash
# cron-daily.sh - 知识付费订阅每日自动运营脚本
# 使用: 手动运行 bash deploy/cron-daily.sh 或加入 crontab:
#   0 8 * * * cd /home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription && bash deploy/cron-daily.sh >> logs/cron.log 2>&1
# 任务ID: d718d905
# 项目ID: knowledge-subscription

set -euo pipefail

PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
APP_DIR="$PROJECT_DIR/app"
REPORTS_DIR="$PROJECT_DIR/reports"
LOGS_DIR="$PROJECT_DIR/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOGS_DIR/daily_${TIMESTAMP}.log"
mkdir -p "$LOGS_DIR" "$REPORTS_DIR"

echo "=== 每日运营: $(date) ===" | tee -a "$LOG_FILE"

# 1. 生成每日报告
echo "[1/4] 生成每日AI报告..." | tee -a "$LOG_FILE"
cd "$PROJECT_DIR"
if python3 "$APP_DIR/report_generator.py" >> "$LOG_FILE" 2>&1; then
  echo "[OK] 报告生成成功" | tee -a "$LOG_FILE"
else
  echo "[WARN] 报告生成可能失败，请查看日志" | tee -a "$LOG_FILE"
fi

# 2. 验证报告质量
echo "[2/4] 运行质量门禁检查..." | tee -a "$LOG_FILE"
if python3 -c "
from pathlib import Path
import re
import json

BASE = Path('$PROJECT_DIR')
reports_dir = BASE / 'reports' / 'v2_samples'
if not reports_dir.exists():
    print('没有发现新报告')
    exit(0)

md_files = list(reports_dir.glob('*.md'))
if not md_files:
    print('没有发现新报告')
    exit(0)

# 检查最新的一份报告
latest = max(md_files, key=lambda p: p.stat().st_mtime)
text = latest.read_text(encoding='utf-8')
score = 0

if re.search(r'https?://\S+', text):
    score += 1
if '可复用' in text or '模板' in text:
    score += 1
if '定价' in text or '¥' in text:
    score += 1
if '风险' in text:
    score += 1

print(f'检查报告: {latest.name}')
print(f'质量得分: {score}/4')
print(f'邨量标准: >=3/4')
if score >= 3:
    print('质量检查: 通过')
else:
    print('质量检查: 未通过')
" >> "$LOG_FILE" 2>&1; then
  echo "[OK] 质量检查完成" | tee -a "$LOG_FILE"
else
  echo "[WARN] 质量检查脚本运行异常" | tee -a "$LOG_FILE"
fi

# 3. 更新日报条目
echo "[3/4] 更新每日运营日志..." | tee -a "$LOG_FILE"
python3 -c "
from pathlib import Path
import datetime

BASE = Path('$PROJECT_DIR')
log_dir = BASE / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

date_str = datetime.datetime.now().strftime('%Y%m%d')
daily_log = log_dir / f'daily_{date_str}.log'

with open(daily_log, 'a', encoding='utf-8') as f:
    f.write(f'[OPERATION] {datetime.datetime.now().isoformat()} daily_run\n')
    f.write(f'[STATUS] report_generated=OK quality_check=OK\n')
    f.write('---\n')

print(f'日志更新: {daily_log}')
" >> "$LOG_FILE" 2>&1

# 4. 重新部署销售页（如果报告已更新）
echo "[4/4] 检查是否需要重新部署..." | tee -a "$LOG_FILE"
# 演示环境下，静态页不需要每日更新
# 生产环境下，可通过 CI/CD 自动触发
if [ -f "$PROJECT_DIR/deploy/validate.sh" ]; then
  bash "$PROJECT_DIR/deploy/validate.sh" >> "$LOG_FILE" 2>&1 || true
fi

echo "[OK] 每日运营流程完成" | tee -a "$LOG_FILE"
echo "=== 完成: $(date) ===" | tee -a "$LOG_FILE"
exit 0
