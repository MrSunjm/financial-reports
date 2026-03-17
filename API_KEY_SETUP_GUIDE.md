# 🔑 币安API密钥配置指南

## 📋 配置步骤

### 1. 获取币安API密钥
1. 登录币安官网 (https://www.binance.com)
2. 进入用户中心 → API管理
3. 创建新的API密钥
4. 设置API密钥名称（如：financial-analysis）
5. 获取API Key和Secret Key

### 2. 配置权限设置
确保API密钥有以下权限：
- ✅ 读取权限 (Enable Reading)
- ✅ 允许现货交易 (Allow Spot & Margin Trading)
- ❌ 禁用提现权限 (Disable Withdrawals - 安全考虑)

### 3. 编辑配置文件
编辑 `binance_config.py` 文件：

```python
# 币安API配置
BINANCE_CONFIG = {
    'api_key': '您的API Key',      # 替换为您的API Key
    'api_secret': '您的Secret Key', # 替换为您的Secret Key
    'testnet': False,               # 使用主网
    'base_url': 'https://api.binance.com'
}
```

### 4. 测试连接
运行测试脚本验证配置：

```bash
cd ~/Desktop/financial-reports-online
python3 binance_data_fetcher.py
```

## ⚠️ 安全注意事项

### 重要安全措施：
1. **不要分享API密钥**：API密钥等同于密码
2. **使用IP白名单**：在币安API设置中配置IP白名单
3. **定期更换密钥**：建议每3个月更换一次API密钥
4. **禁用提现权限**：分析系统只需要读取权限
5. **备份密钥**：安全存储API密钥副本

### 推荐的IP白名单：
```
您的服务器IP地址
您的本地网络IP地址
```

## 🔧 故障排除

### 常见问题：

#### 1. API连接失败
- 检查API密钥是否正确
- 检查网络连接
- 验证IP白名单设置

#### 2. 权限不足
- 确保已启用读取权限
- 检查API密钥是否被禁用

#### 3. 请求限制
- 币安API有请求频率限制
- 系统已实现缓存机制减少请求

## 🚀 立即配置

### 快速配置命令：
```bash
cd ~/Desktop/financial-reports-online
nano binance_config.py  # 编辑配置文件
```

### 测试配置：
```bash
python3 binance_data_fetcher.py
```

### 运行实时分析：
```bash
python3 realtime_analysis_system.py
```

## 📞 技术支持

### 需要帮助？
1. 检查币安API文档：https://binance-docs.github.io/apidocs/
2. 查看错误日志：`cron.log`
3. 联系技术支持

## ✅ 配置完成标志

成功配置后，您将看到：
```
✅ 币安API连接成功
   服务器时间: 2026-03-16 21:45:00
📊 测试获取实时价格...
   BTC: $73,860.42
   ETH: $2,100.25
   ...
```

**现在您可以享受基于真实币安数据的金融市场分析了！**
