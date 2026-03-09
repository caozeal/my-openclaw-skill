# wechat-markdown-publisher

把 Markdown 转成适合微信公众号编辑器粘贴的 HTML。

## 用法

在 workspace 根目录执行：

```bash
python3 ./skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --theme wechat --embed-images --copy
```

## 图片说明

现在脚本会优先做这两件事：

- **支持两种图片语法**：普通 Markdown `![alt](path)`，以及 Obsidian 风格 `![[path]]`
- **本地相对路径图片**：即使不加 `--embed-images`，也会自动转成可直接打开的 `file://` 绝对路径，方便本地预览
- **远程图片 / 需要更稳粘贴到公众号**：加 `--embed-images`，会尽量转成 base64

如果你发现“HTML 里看不到图片”，优先用：

```bash
python3 ./skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --theme janus --embed-images --output article.wechat.html
```

## 一键预览

```bash
bash ./skills/wechat-markdown-publisher/scripts/preview_wechat.sh ./skills/wechat-markdown-publisher/example.md janus
```

它会先生成 `.wechat.html`，再尽量用系统默认浏览器打开。

## 可用主题

- `wechat`
- `notion`
- `claude`
- `janus`（更克制、直给、正文感更强）

## 常见示例

```bash
# 微信原生风格
python3 ./skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --theme wechat --embed-images --copy

# Notion 风格
python3 ./skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --theme notion --embed-images --copy

# Claude 风格
python3 ./skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --theme claude --embed-images --copy

# Janus 风格
python3 ./skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --theme janus --embed-images --copy

# 指定标题
python3 ./skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --title "标题" --copy

# 输出到文件
python3 ./skills/wechat-markdown-publisher/scripts/md_to_wechat.py article.md --output out/article.html
```

## 输出结果

默认会生成一个 `.wechat.html` 文件；如果加了 `--copy`，会尽量复制到剪贴板。

## 说明

- `--embed-images` 会尽量把图片转成 base64，减少公众号对第三方图片的兼容问题
- 这是“生成可粘贴 HTML”的方案，不直接调用公众号 API
- 如果剪贴板失败，就打开输出的 HTML 文件，全选复制即可
