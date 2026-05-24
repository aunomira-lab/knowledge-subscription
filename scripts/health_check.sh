#!/bin/bash
#
# knowledge-subscription 健康检查脚本
# 被 ks-exception-monitor cronjob 调用
# 返回空表示没有问题，非空表示需要报告的异常

PROJECT_DIR="/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription"
ERRORS=""

# 1. 检查关键目录可写
if [ ! -w "$PROJECT_DIR/reports" ]; then
    ERRORS="${ERRORS}❌ reports 目录不可写\n"
fi

if [ ! -w "$PROJECT_DIR/logs" ]; then
    ERRORS="${ERRORS}❌ logs 目录不可写\n"
fi

if [ ! -w "$PROJECT_DIR/metrics" ]; then
    ERRORS="${ERRORS}❌ metrics 目录不可写\n"
fi

# 2. 检查内容生成器运行状态（通过日志时间截）
LAST_CONTENT_GEN=$(find "$PROJECT_DIR/logs" -name "content_gen_*.log" -type f -mtime -1 2>/dev/null | head -1)
if [ -z "$LAST_CONTENT_GEN" ]; then
    ERRORS="${ERRORS}⚠️ 近24小时内无内容生成记录\n"
fi

# 3. 检查发布队列是否堵塞
QUEUE_FILE="$PROJECT_DIR/reports/queue/pending.json"
if [ -f "$QUEUE_FILE" ]; then
    QUEUE_COUNT=$(grep -c '"status": "pending"' "$QUEUE_FILE" 2>/dev/null || echo "0")
    if [ "$QUEUE_COUNT" -gt "5" ]; then
        ERRORS="${ERRORS}⚠️ 发布队列有 $QUEUE_COUNT 个待处理项目（超过5个）\n"
    fi
fi

# 4. 检查数据文件是否存在且最新
METRICS_FILE="$PROJECT_DIR/metrics/experiment_tracker.csv"
if [ ! -f "$METRICS_FILE" ]; then
    ERRORS="${ERRORS}❌ 指标数据文件不存在\n"
else
    LAST_UPDATE=$(stat -c %Y "$METRICS_FILE" 2>/dev/null)
    NOW=$(date +%s)
    AGE=$((NOW - LAST_UPDATE))
    if [ $AGE -gt 172800 ]; then
        ERRORS="${ERRORS}⚠️ 指标数据2天未更新\n"
    fi
fi

# 5. 检查磁盘空间
DISK_USAGE=$(df "$PROJECT_DIR" | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt "90" ]; then
    ERRORS="${ERRORS}🚨 磁盘使用率超过 90% ($DISK_USAGE%)\n"
fi

# 输出结果
if [ -z "$ERRORS" ]; then
    # 没有问题，返回空（静默）
    exit 0
else
    # 有问题，输出错误信息（会触发通知）
    echo -e "🚨 knowledge-subscription 异常检测:\n$ERRORS"
    exit 0
fi
