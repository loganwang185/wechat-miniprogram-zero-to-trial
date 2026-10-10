# 官方资料与核对范围

最近人工流程核对：2026-10-10。以下为 Codex 通过官方网页读到的依据，不是永远有效的规则快照。实施时对将使用的能力再次核对；后台菜单名称、账号资格、收费、限额和可用 API 以当时官方页面为准。

| 官方资料 | 本次核对到的要点 | 何时读取 |
| --- | --- | --- |
| [微信：开始](https://developers.weixin.qq.com/miniprogram/dev/framework/quickstart/getstart.html) | 注册账号、取得小程序 AppID、安装工具、扫码登录及编译预览 | 新账号/新工程 |
| [微信：协同工作和发布](https://developers.weixin.qq.com/miniprogram/dev/framework/quickstart/release.html) | 开发版、体验版和线上版不同；上传后在后台选择开发版本设为体验版；体验成员有独立权限 | 每次首次发布或权限问题 |
| [微信：命令行 V2](https://developers.weixin.qq.com/miniprogram/dev/devtools/cli.html) | 服务端口前置条件；登录、预览、上传、构建 npm、云环境和云函数操作 | 命令行准备和参数排错 |
| [微信：miniprogram-ci](https://developers.weixin.qq.com/miniprogram/dev/devtools/ci.html) | 独立于开发者工具的上传/预览，代码上传密钥和 IP 白名单，云函数上传 | 使用密钥自动上传 |
| [微信：miniprogram-mp-ci](https://developers.weixin.qq.com/miniprogram/dev/devtools/miniprogram-mp-ci.html) | 添加体验成员 action 为 add_experiencer；调用成功后还需管理员微信确认 | 自动添加体验成员 |
| [CloudBase：创建环境](https://docs.cloudbase.net/quick-start/create-env) | 微信工具开通和环境关联；已有腾讯云环境需核对绑定；开发期免费有条件与限制 | 环境开通/复用 |
| [CloudBase：小程序快速开始](https://docs.cloudbase.net/quick-start/frameworks/wechat-miniprogram) | 小程序账号、开发工具、云环境及 wx.cloud 初始化 | 云端接入 |
| [微信：隐私指引填写](https://developers.weixin.qq.com/miniprogram/dev/framework/user-privacy/) | 按真实个人信息处理行为补充指引；现网与提审入口有区别 | 涉及用户数据与隐私接口 |
| [微信：订阅消息](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/subscribe-message-overview.html) | 弹窗一次性、长期以及新消息模式有不同机制与适用资格 | 做微信提醒之前 |

费用与备案不在技能中硬编码金额、期限或普遍豁免。开通/上线当次从已登录官方后台进入具体说明，保存适用于该账号的结论；无法核实时标注未核实并询问用户。

## 经验来源与适用边界

技能吸收了一个私人双人记账/待办项目的经验，只保留通用处理方法：体验权限与业务邀请分别验证、二维码与邀请码分别核对有效性、部署创建与代码生效分开确认、模拟器不能替代第二真实账号验证。该项目真实名称、AppID、环境编号、人员、联系方式、邀请码和二维码均不随技能发布。

私人项目发生过的失败不是微信平台通用规则。例如邀请保留多久、是否单次使用、生成新码是否使旧码失效，应读取当前项目设计；不能推广为所有微信小程序的统一限制。官方新能力和旧文档有冲突时查其生效范围，保留不确定性，不自行下结论。
