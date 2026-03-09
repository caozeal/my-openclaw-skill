---
name: wechat-markdown-publisher
description: 将 Markdown 文档转换为适合微信公众号编辑器粘贴的 HTML 富文本，并尽力自动复制到剪贴板。适用于用户提到“公众号排版、Markdown 转公众号格式、复制到公众号编辑器、微信公众号文章粘贴发布”等场景。
---

# WeChat Markdown Publisher

参考 Raphael Publish 的思路，把本地 Markdown 转成**适合微信公众号编辑器粘贴**的 HTML。

## 什么时候用

当用户需要：
- 把 Markdown 文章转成公众号格式
- 复制文章到微信公众号编辑器
- 生成适合公众号排版的 HTML
- 将本地 `.md` 文档快速变成可粘贴稿件

## 默认做法

```bash
python3 /root/.openclaw/workspace/skills/wechat-markdown-publisher/scripts/md_to_wechat.py <input.md> --theme wechat --embed-images --copy
```

## 常用命令

```bash
# 微信原生风格 + 图片转 base64 + 尽量复制到剪贴板
python3 /root/.openclaw/workspace/skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --theme wechat --embed-images --copy

# Notion 风格
python3 /root/.openclaw/workspace/skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --theme notion --embed-images --copy

# Claude 风格
python3 /root/.openclaw/workspace/skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --theme claude --embed-images --copy

# 指定标题
python3 /root/.openclaw/workspace/skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --title "标题" --copy

# 输出 HTML 文件
python3 /root/.openclaw/workspace/skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --output out/article.html
```

## 当前支持

- Markdown → HTML 富文本
- 标题、段落、引用、列表、代码块、分隔线、链接、图片
- 基础表格支持
- 主题：`wechat` / `notion` / `claude`
- `--embed-images`：将本地或公网图片尽量转成 base64，减少公众号“第三方图片”问题
- `--copy`：尽量复制到剪贴板
- 公众号兼容处理：
  - 以内联样式为主
  - 连续图片转稳定表格布局
  - 列表段落扁平化
  - 中文标点与强调样式贴合，减少断行

## 注意

- 这是**粘贴到公众号编辑器**的方案，不直接调用公众号 API。
- 当前还没有实现 Raphael Publish 那种完整 Web UI、富文本魔法粘贴、多设备预览。
- 当前环境若没有可用剪贴板，脚本会保留 HTML 文件路径，便于手动复制。

## 结果判定

成功时优先返回：
- 输出文件路径
- 使用的主题
- 是否成功复制到剪贴板
- 是否已嵌入图片
- 如果复制失败，提醒“打开 HTML 文件全选复制即可”
