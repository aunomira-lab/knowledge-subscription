# 账号与支付阻塞点检查清单

**更新时间**: 2026-05-11  
**项目**: knowledge-subscription  
**目的**: 明确列出 Substack/Stripe 账号创建、支付设置、提现的所有前置条件和潜在阻塞点

---

## 1. 执行前必须填写

### 1.1 账号基本信息
```yaml
# 由用户填写
account_info:
  creator_name: "_______"  # 创作者真实姓名
  contact_email: "_______"  # 联系邮箱（必须可收验证邮件）
  location_country: "_______"  # 创作者所在国家
  location_city: "_______"  # 城市
  
publication_info:
  name: "_______"  # 建议: AI Money Brief / AI变现情报
  subdomain: "_______"  # 如: aimoneybrief
  full_url: "_______"  # 如: https://aimoneybrief.substack.com
  description: "_______"  # 50-100字描述
  category: "Technology"  # 分类
```

### 1.2 账号验证检查表
- [ ] 已拥有可用邮箱 (建议 Gmail/Outlook，避免 QQ/163 邮箱进收件箱)
- [ ] 已确认 Substack 账号可注册 (无 IP 地域限制)
- [ ] 已确认可访问 Substack.com (无防火墙阻挡)

---

## 2. Stripe 连接阻塞点 (关键)

### 2.1 国家/地区支持检查

#### 支持列表 (44个国家/地区)
```bash
# 验证命令: 获取最新支持列表
curl -s "https://stripe.com/global" | grep -oP 'country=[A-Z]{2}' | sed 's/country=//' | sort -u
```

**完整列表**:
| 代码 | 国家/地区 | 常见身份证 | 备注 |
|------|------------|------------|-------|
| AE | 阿联酋 | 护照 | 可行 |
| AT | 奥地利 | 护照/身份证 | 欧盟 |
| AU | 澳大利亚 | 护照/驾照 | 英联邦 |
| BE | 比利时 | 身份证 | 欧盟 |
| BG | 保加利亚 | 身份证 | 欧盟 |
| BR | 巴西 | 护照 | 南美 |
| CA | 加拿大 | 护照/驾照 | 北美 |
| CH | 瑞士 | 身份证 | 非欧盟 |
| CY | 塞浦路斯 | 身份证 | 欧盟 |
| CZ | 捷克 | 身份证 | 欧盟 |
| DE | 德国 | 身份证 | 欧盟 |
| DK | 丹麦 | 身份证 | 欧盟 |
| EE | 爱沙尼亚 | 身份证 | 欧盟 |
| ES | 西班牙 | 身份证 | 欧盟 |
| FI | 芬兰 | 身份证 | 欧盟 |
| FR | 法国 | 身份证 | 欧盟 |
| GB | 英国 | 护照/驾照 | 英联邦 |
| GI | 直布罗陀 | 护照 | 英联邦 |
| GR | 希腊 | 身份证 | 欧盟 |
| HK | 香港 | 护照/身份证 | 华人友好 |
| HR | 克罗地亚 | 身份证 | 欧盟 |
| HU | 匈牙利 | 身份证 | 欧盟 |
| IE | 爱尔兰 | 护照/身份证 | 英联邦 |
| IT | 意大利 | 身份证 | 欧盟 |
| JP | 日本 | 在留卡/身份证 | 东亚 |
| LI | 列支敦士登 | 护照 | 欧洲 |
| LT | 立陶宛 | 身份证 | 欧盟 |
| LU | 卢森堡 | 身份证 | 欧盟 |
| LV | 拉脱维亚 | 身份证 | 欧盟 |
| MT | 马耳他 | 身份证 | 欧盟 |
| MX | 墨西哥 | 护照 | 北美 |
| MY | 马来西亚 | 护照/身份证 | 华人友好 |
| NL | 荷兰 | 身份证 | 欧盟 |
| NO | 挪威 | 身份证 | 欧洲 |
| NZ | 新西兰 | 护照/驾照 | 英联邦 |
| PL | 波兰 | 身份证 | 欧盟 |
| PT | 葡萄牙 | 身份证 | 欧盟 |
| RO | 罗马尼亚 | 身份证 | 欧盟 |
| SE | 瑞典 | 身份证 | 欧盟 |
| SG | 新加坡 | 护照/身份证 | 华人友好 |
| SI | 斯洛文尼亚 | 身份证 | 欧盟 |
| SK | 斯洛伐克 | 身份证 | 欧盟 |
| TH | 泰国 | 护照 | 东南亚 |
| US | 美国 | 护照/驾照/SSN | 最常用 |

#### 中国大陆创作者的选择

> ⚠️ **重要**: 中国大陆 (CN) 不在 Stripe 直接支持列表

**解决方案**：

| 方案 | 需要资料 | 难度 | 成本 | 推荐度 |
|------|----------|------|------|----------|
| **A. 香港账户** | 香港身份证 + 香港银行卡 | 中 | 中 | ⭐⭐⭐⭐⭐ |
| **B. 新加坡账户** | 新加坡身份 + 新加坡银行卡 | 中 | 中 | ⭐⭐⭐⭐ |
| **C. 美国账户** | 美国银行卡 + ITIN/EIN | 高 | 高 | ⭐⭐⭐ |
| **D. 第三方服务** | Mercury/ Wise Business | 低 | 中 | ⭐⭐⭐⭐ |
| **E. 替代方案** | 小报童 + 微信收款 | 低 | 低 | ⭐⭐⭐ |

**建议选择**: 方案 A (香港) 或 D (Mercury)

### 2.2 KYC (了解你的客户) 要求

#### 身份验证 (必须提供)
- [ ] 政府签发的有效身份证件 (护照/身份证/驾照)
- [ ] 证件照片 (正反面或人像页)
- [ ] 证件有效期需要 > 6 个月
- [ ] 出生日期

**常见拒绝原因**:
- 证件模糊/无法识别
- 证件已过期
- 名字拼写与银行账户不一致
- 地址证明不足 (部分国家需要)

#### 银行账户要求
- [ ] 支持的国家/地区的银行账户
- [ ] 账户名字与身份证件一致
- [ ] 支持外币收款 (接收 USD 或当地货币)
- [ ] IBAN 或 Routing number 准确

**支持的银行类型**:
- 个人支票账户 (Checking account)
- 公司账户 (若有注册公司)
- Wise/Mercury 等虚拟银行 (若支持对应国家)

#### 税务信息
- [ ] **美国公民/绿卡**: 填写 W-9 表格
  - 需要: SSN 或 EIN
  - 用途: 报税和 1099 表
  
- [ ] **非美国居民**: 填写 W-8BEN 表格
  - 需覂: 外国税号 (TIN)
  - 用途: 证明非美国税务居民身份
  - 好处: 避免美国预扣税 (30% withholding)

---

## 3. 支付测试验证

### 3.1 测试支付流程
必须完成一次真实付费测试 (可取消):

```bash
# 测试步骤
1. 创建测试用户账号 (或请朋友帮忙)
2. 访问 publication 付费订阅页面
3. 选择 monthly 或 annual plan
4. 使用测试卡或真实信用卡完成支付
5. 验证 Substack 后台显示新订阅
6. 立即取消订阅 (避免费用)
```

### 3.2 Stripe 测试卡信息
```
卡号: 4242 4242 4242 4242
到期: 任意未来日期 (MM/YY 格式)
CVC: 任意 3 位数字
邮编: 任意 5 位数字
```

### 3.3 测试验证清单
- [ ] 付费页面可正常加载
- [ ] 可选择 monthly/annual plan
- [ ] Stripe checkout 页面正常显示
- [ ] 支付成功
- [ ] 收到订阅确认邮件
- [ ] Substack 后台显示新订阅者
- [ ] Stripe Dashboard 显示订单

---

## 4. 收入提现阻塞点

### 4.1 提现周期
- **Stripe 标准**: 2-7 个工作日
- **Substack 定期**: 通常每月提现
- **首次提现**: 可能需要更长 (7-14 天)

### 4.2 所需信息
- [ ] 银行账户可正常收款
- [ ] 提现地址信息准确
- [ ] 联系方式有效

### 4.3 费用明细 (已核实)
```
订阅金额: $9.00
- Substack 10% 平台费: -$0.90
- Stripe 处理费 (~2.9% + $0.30): ~$0.56
= 创作者实收: ~$7.54 (约 83.8%)
```

---

## 5. 常见阻塞点与解决方案

### 5.1 高频阻塞点

| 阻塞点 | 表现 | 解决方案 | 预估解决时间 |
|--------|------|----------|-------------|
| **国家不支持** | Stripe 拒绝注册 | 使用香港/新加坡/美国账户 | 1-2 周 |
| **KYC 失败** | 身份验证被拒 | 更换证件/联系 Stripe 客服 | 3-7 天 |
| **银行验证失败** | 无法添加银行卡 | 确认银行在支持列表/换卡 | 1-3 天 |
| **税务表格错误** | W-8BEN 信息不完整 | 重新提交正确信息 | 1-2 天 |
| **支付测试失败** | 测试卡付款被拒 | 检查卡信息/换卡测试 | 即时 |
| **邮箱验证失败** | 收不到验证邮件 | 更换邮箱/检查垃圾邮件 | 即时 |

### 5.2 升级流程

如果遇到阻塞点：
1. 记录具体错误信息
2. 检查 Stripe/Substack 帮助中心
3. 尝试解决方案
4. 若无法解决: `kanban_block` 并详细说明需要用户提供的字段

---

## 6. 用户必须提供的字段清单

以下字段缺一不可，若未提供必须 `kanban_block`:

```yaml
# 基本信息
required_fields:
  - creator_full_name: "___"  # 真实姓名
  - creator_email: "___"  # 有效邮箱
  - location_country: "___"  # 所在国家
  - location_city: "___"  # 所在城市
  
# Stripe 相关
stripe_fields:
  - stripe_account_country: "___"  # 开户国家 (必须在支持列表)
  - id_document_type: "___"  # 身份证类型
  - id_document_number: "___"  # 证件号码
  - bank_account_country: "___"  # 银行账户所在国
  - bank_name: "___"  # 银行名称
  - tax_form_type: "___"  # W-9 或 W-8BEN
  
# 公开信息
publication_fields:
  - publication_name: "___"  # 发布名称
  - publication_description: "___"  # 50-100字描述
  - intended_launch_date: "___"  # 计划上线日期
  - pricing_preference: "___"  # $5/$9 monthly 首选
```

---

## 7. 验证命令汇总

```bash
#!/bin/bash
# 账号与支付阻塞点检查脚本

echo "=== 账号与支付阻塞点检查 ==="
echo ""

# 1. 检查 Stripe 支持国家
echo "1. Stripe 支持的国家 (44个):"
curl -s "https://stripe.com/global" | grep -oP 'country=[A-Z]{2}' | sed 's/country=//' | sort -u | tr '\n' ' '
echo ""
echo ""

# 2. 检查特定国家是否支持
check_country() {
    local country=$1
    if curl -s "https://stripe.com/global" | grep -q "country=$country"; then
        echo "✅ $country 支持"
    else
        echo "❌ $country 不支持"
    fi
}

echo "2. 常见国家检查:"
check_country "CN"  # 中国
check_country "HK"  # 香港
check_country "SG"  # 新加坡
check_country "US"  # 美国
check_country "TW"  # 台湾
echo ""

# 3. 账号检查清单
echo "3. 必须填写字段检查:"
echo "⬜ 创作者真实姓名"
echo "⬜ 联系邮箱 (可收验证邮件)"
echo "⬜ 所在国家/城市"
echo "⬜ Substack publication 名称"
echo "⬜ Stripe 开户国家"
echo "⬜ 身份证件类型和号码"
echo "⬜ 银行账户信息"
echo "⬜ 税务表格类型 (W-9/W-8BEN)"
echo "⬜ 定价偏好 ($5/$9 monthly)"
echo ""

# 4. 测试支付检查
echo "4. 测试支付检查:"
echo "⬜ Stripe 测试卡: 4242 4242 4242 4242"
echo "⬜ 测试页面可访问"
echo "⬜ 支付流程正常"
echo "⬜ 收到订阅确认"
echo ""

echo "=== 检查完毕 ==="
echo "若以上任何项未完成，请 kanban_block 并说明具体需要的字段"
```

---

## 8. 完成确认

当所有检查项通过后，填写以下确认信息:

```yaml
verification_completed:
  date: "2026-XX-XX"
  verified_by: "_______"  # 验证人/工具
  
blockers_found:
  - none  # 或列出发现的阻塞点
  
next_action: "执行 substack_launch_checklist.md Day 0-1 步骤"
status: "READY_TO_LAUNCH"  # 或 BLOCKED
```

---

**文件路径**: `/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription/docs/account_payment_blockers.md`
