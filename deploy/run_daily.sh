#!/bin/bash
# run_daily.sh — AI Opportunity Radar 每日运营脚本
# 用途: 每日自动生成报告、检查网站健康、更新运营数据
# 建议配合 crontab 每日 08:00 执行
# 任务ID: d1eb27ce
# 更新日期: 2026-05-31

set -euo pipefail

PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
LOG_DIR="$PROJECT_DIR/logs"
REPORTS_DIR="$PROJECT_DIR/reports"
METRICS_DIR="$PROJECT_DIR/metrics"
SITE_DIR="$PROJECT_DIR/site"
APP_DIR="$PROJECT_DIR/app"

# 确保目录存在
mkdir -p "$LOG_DIR" "$REPORTS_DIR/daily" "$METRICS_DIR"

LOG_FILE="$LOG_DIR/daily_$(date +%Y%m%d).log"
DAILY_REPORT="$REPORTS_DIR/daily/briefing_$(date +%Y%m%d).md"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ===== 每日运营开始 =====" | tee -a "$LOG_FILE"

# -------------------------------------------------
# 1. 内容生成（如果有新数据源更新）
# -------------------------------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 1/6: 检查内容生成器..." | tee -a "$LOG_FILE"

if [ -f "$APP_DIR/sample_pack_generator_a6837f49.py" ]; then
    cd "$PROJECT_DIR"
    python3 "$APP_DIR/sample_pack_generator_a6837f49.py" >> "$LOG_FILE" 2>&1 || echo "[警告] 内容生成器返回非零退出码，跳过" | tee -a "$LOG_FILE"
else
    echo "[警告] 未找到内容生成器，跳过自动生成" | tee -a "$LOG_FILE"
fi

# -------------------------------------------------
# 2. 检查销售页可访问性
# -------------------------------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 2/6: 检查销售页健康..." | tee -a "$LOG_FILE"

SITE_URL="https://aunomira-lab.github.io/knowledge-subscription/"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ]; then
    echo "[通过] 销售页可访问 (HTTP 200)" | tee -a "$LOG_FILE"
else
    echo "[异常] 销售页返回 HTTP $HTTP_CODE，需要检查" | tee -a "$LOG_FILE"
    # 发送告警（如果有邮件/Slack钩子，可在此扩展）
fi

# 检查关键内容是否存在
if curl -s "$SITE_URL" | grep -q "AI Opportunity Radar"; then
    echo "[通过] 关键内容检查通过" | tee -a "$LOG_FILE"
else
    echo "[异常] 销售页缺少关键内容" | tee -a "$LOG_FILE"
fi

# -------------------------------------------------
# 3. 生成简报标题跟踪
# -------------------------------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 3/6: 生成简报标题跟踪..." | tee -a "$LOG_FILE"

TODAY=$(date +%Y-%m-%d)
WEEKDAY=$(date +%u)

# 生成简单的日报标题模板（供运营者填充）
cat > "$DAILY_REPORT" <<EOF
# AI赚钱机会简报 | $TODAY

## 本期精选 ($TODAY)

> 自动生成时间: $(date '+%Y-%m-%d %H:%M:%S')
> 编辑状态: 待人工审核
> 发布渠道: 公众号 / 知识星球 / 微信群

### 机会 1: [标题占位]
- 数据支撑: [填充]
- 执行 SOP: [填充]
- 收益测算: [填充]
- Prompt 模板: [填充]
- 风险提示: [填充]

### 机会 2: [标题占位]
...

### 机会 3: [标题占位]
...

---

## 运营动作
- [ ] 人工审核内容
- [ ] 填充具体机会数据
- [ ] 生成图文素材
- [ ] 发布至公众号/知识星球/微信群
- [ ] 记录数据至 metrics/daily_metrics.csv

EOF

echo "[完成] 日报模板已生成: $DAILY_REPORT" | tee -a "$LOG_FILE"

# -------------------------------------------------
# 4. 更新每日数据记录（如果未存在则创建表头）
# -------------------------------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 4/6: 更新运营数据..." | tee -a "$LOG_FILE"

DAILY_CSV="$METRICS_DIR/daily_metrics.csv"
if [ ! -f "$DAILY_CSV" ]; then
    echo "日期,平台,内容数,UV,表单提交,订阅意向,付费转化,收入,备注" > "$DAILY_CSV"
fi

# 记录今日基础数据（需要运营者每日手动更新或接入分析工具API）
echo "$TODAY,全平台,-,-,-,-,-,-,自动检测运行" >> "$DAILY_CSV"

echo "[完成] 运营数据已记录: $DAILY_CSV" | tee -a "$LOG_FILE"

# -------------------------------------------------
# 5. 备份关键文件
# -------------------------------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 5/6: 备份关键文件..." | tee -a "$LOG_FILE"

BACKUP_DIR="$PROJECT_DIR/backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"
cp "$SITE_DIR/index.html" "$BACKUP_DIR/" 2>/dev/null || true
cp -r "$REPORTS_DIR/sample_pack" "$BACKUP_DIR/" 2>/dev/null || true

echo "[完成] 关键文件已备份至: $BACKUP_DIR" | tee -a "$LOG_FILE"

# -------------------------------------------------
# 6. Git 提交日常更新（如有变更）
# -------------------------------------------------
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Step 6/6: 检查Git状态..." | tee -a "$LOG_FILE"

cd "$PROJECT_DIR"
if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
    echo "[完成] 无文件变更，跳过Git提交" | tee -a "$LOG_FILE"
else
    git add -A
    git commit -m "daily: auto-run $(date +%Y-%m-%d) [task d1eb27ce]" >> "$LOG_FILE" 2>&1 || true
    # 不自动 push，避免干扰，运营者可手动 push
    echo "[完成] 本地提交已创建，请手动 push 触发部署" | tee -a "$LOG_FILE"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ===== 每日运营完成 =====" | tee -a "$LOG_FILE"
echo "日志位置: $LOG_FILE"
echo "今日简报: $DAILY_REPORT"
echo "运营数据: $DAILY_CSV"
