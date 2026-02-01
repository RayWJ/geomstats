# 🎯 认知物理引擎 - 测试访问指南

## ✅ 系统状态：**运行中**

两个服务器都已启动并正常运行！

---

## 🌐 访问地址

### 1. **前端 Web 界面** (推荐使用)
**URL**: https://3000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai

**功能**:
- 🎨 美观的渐变 UI
- 📊 实时参数调整
- 🌍 6D 流形维度展示
- 🚀 一键运行模拟

**使用方法**:
1. 点击上面的 URL 在浏览器中打开
2. 在输入框中输入你的问题（默认已有示例）
3. 调整参数（可选）：
   - Viewpoints: 观点数量 (10-500)
   - Diversity: 多样性 (0.1-1.0)
   - Simulation Time: 模拟时间 (1-30秒)
   - Time Step: 时间步长 (0.01-0.5)
4. 点击 "🚀 Run Simulation" 按钮
5. 等待几秒，查看结果

---

### 2. **后端 API 服务器**
**URL**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai

**API 文档**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/docs

**主要端点**:
- `GET /` - API 信息
- `GET /health` - 健康检查
- `POST /query` - 查询模拟器
- `POST /inject` - 注入新信息
- `POST /compare` - 场景对比
- `GET /examples` - 示例查询

---

## 🧪 快速测试方法

### 方法 1: 使用 Web 界面（最简单）
直接访问前端 URL，在浏览器中操作。

### 方法 2: 使用 curl 测试 API

```bash
# 健康检查
curl https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/health

# 查询示例
curl -X POST https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "人工智能的未来如何？",
    "n_viewpoints": 50,
    "simulation_time": 5.0
  }'
```

### 方法 3: 使用 Python

```python
import requests

# API 基础 URL
API_URL = "https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai"

# 发送查询
response = requests.post(f"{API_URL}/query", json={
    "question": "区块链技术的未来如何？",
    "n_viewpoints": 30,
    "simulation_time": 3.0
})

result = response.json()
print(f"共识: {result['consensus']}")
print(f"置信度: {result['confidence']:.1%}")
```

---

## 📝 测试示例问题

试试这些问题：

1. **金融类**
   - "英伟达股票的前景如何？"
   - "应该投资人工智能基础设施吗？"
   - "加密货币市场未来走势？"

2. **技术类**
   - "量子计算何时能投入生产使用？"
   - "人工智能会取代程序员吗？"
   - "5G 技术的影响有多大？"

3. **社会类**
   - "远程工作会成为主流吗？"
   - "气候变化的风险有多严重？"
   - "教育系统需要改革吗？"

4. **创新类**
   - "元宇宙是未来还是泡沫？"
   - "自动驾驶何时能普及？"
   - "脑机接口技术的前景？"

---

## 🎮 参数调整指南

### Viewpoints (观点数量)
- **少 (10-30)**: 快速测试，结果可能不稳定
- **中 (50-100)**: 平衡速度和准确性 ✅ 推荐
- **多 (200-500)**: 更全面，但速度慢

### Diversity (多样性)
- **低 (0.1-0.2)**: 观点集中，快速收敛
- **中 (0.3-0.5)**: 平衡探索 ✅ 推荐
- **高 (0.6-1.0)**: 探索广泛，可能不收敛

### Simulation Time (模拟时间)
- **短 (1-3秒)**: 快速预览
- **中 (5-10秒)**: 标准设置 ✅ 推荐
- **长 (15-30秒)**: 充分收敛

### Time Step (时间步长)
- **大 (0.3-0.5)**: 快但不稳定
- **中 (0.1-0.2)**: 平衡 ✅ 推荐
- **小 (0.01-0.05)**: 精确但慢

---

## 🔍 理解结果

### Consensus (共识)
自然语言描述的最终结论，综合了所有收敛观点。

### Confidence (置信度)
- **0-20%**: 观点分散，没有强共识
- **20-50%**: 部分收敛，有一定共识
- **50-80%**: 良好收敛，较强共识 ✅
- **80-100%**: 高度收敛，强共识

### Clusters (聚类数)
- **多聚类 (20+)**: 观点分散，多种意见
- **中聚类 (5-20)**: 几个主要观点
- **少聚类 (1-5)**: 强烈共识 ✅

**理想结果**: 少量聚类 + 高置信度

---

## 🎨 6D 流形维度说明

界面下方显示的6个维度：

1. **Z - Level** (层级)
   - L1: 可验证事实
   - L2: 数据分析
   - L3: 战略评估
   - L4: 观点意见
   - L5: 纯推测

2. **Y - Domain** (领域)
   - 科技、金融、政治等

3. **X - Stance** (立场)
   - 看空 ↔ 中立 ↔ 看多

4. **W - Intent** (意图)
   - 可疑 ↔ 建设性

5. **T - Time** (时间)
   - 过去 ↔ 现在 ↔ 未来

6. **S - Scale** (尺度)
   - 微观 ↔ 中观 ↔ 宏观

---

## 🐛 常见问题

### Q: 前端显示 "Cannot connect to backend"
**A**: 确保后端 API 正在运行。前端会自动连接到 `http://localhost:8000`

### Q: 置信度总是很低
**A**: 尝试：
- 增加模拟时间
- 减少多样性
- 使用更具体的问题

### Q: 查询很慢
**A**: 减少观点数量或缩短模拟时间

### Q: 结果总是 "中立立场"
**A**: 这是 Mock LLM 的默认行为。在生产环境中，替换为真实 LLM API 会有更准确的语义分析。

---

## 📊 系统架构

```
用户输入问题
    ↓
[Translator: 语义分析]
    ↓
生成 N 个初始观点坐标 (6D)
    ↓
[Dynamics: 物理模拟]
    在势能场中运动
    ↓
收敛到 Nash 均衡点
    ↓
[Translator: 共识合成]
    ↓
自然语言共识 + 置信度
```

---

## 🎓 进阶使用

### 注入突发新闻

```bash
# 先查询基准
curl -X POST $API_URL/query -d '{"question": "英伟达前景?"}'

# 注入新闻
curl -X POST $API_URL/inject -d '{"information": "英伟达宣布重大合作"}'

# 再次查询，观察变化
curl -X POST $API_URL/query -d '{"question": "英伟达前景?"}'
```

### 场景对比

```bash
curl -X POST $API_URL/compare -d '{
  "question": "AI 芯片市场展望？",
  "scenarios": [
    "场景A: AI 需求激增",
    "场景B: 经济衰退",
    "场景C: 新竞争者出现"
  ]
}'
```

---

## 💡 提示

1. **首次使用**: 使用默认参数和示例问题
2. **速度优化**: 减少观点数量到 30-50
3. **精确结果**: 增加模拟时间到 15-20 秒
4. **探索性分析**: 提高多样性到 0.5-0.7
5. **对比测试**: 用相同问题但不同参数多次测试

---

## 🎯 快速测试清单

✅ 访问前端 URL  
✅ 输入一个问题  
✅ 点击 "Run Simulation"  
✅ 等待结果（5-10秒）  
✅ 查看共识和置信度  
✅ 尝试不同参数  
✅ 测试不同类型问题  

---

**现在开始探索认知物理引擎吧！** 🚀

**前端界面**: https://3000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai

**API 文档**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/docs
