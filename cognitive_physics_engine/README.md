# Cognitive Physics Engine (CPE)

## 🌍 认知物理引擎 - 在弯曲空间中计算真理

这是一个创新的原型系统，将**黎曼几何**、**神经微分方程**和**语言模型**结合，构建了一个"微缩宇宙"来模拟观点的演化和共识的形成。

### 🎯 核心概念

系统不是传统的聊天机器人或投票系统，而是一个**物理模拟器**：

1. **6D 认知流形** (Cognitive Manifold)
   - 3D 双曲空间：层级结构 (事实→观点)、领域、立场
   - 3D 欧几里得空间：意图、时间、尺度
   
2. **动力学系统** (Dynamics)
   - 观点在流形上的运动由势能场驱动
   - 真理 = 低势能点 (Nash 均衡)
   - 矛盾 = 高势能峰

3. **语义桥接** (Translator)
   - 文本 ↔ 几何坐标
   - LLM 理解语义 → 映射到数学空间

### 🏗️ 系统架构

```
cognitive_physics_engine/
├── backend/
│   ├── cpe/
│   │   ├── __init__.py
│   │   ├── manifold.py      # 6D 流形定义
│   │   ├── dynamics.py      # Neural ODE 动力学
│   │   ├── translator.py    # LLM-几何桥接
│   │   └── simulator.py     # 主引擎
│   ├── server.py            # FastAPI 服务器
│   ├── requirements.txt
│   └── tests/
└── frontend/                # React + Three.js (开发中)
```

### ⚙️ 安装和运行

#### 后端设置

```bash
cd cognitive_physics_engine/backend

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m cpe.manifold
python -m cpe.dynamics
python -m cpe.translator
python -m cpe.simulator

# 启动 API 服务器
python server.py
```

服务器将在 `http://localhost:8000` 启动。

#### API 文档

访问 `http://localhost:8000/docs` 查看交互式 API 文档。

### 🚀 使用示例

#### Python 直接调用

```python
from cpe import WorldSimulator

# 初始化模拟器
simulator = WorldSimulator(
    backend='numpy',
    hidden_dim=128,
    n_layers=3
)

# 提出问题
result = simulator.query(
    question="What is the outlook for NVIDIA stock?",
    n_viewpoints=100,
    simulation_time=10.0
)

print(f"Consensus: {result['consensus']}")
print(f"Confidence: {result['confidence']:.2%}")
```

#### REST API 调用

```bash
# 查询模拟器
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the outlook for NVIDIA stock?",
    "n_viewpoints": 100,
    "simulation_time": 10.0
  }'

# 注入新信息
curl -X POST http://localhost:8000/inject \
  -H "Content-Type: application/json" \
  -d '{
    "information": "NVIDIA announces major partnership with OpenAI"
  }'
```

### 📊 工作流程

1. **输入**：用户提问（自然语言）
2. **繁衍**：生成 N 个多样化的初始观点
3. **映射**：将观点转换为流形上的坐标
4. **演化**：在势能场作用下模拟坐标运动
5. **收敛**：观点聚集到 Nash 均衡点（真理吸引子）
6. **合成**：将最终质心转换回自然语言共识

### 🔬 技术细节

#### 流形结构

- **Z 轴 (Level)**：L1 (事实) → L5 (推测)
- **Y 轴 (Domain)**：技术、金融、政治等
- **X 轴 (Stance)**：看空 (-1) ↔ 看多 (+1)
- **W 轴 (Intent)**：阴影 (-1) ↔ 光明 (+1)
- **T 轴 (Time)**：过去 → 未来
- **S 轴 (Scale)**：微观 → 宏观

#### 动力学方程

```
dx/dt = -∇V(x)
```

其中：
- `V(x)` 是神经网络学习的势能场
- `∇V` 使用黎曼度量修正：`∇_R = g^(-1) ∇_E`

#### 认知引力

```python
gravity = exp(-2|z|) * (1 + intent_penalty)
```

- 事实层 (z≈0) 引力强
- 意图阴影区 (w<-0.5) 有排斥力

### 🎨 特性

- ✅ **白盒系统**：每个观点的轨迹都可追踪
- ✅ **几何可解释**：坐标有明确的语义含义
- ✅ **动态更新**：可实时注入新信息改变势能场
- ✅ **多场景对比**：比较不同假设下的结果
- ✅ **信心度量**：基于收敛程度计算置信度

### 📈 应用场景

1. **金融分析**：综合多方观点预测市场趋势
2. **风险评估**：评估复杂系统的潜在风险
3. **战略决策**：在多维空间中权衡不同策略
4. **舆论分析**：追踪观点演化和共识形成
5. **知识整合**：从碎片化信息中提取一致性

### 🔧 开发状态

- ✅ 后端核心引擎
- ✅ REST API 服务器
- 🚧 前端 3D 可视化（开发中）
- 🚧 真实 LLM 集成（使用 Mock）
- 🚧 高级 ODE 求解器（使用简单积分）

### 📝 引用

基于以下理论和工具：

- [Geomstats](https://geomstats.github.io/): Python 流形学习库
- PyTorch: 深度学习框架
- Neural ODEs: 连续时间动力学建模
- 黎曼几何: 弯曲空间度量理论

### 🤝 贡献

这是一个实验性项目，欢迎贡献！

### 📄 许可证

MIT License

---

**构建者注释**：这不是玩具——这是一个在数学基础上构建的认知反应堆。它用几何代替了模糊的"权重"，用物理定律代替了黑盒算法。每一个维度都有含义，每一条轨迹都可追踪，每一个结果都可解释。

*"在弯曲的空间中，最短的路径就是真理。"*
