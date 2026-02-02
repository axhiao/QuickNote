# QuickNote
只记录你真正想保留的内容（基于视觉语言模型）。

[English Version](./README.md)

## 项目介绍
QuickNote 是一个面向 iOS 与 macOS 的轻量、注重隐私的信息捕捉工作流。

它不会持续记录你的屏幕行为，而是采用“主动保存”的模式：只有你认为值得保存时，才进行截图。截图（连同提示词）会发送给视觉语言模型，模型将内容整理为结构化 Markdown，然后写入 [Memos](https://github.com/usememos/memos)，便于后续检索与管理。

核心思路很简单：
- 截图很容易保存，但后续很难检索。
- 结构化笔记更容易搜索、打标签和复用。
- 该保存什么，应该由用户自己决定。

QuickNote 的灵感来自微软 [Recall](https://en.wikipedia.org/wiki/Windows_Recall) 引发的讨论，但设计理念相反：QuickNote 强调“选择性记忆”，而不是“默认全量记录”。

## 工作流程
```
            IOS / MacOS (Shortcuts)
               │
               ▼
┌───────────────────────────────┐
│            Server             │
│   (VisionLanguage Model)      │
│            parse              │
└──────────────┬────────────────┘
               │ 
               ▼
              Memos
```

## QuickNote 解决了什么问题
- 将原始截图转换为可检索的笔记。
- 同时保留原图与提取后的文字上下文。
- 在移动端与桌面端都能低成本快速记录。
- 在 Memos 中按关键词和标签组织信息。

## 当前实现方式
QuickNote 当前以 [Memos](https://github.com/usememos/memos) 作为笔记界面与存储层。

客户端触发方式：
- **iOS**：通过 Apple Shortcuts 触发截图与上传。
- **macOS**：通过全局热键触发同一个 Shortcut（可配合 Raycast）。

## iOS 快捷指令
可使用以下快捷指令模板：

[QuickNote iOS Shortcut](https://www.icloud.com/shortcuts/66484a23c6094afbb6c2078c5cd237d9)

导入后，请将请求 URL 修改为你自己的 QuickNote 服务地址。IOS 可以设置手机的 action 按钮绑定 Shortcuts 进行触发，非常方便快捷。

## macOS 触发方式（推荐）
在 macOS 上，建议使用 Raycast 绑定全局热键来触发 Shortcut。

示例：
- 热键：`Command + F2`
- 优先级：设置为高（避免热键被其他应用抢占）

## 演示
### iPhone

[https://youtu.be/khHIss2ajnc](https://youtu.be/khHIss2ajnc)

### macOS
[https://youtu.be/SHuq5kxRCWA](https://youtu.be/SHuq5kxRCWA)

## 快速开始
QuickNote 依赖 Memos。请先独立部署 Memos，再配置并启动 QuickNote 服务端。也可以使用下面的docker compsoe 进行快速部署，里面包含了 Memos 服务。

```bash
cd server
cp .env.example .env
# 编辑 .env，设置模型提供方、API Key 和 memos 参数
docker compose up
```

服务启动后，将快捷指令中的请求地址指向该服务，即可开始使用。
