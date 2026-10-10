# 微信小程序：从零到体验版

给零基础使用者的 Codex skill。把想法告诉 Codex，由它完成开发、云端配置、上传、设为体验版、添加体验者及交付二维码；你只需填写必要信息、扫码、授权，并在自己的手机上试用。

重点是把体验版真正交到家人手里。既可新建小程序，也可接手已有项目、修复问题和更新体验版。不会把“代码上传成功”当成“对方已经能用”。

## 安装

将下面这句话发送给 Codex 即可，由 Codex 安装，不需要你操作终端：

> 帮我安装这个仓库的 skill：https://github.com/loganwang185/wechat-miniprogram-zero-to-trial ，技能目录是 skills/wechat-miniprogram-zero-to-trial。

也可以把 `skills/wechat-miniprogram-zero-to-trial` 文件夹放到 Codex 的用户技能目录（通常是 `~/.codex/skills/`），在新聊天中使用。

## 使用

安装后，发给 Codex：

> 使用 $wechat-miniprogram-zero-to-trial，帮我做一个两个人用的记账和待办小程序，做到能扫码使用的体验版。能由你完成的都直接完成，我只负责必要信息、扫码和授权。

已有项目可以说：

> 使用 $wechat-miniprogram-zero-to-trial，把这个项目更新成体验版给家人用，保留原来的数据。

## 包含什么

- 从需求、账号准备、开发环境和页面开发，到云服务、共享权限和隐私配置。
- 体验版发布的完整操作、体验成员权限、二维码及真实手机验收。
- 后续更新、常见问题排查，以及按需进入的正式上线流程。
- 无第三方 Python 依赖的开发者工具辅助脚本：工程检查、开发预览、代码上传。
- 微信和腾讯云官方资料索引，最近核对于 **2026-10-10**。

网页操作优先使用已安装的 Ego Browser；缺少工具时 Codex 先协助配置。浏览器操作不取代微信开发者工具。脚本路径由 Codex 查找与配置，Windows 批处理命令使用官方工具本身。

平台身份核验、扫码确认及个人授权仍由本人完成；体验版资格、云服务费用和功能开放范围以当前账号的官方页面为准。技能不会要求零基础使用者手动写代码或运行部署命令。

本仓库只包含可复用技能，不含实际业务项目、账号密钥、个人资料或体验二维码。公开仓库不等于小程序已正式上线。

## 文件

入口：[SKILL.md](skills/wechat-miniprogram-zero-to-trial/SKILL.md) · [发布流程](skills/wechat-miniprogram-zero-to-trial/references/trial-release.md) · [官方依据](skills/wechat-miniprogram-zero-to-trial/references/official-sources.md)

开发维护者可运行 `python3 -m unittest discover -s tests -v` 验证辅助脚本。测试使用替身命令，不上传真实小程序或变更微信账号。
