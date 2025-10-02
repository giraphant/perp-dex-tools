# Pushover 推送通知设置指南

## 简介

本交易机器人已集成 Pushover 推送通知功能，可在以下情况自动发送通知：

- 🚀 **程序启动** - 显示交易配置信息
- 🚨 **程序停止/崩溃** - 显示停止原因和时间
- ⚠️ **交易错误** - 显示具体错误信息
- 📢 **重要提醒** - 其他重要交易事件

## 设置步骤

### 1. 注册 Pushover 账号
访问 [https://pushover.net/](https://pushover.net/) 注册账号

### 2. 创建应用
1. 登录后点击 "Create an Application/API Token"
2. 填写应用名称（如：Trading Bot）
3. 选择应用类型：Script
4. 提交后获得 **Application Token**

### 3. 获取用户密钥
在账号主页可以看到您的 **User Key**

### 4. 配置环境变量
在项目根目录的 `.env` 文件中添加：

```bash
# Pushover notification (optional)
PUSHOVER_TOKEN=your_app_token_here
PUSHOVER_USER_KEY=your_user_key_here

# Timezone configuration
TIMEZONE=Europe/London
```

### 5. 测试配置
运行测试脚本验证配置：

```bash
source env/bin/activate
python test_pushover.py
```

如果配置正确，您将收到测试推送通知。

### 6. 测试时区设置
验证时区配置是否正确：

```bash
source env/bin/activate
python test_timezone.py
```

这将显示当前配置的时区和时间。

## 通知优先级

- **启动通知**: 普通优先级 (0)
- **停止/错误通知**: 高优先级 (1) - 会发出声音提醒
- **一般提醒**: 高优先级 (1)

## 故障排除

### UTF-8 编码错误
如果遇到编码错误，请确保：
1. 系统编码设置为 UTF-8
2. 消息内容不包含特殊字符
3. 重新启动程序

### 通知发送失败
检查：
1. Token 和 User Key 是否正确
2. 网络连接是否正常
3. Pushover 服务是否可用

### 禁用通知
如果不想接收通知，只需在 `.env` 文件中留空：
```bash
PUSHOVER_TOKEN=
PUSHOVER_USER_KEY=
```

## 同时使用多种通知

您可以同时配置 Pushover 和 Lark 通知：
- Pushover：适合手机推送
- Lark：适合团队协作

两种通知方式会同时工作，互不影响。

## 时区配置

程序默认使用英国伦敦时间 (`Europe/London`)。如需修改时区，请在 `.env` 文件中设置：

```bash
# 常用时区示例
TIMEZONE=Europe/London      # 英国伦敦时间 (GMT/BST)
TIMEZONE=America/New_York   # 美国东部时间 (EST/EDT)
TIMEZONE=Asia/Shanghai      # 中国时间 (CST)
TIMEZONE=Europe/Paris       # 欧洲中部时间 (CET/CEST)
TIMEZONE=Asia/Tokyo         # 日本时间 (JST)
```

时区会影响：
- 日志文件中的时间戳
- 推送通知中的时间显示
- CSV交易记录中的时间

## 支持

如有问题，请检查：
1. 运行 `python test_pushover.py` 测试配置
2. 查看程序日志文件
3. 确认 Pushover 账号状态正常