# my-openclaw-skill

这个仓库用于存放和共同维护各种 **OpenClaw skills** 源码。

## 定位

- 这里是 **skills 的源码仓库**
- 日常开发、版本管理、提交与推送，都在这里完成
- `~/.openclaw/workspace/skills/` 下的同名目录，仅作为 OpenClaw 实际运行时使用的位置

## 当前约定

以 `wechat-markdown-publisher` 为例：

- 源码主位置：
  `~/projects/github/my-openclaw-skill/skills/wechat-markdown-publisher`
- OpenClaw 运行位置：
  `~/.openclaw/workspace/skills/wechat-markdown-publisher`

当前运行位置采用 **symlink** 指向源码目录，因此：

- 改源码仓库里的文件 = OpenClaw 实际使用的就是最新内容
- 不再把 workspace 下的 skill 目录当作 git 主位置维护

## 目录建议

```text
skills/
  wechat-markdown-publisher/
  <another-skill>/
  <another-skill>/
```

后续新增 skill，统一放到 `skills/` 下。

## 推荐工作流

1. 在这个仓库里新增或修改 skill
2. 本地测试
3. `git commit` / `git push`
4. OpenClaw 直接通过 workspace 中的 symlink 使用

## 备注

这个仓库是“我和老曹一起写 skill”的总仓，不是单一 skill 专仓。
