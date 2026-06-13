#!/usr/bin/env python3
"""
knowledge-subscription 静态销售站点生成器
Task: 889b251b
运行: python app/build_sales_site.py
功能: 将 markdown 样例包转为可直接部署的 HTML 销售页
部署: Cloudflare Pages / Vercel / GitHub Pages
"""

import json
import re
import sys
from pathlib import Path

PROJECT_DIR = Path("/home/AgentAdmin/.hermes/shared/dev-team/projects/knowledge-subscription")
INPUT_DIR = PROJECT_DIR / "reports" / "sample_pack"
OUTPUT_DIR = PROJECT_DIR / "site" / "sample_pack"


def read_md(name: str) -> str:
    path = INPUT_DIR / name
    if not path.exists():
        print(f"ERROR: {path} not found")
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def md_to_html(text: str) -> str:
    """极简 markdown 转 HTML（适合本项目的格式）"""
    # 转义 HTML
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    lines = text.splitlines()
    html = []
    in_code = False
    in_list = False
    in_table = False
    table_rows = []

    for line in lines:
        # 代码块
        if line.startswith("```"):
            if in_code:
                html.append("</pre></div>")
                in_code = False
            else:
                html.append('<div class="code-block"><pre>')
                in_code = True
            continue
        if in_code:
            html.append(line)
            continue

        # 标题
        if line.startswith("# "):
            html.append(f"<h1>{line[2:].strip()}</h1>")
            continue
        if line.startswith("## "):
            html.append(f"<h2>{line[3:].strip()}</h2>")
            continue
        if line.startswith("### "):
            html.append(f"<h3>{line[4:].strip()}</h3>")
            continue

        # 表格
        if line.startswith("| ") and " | " in line:
            if not in_table:
                in_table = True
                table_rows = []
            cells = [c.strip() for c in line.split("|")]
            cells = [c for c in cells if c]
            if all(set(c) <= set("- :|") for c in cells):
                continue  # skip separator
            table_rows.append(cells)
            continue
        else:
            if in_table:
                html.append('<div class="table-wrap"><table>')
                for i, row in enumerate(table_rows):
                    tag = "th" if i == 0 else "td"
                    html.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in row) + "</tr>")
                html.append("</table></div>")
                in_table = False
                table_rows = []

        # 列表
        if line.startswith("- ") or line.startswith("* "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            item = line[2:].strip()
            item = format_inline(item)
            html.append(f"<li>{item}</li>")
            continue
        else:
            if in_list:
                html.append("</ul>")
                in_list = False

        # 引用
        if line.startswith("> "):
            html.append(f'<blockquote>{format_inline(line[2:])}</blockquote>')
            continue

        # 粗体行（如 **Q:** 开头）
        if line.strip():
            line = format_inline(line)
            html.append(f"<p>{line}</p>")
        else:
            html.append("<br/>")

    if in_list:
        html.append("</ul>")
    if in_table:
        html.append('<div class="table-wrap"><table>')
        for i, row in enumerate(table_rows):
            tag = "th" if i == 0 else "td"
            html.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in row) + "</tr>")
        html.append("</table></div>")

    return "\n".join(html)


def format_inline(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


def extract_free_opps(text: str) -> list:
    """从 free_preview.md 提取3个机会标题和描述"""
    opps = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].startswith("### "):
            title = lines[i][4:].strip()
            desc = []
            i += 1
            while i < len(lines) and not lines[i].startswith("### ") and not lines[i].startswith("## "):
                if lines[i].strip() and not lines[i].startswith("---"):
                    desc.append(lines[i].strip())
                i += 1
            opps.append({"title": title, "desc": " ".join(desc[:3])})
            continue
        i += 1
    return opps


def build_index_html(free_html: str, catalog_html: str, free_opps: list) -> str:
    css = """
:root{--bg:#0f172a;--card:#1e293b;--text:#f8fafc;--muted:#94a3b8;--accent:#38bdf8;--accent2:#818cf8;--cta:#f59e0b;--danger:#ef4444;--success:#22c55e}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
.container{max-width:760px;margin:0 auto;padding:24px}
.hero{text-align:center;padding:48px 24px 32px;background:linear-gradient(135deg,var(--bg),#1e293b);border-bottom:1px solid #334155}
.hero h1{font-size:2.2rem;margin:0 0 12px}
.hero p{color:var(--muted);font-size:1.15rem;max-width:560px;margin:0 auto}
.badge{display:inline-block;background:var(--accent2);color:#fff;padding:4px 12px;border-radius:999px;font-size:.8rem;font-weight:600;margin-bottom:12px}
.cta-btn{display:inline-block;background:var(--cta);color:#0f172a;padding:14px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:1.05rem;box-shadow:0 4px 14px rgba(245,158,11,.35);transition:transform .15s}
.cta-btn:hover{transform:translateY(-2px)}
.cta-btn.secondary{background:var(--card);color:var(--text);box-shadow:0 4px 14px rgba(0,0,0,.25)}
.card{background:var(--card);border-radius:12px;padding:24px;margin:24px 0;border:1px solid #334155}
.card h2{margin-top:0;color:var(--accent)}
.opp-card{background:var(--card);border-radius:12px;padding:20px;margin:16px 0;border-left:4px solid var(--accent2)}
.opp-card h3{margin:0 0 8px;color:var(--accent)}
.opp-card p{color:var(--muted);margin:0}
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
th,td{border:1px solid #334155;padding:10px 12px;text-align:left}
th{background:#0f172a;color:var(--accent);font-weight:600}
ul{padding-left:20px}
ul li{margin:6px 0}
blockquote{border-left:4px solid var(--accent2);padding-left:16px;margin:12px 0;color:var(--muted);font-style:italic}
.code-block{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:16px;overflow-x:auto;margin:12px 0}
.code-block pre{margin:0;color:#e2e8f0;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:.9rem}
.pricing{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:24px 0}
.price-card{background:var(--card);border-radius:12px;padding:20px;text-align:center;border:1px solid #334155}
.price-card.popular{border-color:var(--cta);position:relative}
.popular-badge{position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:var(--cta);color:#0f172a;padding:2px 10px;border-radius:999px;font-size:.75rem;font-weight:700}
.price-card h4{margin:0 0 8px}
.price-card .price{font-size:1.6rem;font-weight:700;color:var(--accent)}
.price-card ul{text-align:left;padding-left:20px}
.faq-item{margin:16px 0}
.faq-item strong{display:block;color:var(--accent);margin-bottom:4px}
.footer{text-align:center;padding:32px 24px;color:var(--muted);font-size:.9rem;border-top:1px solid #334155;margin-top:48px}
@media(max-width:640px){.hero h1{font-size:1.6rem}.container{padding:16px}.pricing{grid-template-columns:1fr}}
"""
    # 构建3个机会卡片
    opp_cards = "\n".join(
        f'<div class="opp-card"><h3>{o["title"]}</h3><p>{o["desc"]}</p></div>'
        for o in free_opps
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI赚钱机会雷达 - 专业版订阅</title>
<meta name="description" content="每日自动收集AI赚钱机会，含深度SOP、收益测算、可运行代码和AI提示词模板。">
<style>{css}</style>
</head>
<body>
<div class="hero">
<div class="container">
<div class="badge">🔥 首批验证用户招募中</div>
<h1>AI赚钱机会雷达</h1>
<p>每天为你精选 <strong>2-3个经过验证的AI赚钱机会</strong>，附完整执行SOP、收益测算、可运行代码和AI提示词模板。不是信息，而是可直接执行的变现系统。</p>
<div style="margin-top:24px">
<a href="#pricing" class="cta-btn">立即订阅 ¥99/月</a>
<a href="#preview" class="cta-btn secondary" style="margin-left:12px">免费试看样例</a>
</div>
</div>
</div>

<div class="container">
<div class="card" id="preview">
<h2>📖 免费试看版（3个机会节选）</h2>
<p>以下是你订阅后将每日收到的内容节选。完整版含<strong>8个机会的深度SOP、代码片段、AI提示词模板</strong>。</p>
{opp_cards}
<div style="margin-top:20px">
<a href="free_preview.html" class="cta-btn secondary">阅读完整免费试看版 →</a>
</div>
</div>

<div class="card" id="catalog">
<h2>📚 专业版订阅目录</h2>
<p>首批收录 <strong>8个已深度解析的AI赚钱机会</strong>，覆盖B2B服务、SaaS、社媒变现、独立开发者、求职陪跑等赛道。</p>
<div style="margin-top:16px">
<a href="premium_catalog.html" class="cta-btn secondary">查看完整目录与定价 →</a>
</div>
</div>

<div class="card" id="pricing">
<h2>💰 定价方案</h2>
<div class="pricing">
<div class="price-card">
<h4>月付</h4>
<div class="price">¥99/月</div>
<ul>
<li>全部内容 + 会员群</li>
<li>基础脚本工具包</li>
<li>7天无理由退款</li>
</ul>
<a href="#" class="cta-btn secondary" style="margin-top:12px;display:block">选择月付</a>
</div>
<div class="price-card popular">
<div class="popular-badge">最划算</div>
<h4>年付</h4>
<div class="price">¥799/年</div>
<ul>
<li>全部内容 + 1v1评估</li>
<li>完整脚本库 + 陪跑营折扣</li>
<li>省 ¥389</li>
</ul>
<a href="#" class="cta-btn" style="margin-top:12px;display:block">选择年付</a>
</div>
<div class="price-card">
<h4>企业版</h4>
<div class="price">¥2,999/年</div>
<ul>
<li>5个账号</li>
<li>定制行业雷达</li>
<li>专属支持</li>
</ul>
<a href="#" class="cta-btn secondary" style="margin-top:12px;display:block">咨询企业版</a>
</div>
</div>
</div>

<div class="card" id="faq">
<h2>❓ 常见问题</h2>
<div class="faq-item">
<strong>Q: 内容能直接复制赚钱吗？</strong>
<p>不能。我们提供经过验证的方向、数据、SOP和工具，执行和结果取决于你的投入、技能和市场变化。不承诺收益。</p>
</div>
<div class="faq-item">
<strong>Q: 可以退款吗？</strong>
<p>7天内无理由全额退款。超过7天按剩余天数比例退。</p>
</div>
<div class="faq-item">
<strong>Q: 我没有技术背景，能跟上吗？</strong>
<p>60%内容面向非技术用户，技术类内容会标注难度等级。非技术用户可重点看「社媒变现」「自动化现金流」「求职陪跑」专栏。</p>
</div>
<div class="faq-item">
<strong>Q: 代码片段可以直接商用吗？</strong>
<p>可以。所有源码和模板均为原创，可自由用于个人或商业项目。</p>
</div>
</div>

<div class="card" id="contact">
<h2>📬 联系与订阅</h2>
<p>当前为 <strong>占位收款入口</strong>。请通过以下方式联系运营者获取真实订阅链接：</p>
<ul>
<li>微信客服: <strong>ai-radar-support</strong>（占位）</li>
<li>邮箱: <strong>contact@ai-radar.dev</strong>（占位）</li>
<li>订阅入口: <strong>https://ai-radar.io/subscribe</strong>（占位）</li>
</ul>
<p style="color:var(--danger)">⚠️ 部署前必须替换为真实收款入口（小报童/爱发电/Substack/微信收款码）。</p>
</div>
</div>

<div class="footer">
<p>AI赚钱机会雷达 | knowledge-subscription | 任务ID: 889b251b</p>
<p>由 Dev Team 自动生成 · 数据仅供参考 · 执行风险自行评估</p>
</div>
</body>
</html>
"""


def generate() -> list:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = []

    free_text = read_md("free_preview.md")
    catalog_text = read_md("premium_catalog.md")
    free_opps = extract_free_opps(free_text)

    # 1. 主销售页
    idx_path = OUTPUT_DIR / "index.html"
    idx_path.write_text(build_index_html("", "", free_opps), encoding="utf-8")
    generated.append(str(idx_path))

    # 2. 完整免费试看页
    fp_html = md_to_html(free_text)
    fp_path = OUTPUT_DIR / "free_preview.html"
    css = """
:root{--bg:#0f172a;--card:#1e293b;--text:#f8fafc;--muted:#94a3b8;--accent:#38bdf8;--accent2:#818cf8;--cta:#f59e0b}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
.container{max-width:760px;margin:0 auto;padding:24px}
.header{padding:24px 0;border-bottom:1px solid #334155;margin-bottom:24px}
.header a{color:var(--accent);text-decoration:none;font-weight:600}
.card{background:var(--card);border-radius:12px;padding:24px;margin:24px 0;border:1px solid #334155}
h1{color:var(--accent);margin-top:0}
h2{color:var(--accent2);margin-top:32px}
h3{color:var(--accent);margin-top:24px}
.table-wrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:.95rem}
th,td{border:1px solid #334155;padding:10px 12px;text-align:left}
th{background:#0f172a;color:var(--accent);font-weight:600}
ul{padding-left:20px}
ul li{margin:6px 0}
blockquote{border-left:4px solid var(--accent2);padding-left:16px;margin:12px 0;color:var(--muted);font-style:italic}
.code-block{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:16px;overflow-x:auto;margin:12px 0}
.code-block pre{margin:0;color:#e2e8f0;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:.9rem}
.cta-btn{display:inline-block;background:var(--cta);color:#0f172a;padding:14px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:1.05rem;box-shadow:0 4px 14px rgba(245,158,11,.35);transition:transform .15s}
.cta-btn:hover{transform:translateY(-2px)}
.footer{text-align:center;padding:32px 24px;color:var(--muted);font-size:.9rem;border-top:1px solid #334155;margin-top:48px}
@media(max-width:640px){.container{padding:16px}}
"""
    fp_html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>免费试看版 - AI赚钱机会雷达</title>
<style>{css}</style>
</head>
<body>
<div class="container">
<div class="header"><a href="index.html">← 返回销售页</a></div>
{fp_html}
<div style="margin:32px 0;text-align:center">
<a href="index.html#pricing" class="cta-btn">解锁专业版 →</a>
</div>
</div>
<div class="footer">
<p>AI赚钱机会雷达 | 免费试看版 | 任务ID: 889b251b</p>
</div>
</body>
</html>
"""
    fp_path.write_text(fp_html_full, encoding="utf-8")
    generated.append(str(fp_path))

    # 3. 完整目录页
    cat_html = md_to_html(catalog_text)
    cat_path = OUTPUT_DIR / "premium_catalog.html"
    cat_html_full = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>专业版目录 - AI赚钱机会雷达</title>
<style>{css}</style>
</head>
<body>
<div class="container">
<div class="header"><a href="index.html">← 返回销售页</a></div>
{cat_html}
<div style="margin:32px 0;text-align:center">
<a href="index.html#pricing" class="cta-btn">立即订阅 →</a>
</div>
</div>
<div class="footer">
<p>AI赚钱机会雷达 | 专业版目录 | 任务ID: 889b251b</p>
</div>
</body>
</html>
"""
    cat_path.write_text(cat_html_full, encoding="utf-8")
    generated.append(str(cat_path))

    return generated


if __name__ == "__main__":
    files = generate()
    print(f"Generated {len(files)} HTML files:")
    for f in files:
        print(f"  - {f}")
    print("\nDeploy: npx wrangler pages deploy site/sample_pack (Cloudflare)")
    print("         or git push to GitHub Pages / Vercel")
