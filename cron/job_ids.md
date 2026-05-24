# Cronjob ID 参考

本文件记录已部署的 cronjob ID，便于管理和查询。

## 活动中的 Jobs

| 名称 | Job ID | 类型 | 频率 | Deliver |
|------|--------|------|------|---------|
| ks-content-generator | 4427cdd2d495 | LLM-driven | 0 6 * * * | local |
| ks-daily-report | b24455c0c11a | LLM-driven | 0 9 * * * | origin |
| ks-exception-monitor | 47cfd92aacbb | Script | */5 * * * * | origin |
| ks-credential-check | 72a1f72a08b4 | LLM-driven | 0 0 * * * | origin |

## 管理命令

```bash
# 查看所有 jobs
hermes cronjob list

# 查看单个 job 详情
hermes cronjob show 4427cdd2d495

# 暂停
hermes cronjob pause 4427cdd2d495

# 恢复
hermes cronjob resume 4427cdd2d495

# 删除（谨慎）
hermes cronjob remove 4427cdd2d495
```

## 创建时间
2026-05-11
