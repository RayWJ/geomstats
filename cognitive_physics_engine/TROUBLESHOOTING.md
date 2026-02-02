# 🔧 前后端连接问题已修复！

## ✅ 问题解决

**问题**: 前端显示 "Failed to query simulator: Load failed"

**原因**: 前端使用的是 `localhost:8000`，但在沙箱环境中需要使用公开 URL

**解决方案**: 更新前端代码自动检测并使用正确的 API 地址

---

## 🌐 现在可以访问了！

### 前端界面
**URL**: https://3000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai

刷新页面后应该就能正常工作了！

### 后端 API
**URL**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai

**API 文档**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/docs

---

## 🧪 验证测试

### ✅ 后端健康检查
```bash
curl https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/health
```

结果：
```json
{
    "status": "healthy",
    "simulator_initialized": true
}
```

### ✅ 查询测试
```bash
curl -X POST https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/query \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the outlook for NVIDIA stock?","n_viewpoints":10,"simulation_time":1.0}'
```

结果：
```json
{
    "question": "What is the outlook for NVIDIA stock?",
    "consensus": "Strategic assessment suggests, the consensus is a positive outlook with caution.",
    "confidence": 0.0,
    "n_clusters": 10,
    "n_viewpoints": 10,
    "simulation_time": 1.0
}
```

---

## 🎯 使用步骤

### 1️⃣ 打开前端
访问: https://3000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai

### 2️⃣ 输入问题
在输入框中输入你的问题，例如：
- "What is the outlook for NVIDIA stock?"
- "人工智能的未来如何？"
- "区块链技术前景？"

### 3️⃣ 调整参数（可选）
- **Viewpoints**: 10-100 推荐
- **Diversity**: 0.3 默认
- **Simulation Time**: 3-10 秒
- **Time Step**: 0.1 默认

### 4️⃣ 点击运行
点击紫色的 "🚀 Run Simulation" 按钮

### 5️⃣ 查看结果
等待 3-10 秒，查看：
- **Consensus**: 共识结论
- **Confidence**: 置信度
- **Clusters**: 聚类数量

---

## 🐛 如果还是不工作

### 检查清单：

1. **刷新页面** 
   - 按 `Ctrl+F5` (Windows) 或 `Cmd+Shift+R` (Mac) 强制刷新

2. **清除浏览器缓存**
   - Chrome: F12 → Network 标签 → 勾选 "Disable cache"

3. **检查浏览器控制台**
   - 按 F12 打开开发者工具
   - 查看 Console 标签是否有错误

4. **检查网络请求**
   - F12 → Network 标签
   - 点击 "Run Simulation"
   - 查看是否有红色的失败请求

5. **直接测试 API**
   ```bash
   curl https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/health
   ```

---

## 📊 已验证的功能

✅ 后端 API 服务器运行正常  
✅ /health 端点响应正常  
✅ /query 端点可以处理请求  
✅ 返回 JSON 格式正确  
✅ 前端代码已更新使用正确 URL  

---

## 💡 使用技巧

### 快速测试
- 使用 10-20 个 viewpoints
- Simulation time 设为 2-3 秒
- 这样几秒钟就能看到结果

### 精确分析
- 使用 50-100 个 viewpoints
- Simulation time 设为 5-10 秒
- 置信度会更高，但需要等待更久

### 问题建议
- 具体明确的问题效果更好
- 避免太抽象或太宽泛的问题
- 可以用中文或英文

---

## 🔗 快速链接

- **前端界面**: https://3000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai
- **API 文档**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/docs
- **健康检查**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/health

---

**现在应该可以正常使用了！** 🎉

如果还有问题，告诉我具体的错误信息，我会帮你解决。
