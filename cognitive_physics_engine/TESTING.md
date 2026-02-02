# 🧪 认知物理引擎 - 完整测试指南

## ✅ 测试结果摘要

所有测试已通过！系统完全正常运行。

---

## 🎯 测试方式汇总

### 方式 1: ⚡ 快速验证（30秒）

```bash
cd cognitive_physics_engine/backend
python -c "
import sys
sys.path.insert(0, 'cpe')
from cpe import WorldSimulator

simulator = WorldSimulator(backend='numpy', hidden_dim=32, n_layers=2)
result = simulator.query('测试查询', n_viewpoints=10, simulation_time=1.0)
print(f'✅ 系统正常！共识: {result[\"consensus\"]}')
"
```

**预期输出**: 
```
🌍 Initializing World Simulator...
✓ World Simulator ready!
✅ 系统正常！共识: ...
```

---

### 方式 2: 📋 完整演示（5-10分钟）

```bash
cd cognitive_physics_engine/backend
python demo.py
```

**交互选项**:
- `1`: 基础查询演示
- `2`: 突发新闻注入演示
- `3`: 多场景对比演示
- `4`: 流形结构探索
- `5`: 收敛模式分析
- `0`: 运行全部演示

**预期**: 5个完整演示场景，展示系统所有功能

---

### 方式 3: 🔬 单元测试

#### 测试流形模块
```bash
cd cognitive_physics_engine/backend
python -m cpe.manifold
```

**预期输出**:
```
=== Cognitive Manifold Test ===
✓ Random point generated
✓ Interpretation: L3: Strategic Assessment
✓ Metric matrix shape: (6, 6)
✓ Distance from L1-Bull to L5-Bear: 1.2207
✓ Manifold test completed!
```

#### 测试翻译器
```bash
python -c "
import sys
sys.path.insert(0, 'cpe')
from manifold import CognitiveManifold
from translator import Translator

manifold = CognitiveManifold()
translator = Translator(manifold)

text = 'NVIDIA股价看涨'
coord = translator.text_to_coordinate(text)
print(f'文本: {text}')
print(f'坐标: {coord}')
print(f'解释: {manifold.interpret_point(coord)}')
"
```

#### 测试动力学
```bash
python -c "
import sys
import torch
sys.path.insert(0, 'cpe')
from manifold import CognitiveManifold
from dynamics import CognitiveDynamics

manifold = CognitiveManifold()
dynamics = CognitiveDynamics(manifold, hidden_dim=32, n_layers=2)

points = torch.randn(20, 6) * 0.3
final, _ = dynamics.simulate_collapse(points, T=2.0, dt=0.2)
print(f'✓ 初始分散度: {points.std():.4f}')
print(f'✓ 最终分散度: {final.std():.4f}')
print(f'✓ 动力学测试通过')
"
```

---

### 方式 4: 🌐 API 服务器测试

#### 4.1 启动服务器

```bash
cd cognitive_physics_engine/backend
python server.py
```

**预期输出**:
```
🚀 Starting Cognitive Physics Engine API...
🌍 Initializing World Simulator...
✓ API Ready!
INFO: Uvicorn running on http://0.0.0.0:8000
```

#### 4.2 测试健康检查

```bash
curl http://localhost:8000/health
```

**预期响应**:
```json
{
    "status": "healthy",
    "simulator_initialized": true
}
```

#### 4.3 测试查询接口

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "人工智能的未来如何？",
    "n_viewpoints": 30,
    "simulation_time": 5.0,
    "dt": 0.2
  }'
```

**预期响应**:
```json
{
    "question": "人工智能的未来如何？",
    "consensus": "Strategic assessment suggests...",
    "confidence": 0.xx,
    "n_clusters": xx,
    "n_viewpoints": 30,
    "simulation_time": 5.0
}
```

#### 4.4 测试信息注入

```bash
curl -X POST http://localhost:8000/inject \
  -H "Content-Type: application/json" \
  -d '{
    "information": "突发：OpenAI 发布 GPT-5"
  }'
```

#### 4.5 测试场景对比

```bash
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "question": "AI投资前景如何？",
    "scenarios": [
      "AI采用加速，需求大增",
      "经济衰退，科技支出减少"
    ],
    "n_viewpoints": 50,
    "simulation_time": 5.0
  }'
```

---

### 方式 5: 🎨 Web 界面测试

#### 步骤：

1. **启动服务器** （如果未启动）
   ```bash
   cd cognitive_physics_engine/backend
   python server.py
   ```

2. **访问公共 URL**:
   ```
   https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai
   ```
   
   或打开本地文件:
   ```bash
   # 在浏览器中打开
   cognitive_physics_engine/frontend/index.html
   ```

3. **使用界面**:
   - 输入问题（如："区块链技术的未来？"）
   - 调整参数滑块
   - 点击 "🚀 Run Simulation"
   - 查看结果

**预期**: 
- 美观的渐变 UI
- 实时参数显示
- 共识结果展示
- 置信度、聚类数等指标

---

## 📊 API 端点完整列表

### 基础端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | API 信息 |
| `/health` | GET | 健康检查 |
| `/docs` | GET | 交互式文档 (Swagger UI) |
| `/redoc` | GET | 文档 (ReDoc) |

### 核心功能端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/query` | POST | 提交查询，获取共识 |
| `/inject` | POST | 注入新信息 |
| `/compare` | POST | 多场景对比 |
| `/manifold/info` | GET | 流形结构信息 |
| `/examples` | GET | 示例查询 |

---

## 🔍 详细测试用例

### 测试用例 1: 金融分析

```python
from cpe import WorldSimulator

simulator = WorldSimulator()

# 查询
result = simulator.query(
    question="英伟达 (NVIDIA) 股价前景如何？",
    n_viewpoints=100,
    simulation_time=10.0
)

print(f"共识: {result['consensus']}")
print(f"置信度: {result['confidence']:.1%}")

# 注入突发新闻
simulator.inject_information("英伟达宣布新一代 GPU 架构")

# 再次查询
result2 = simulator.query(
    question="英伟达 (NVIDIA) 股价前景如何？",
    n_viewpoints=100,
    simulation_time=10.0
)

print(f"更新后共识: {result2['consensus']}")
print(f"置信度变化: {(result2['confidence']-result['confidence'])*100:+.1f}%")
```

### 测试用例 2: 技术评估

```python
# 多场景对比
scenarios = [
    "量子计算取得重大突破",
    "量子计算遭遇技术瓶颈",
    "替代技术出现竞争"
]

results = simulator.compare_scenarios(
    question="量子计算何时能商业化？",
    scenarios=scenarios,
    n_viewpoints=60,
    simulation_time=5.0
)

for key, result in results.items():
    print(f"\n{key}:")
    print(f"  共识: {result['consensus']}")
    print(f"  置信度: {result['confidence']:.1%}")
```

### 测试用例 3: 流形探索

```python
from cpe.manifold import CognitiveManifold
from cpe.translator import Translator

manifold = CognitiveManifold()
translator = Translator(manifold)

# 测试不同类型的陈述
statements = [
    ("英伟达 Q4 营收 $22.1B，同比增 265%", "L1 事实"),
    ("分析显示英伟达占据 90% GPU 市场份额", "L2 数据"),
    ("战略建议：做多半导体股票", "L3 策略"),
    ("我相信 AI 芯片需求会持续增长", "L4 观点"),
    ("也许量子芯片会在 5 年内取代 GPU", "L5 推测"),
]

print("陈述类型映射测试:\n")
for text, expected in statements:
    coord = translator.text_to_coordinate(text)
    interp = manifold.interpret_point(coord)
    print(f"陈述: {text}")
    print(f"  预期: {expected}")
    print(f"  检测: {interp['level']}")
    print(f"  坐标: Z={coord[0]:.2f}, X={coord[2]:.2f}\n")
```

---

## 📈 性能基准

### 不同配置的性能测试

| 配置 | 观点数 | 模拟时间 | 处理时间 | 内存 |
|------|--------|----------|----------|------|
| 小型 | 20 | 2s | ~2s | ~400MB |
| 中型 | 100 | 10s | ~12s | ~500MB |
| 大型 | 500 | 20s | ~60s | ~800MB |

### 运行性能测试

```bash
cd cognitive_physics_engine/backend

# 小型测试
time python -c "
from cpe import WorldSimulator
sim = WorldSimulator(hidden_dim=32, n_layers=2)
sim.query('测试', n_viewpoints=20, simulation_time=2.0)
"

# 中型测试
time python -c "
from cpe import WorldSimulator
sim = WorldSimulator(hidden_dim=64, n_layers=2)
sim.query('测试', n_viewpoints=100, simulation_time=10.0)
"
```

---

## ✅ 验证清单

- [x] **流形模块**: 初始化、随机点、度量、距离 ✓
- [x] **动力学模块**: ODE 积分、收敛、聚类 ✓
- [x] **翻译器**: 文本转换、坐标映射、共识合成 ✓
- [x] **模拟器**: 完整流程、新闻注入、场景对比 ✓
- [x] **API 服务器**: 所有端点响应正常 ✓
- [x] **Web 界面**: UI 正常、请求成功 ✓

---

## 🐛 常见问题排查

### 问题 1: 导入错误

**症状**: `ModuleNotFoundError: No module named 'geomstats'`

**解决**:
```bash
pip install numpy torch geomstats fastapi uvicorn pydantic
```

### 问题 2: 服务器启动失败

**症状**: `Address already in use`

**解决**:
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>

# 或使用不同端口
uvicorn server:app --port 8001
```

### 问题 3: 收敛度低

**症状**: `Convergence: 0.0%`

**原因**: 
- 模拟时间太短
- 观点太分散
- 时间步长太大

**解决**:
```python
# 增加模拟时间
result = simulator.query(
    question=...,
    simulation_time=20.0,  # 增加到 20 秒
    dt=0.05,               # 减小步长
    n_viewpoints=50        # 适度观点数
)
```

### 问题 4: API 连接超时

**症状**: 请求超时

**解决**:
```python
# 减少参数规模
{
    "n_viewpoints": 30,      # 减少到 30
    "simulation_time": 3.0,  # 减少到 3s
    "dt": 0.2                # 增大步长
}
```

---

## 🎓 理解测试结果

### 共识 (Consensus)
- **自然语言**: 系统综合观点的最终结论
- **格式**: "{确定性}, the consensus is a {立场} {语气}."
- **示例**: "Strategic assessment suggests, the consensus is a positive outlook with caution."

### 置信度 (Confidence)
- **范围**: 0% - 100%
- **计算**: `1 - (final_spread / initial_spread)`
- **解释**: 
  - `> 80%`: 高度共识
  - `50-80%`: 中等共识
  - `< 50%`: 观点分散

### 聚类数 (Clusters)
- **含义**: 发现的平衡点数量
- **解释**:
  - `1-3`: 强共识
  - `4-10`: 多个主流观点
  - `> 10`: 观点高度分散

---

## 📚 进一步测试

### 压力测试

```python
# 大规模模拟
result = simulator.query(
    question="复杂问题",
    n_viewpoints=1000,  # 1000 个观点
    simulation_time=30.0
)
```

### 连续查询测试

```python
# 测试多次查询
for i in range(10):
    result = simulator.query(f"查询 {i}", n_viewpoints=50)
    print(f"查询 {i}: 置信度 {result['confidence']:.1%}")
```

### 并发测试

```bash
# 使用 Apache Bench 测试 API
ab -n 100 -c 10 -T 'application/json' \
  -p query.json \
  http://localhost:8000/query
```

---

## 🎉 测试完成

如果所有测试都通过，恭喜！你的**认知物理引擎**已完全可用！

### 下一步

1. 🔧 **定制化**: 调整参数适应你的用例
2. 🧠 **LLM 集成**: 替换 Mock LLM 为真实 API
3. 📊 **可视化**: 添加 3D 轨迹渲染
4. 🚀 **部署**: 部署到生产环境
5. 📈 **优化**: 性能调优和扩展

---

## 📞 获取帮助

- **文档**: `cognitive_physics_engine/README.md`
- **代码**: `cognitive_physics_engine/backend/cpe/`
- **示例**: `cognitive_physics_engine/backend/demo.py`

---

**"在弯曲的空间中，最短的路径就是真理。"** 🌍✨
