# 基于白皮书的后端架构重新设计规范
## Backend Redesign Specification Based on Whitepaper

**Date**: 2026-02-02  
**Status**: 🚧 ARCHITECTURAL REDESIGN IN PROGRESS  
**Source**: 世界流形-微缩宇宙设计白皮书 (119KB)  
**Target**: Production-ready H³×S²×Rⁿ implementation

---

## 📋 Executive Summary

### 核心差异分析

| 维度 | 当前 v61.0 实现 | 白皮书要求 | Gap |
|------|----------------|-----------|-----|
| **流形维度** | 10D embedding (简化) | H³×S²×R⁴ (6D 物理坐标) | ⚠️ 需重构坐标系统 |
| **认知引擎** | 单阶段 tick | 4 阶段 (繁衍→坍缩→平滑→进化) | ❌ 缺少 3 个阶段 |
| **存储协议** | Markdown + YAML | H3S2Rn Protocol (6D 映射) | ⚠️ 格式需标准化 |
| **混合算力** | LLM only | Transformer + Geomstats + Neural ODE | ❌ 缺少几何与动力学 |
| **物理定律** | 基础 Langevin | η/γ/Ψ 三大定律 | ⚠️ 需实现度量场 |
| **共识机制** | 无 | PoM (Proof of Manifold) | ❌ 未实现 |

### 重构优先级

**🔴 Critical (Phase 1-2)**:
1. 核心数学层：完整的 H³×S²×R⁴ 流形几何
2. 认知引擎：4 阶段 CA Engine
3. 混合算力：集成 Geomstats + Neural ODE

**🟡 Important (Phase 3-4)**:
4. 存储协议：标准化 H3S2Rn 格式
5. 度量场：实现 η/γ/Ψ 物理定律
6. 交互界面：上下行协议与 DER

**🟢 Nice-to-have (Phase 5)**:
7. PoM 共识协议
8. 几何分片网络
9. 熵权分配系统

---

## Phase 1: 核心数学层重构

### 1.1 流形几何引擎 (Manifold Geometry Engine)

#### 当前实现问题
```python
# cognitive_physics_engine/world_os/kernel/manifold.py (v61.0)
class CognitiveManifold:
    def __init__(self):
        self.dim = 10  # 简化的 10D embedding
        self.space = ProductManifold([
            Hyperbolic(3),
            Hypersphere(2),
            Euclidean(4)
        ])
```

**问题**:
- ❌ 坐标映射不符合白皮书的 K = (Z, Y, X, W, T, S) 定义
- ❌ 缺少纤维丛（Fiber Bundle）结构
- ❌ 缺少度量场 $g_{ij}$ 的动态计算

#### 重构目标

**新架构**:
```python
# cognitive_physics_engine/world_os/kernel/manifold_v2.py

from dataclasses import dataclass
import numpy as np
from typing import Dict, Tuple
from geomstats.geometry.hyperbolic import Hyperbolic
from geomstats.geometry.hypersphere import Hypersphere
from geomstats.geometry.euclidean import Euclidean
from geomstats.geometry.product_manifold import ProductManifold

@dataclass
class H3S2RnCoordinate:
    """白皮书定义的六维全息坐标
    
    K = (Z, Y, X, W, T, S)
    - Z ∈ H³: 层级深度 (Level: L1/L3/L5)
    - Y ∈ S²: 领域方向 (Domain: Tech/Finance/...)
    - X ∈ R¹: 立场自旋 (Stance: -1 ~ +1)
    - W ∈ R¹: 意图质量 (Intent: Shadow/Daylight)
    - T ∈ R¹: 时间流 (Time: decay_rate)
    - S ∈ R¹: 观察尺度 (Scale: Micro/Meso/Macro)
    """
    # Base Space (底空间): H³ × S²
    z_hyperbolic: np.ndarray  # Shape: (3,) - Poincaré ball coordinates
    y_spherical: np.ndarray   # Shape: (2,) - θ, φ angles
    
    # Fiber Space (纤维空间): R⁴
    x_spin: float        # Stance: -1.0 (Bear) ~ +1.0 (Bull)
    w_mass: float        # Intent: negative = Shadow
    t_time: float        # Time flow parameter
    s_scale: float       # Scale: 0.0 (Micro) ~ 1.0 (Macro)
    
    # Metadata
    level: str = "L3"    # L1/L3/L5 - extracted from z_hyperbolic radius
    domain: str = "Generic"  # Extracted from y_spherical angles
    
    def to_10d_embedding(self) -> np.ndarray:
        """转换为 10D 计算坐标"""
        return np.concatenate([
            self.z_hyperbolic,  # 3D
            self.y_spherical,   # 2D
            [self.x_spin, self.w_mass, self.t_time, self.s_scale],  # 4D
            [1.0]  # Homogeneous coordinate
        ])
    
    @classmethod
    def from_10d_embedding(cls, coords: np.ndarray) -> 'H3S2RnCoordinate':
        """从 10D 向量重构六维坐标"""
        return cls(
            z_hyperbolic=coords[0:3],
            y_spherical=coords[3:5],
            x_spin=coords[5],
            w_mass=coords[6],
            t_time=coords[7],
            s_scale=coords[8]
        )


class CognitiveManifoldV2:
    """白皮书定义的完整流形结构
    
    M = H³ × S² × R⁴
    - Base Space: H³ × S² (position in knowledge space)
    - Fiber Space: R⁴ (attributes: X/W/T/S)
    - Metric Tensor: g_ij(x) - dynamic, state-dependent
    """
    
    def __init__(self):
        # 1. 定义流形结构
        self.h3 = Hyperbolic(dim=3, coords_type='ball')  # Poincaré ball
        self.s2 = Hypersphere(dim=2)
        self.r4 = Euclidean(dim=4)
        
        self.base_space = ProductManifold([self.h3, self.s2])
        self.full_manifold = ProductManifold([self.h3, self.s2, self.r4])
        
        # 2. 度量场参数 (Metric Field Parameters)
        # 由 η/γ/Ψ 物理定律动态调整
        self.metric_params = {
            'eta_friction': 0.5,    # RpX 效率因子
            'gamma_curvature': 1.0, # 机制因子
            'psi_expansion': 0.0    # 演化势能
        }
        
    def encode_state(
        self,
        level: int,  # 1, 3, or 5
        domain: str,
        stance: float,
        intent: float,
        time: float,
        scale: float
    ) -> H3S2RnCoordinate:
        """将语义状态编码为流形坐标
        
        白皮书 3.1 节：层级映射逻辑
        - L5 (Strategy): r → 0 (球心)
        - L3 (Logic): 0 < r < 0.8
        - L1 (Fact): r → 1 (边缘)
        """
        # Z-Axis: 层级 → 双曲半径
        r = self._level_to_hyperbolic_radius(level)
        # 随机方向（或基于 domain hash）
        theta_h, phi_h = self._hash_domain_to_angles(domain, 'hyperbolic')
        z_coords = self._spherical_to_poincare(r, theta_h, phi_h)
        
        # Y-Axis: 领域 → 球面角度
        theta_s, phi_s = self._hash_domain_to_angles(domain, 'spherical')
        y_coords = np.array([theta_s, phi_s])
        
        return H3S2RnCoordinate(
            z_hyperbolic=z_coords,
            y_spherical=y_coords,
            x_spin=stance,
            w_mass=intent,
            t_time=time,
            s_scale=scale,
            level=f"L{level}",
            domain=domain
        )
    
    def compute_metric_tensor(
        self,
        point: H3S2RnCoordinate,
        world_state: Dict
    ) -> np.ndarray:
        """计算给定点的度量张量 g_ij
        
        白皮书 3.7 节：统一场方程
        ds² = (1/η) dx²_L1 + exp(-γ) dx²_W - Ψ dt²
        """
        # 基础度量 (从流形几何)
        g_base = self.full_manifold.metric.metric_matrix(
            point.to_10d_embedding()
        )
        
        # 物理修正 (基于 η/γ/Ψ)
        eta = self._compute_eta(point, world_state)
        gamma = self._compute_gamma(point, world_state)
        psi = self._compute_psi(point, world_state)
        
        # 调整度量张量 (简化版本)
        g_modified = g_base.copy()
        
        # L1 摩擦: 1/η 放大 Z 方向的距离
        g_modified[0:3, 0:3] *= (1.0 / (eta + 1e-6))
        
        # W 轴引力: exp(-γ) 调整 Intent 维度
        g_modified[6, 6] *= np.exp(-gamma)
        
        # T 轴时间膨胀: -Ψ (闵可夫斯基符号)
        g_modified[7, 7] *= -psi
        
        return g_modified
    
    def geodesic(
        self,
        start: H3S2RnCoordinate,
        end: H3S2RnCoordinate,
        n_steps: int = 50
    ) -> np.ndarray:
        """计算测地线 (Geodesic Path)
        
        白皮书 3.3 节：最小作用量原理
        """
        start_coords = start.to_10d_embedding()
        end_coords = end.to_10d_embedding()
        
        # 使用 Geomstats 计算测地线
        path = self.full_manifold.metric.geodesic(
            initial_point=start_coords,
            end_point=end_coords
        )
        
        # 离散化
        t_values = np.linspace(0, 1, n_steps)
        trajectory = np.array([path(t) for t in t_values])
        
        return trajectory
    
    def compute_action_functional(
        self,
        trajectory: np.ndarray,
        world_state: Dict
    ) -> float:
        """计算作用量泛函 S = ∫L dt
        
        白皮书 4.2 节：用于 PoM 共识验证
        L = (1/2) g_ij ż^i ż^j - V(z)
        """
        action = 0.0
        dt = 1.0 / len(trajectory)
        
        for i in range(len(trajectory) - 1):
            point = H3S2RnCoordinate.from_10d_embedding(trajectory[i])
            velocity = (trajectory[i+1] - trajectory[i]) / dt
            
            # 动能: (1/2) g_ij ż^i ż^j
            g_ij = self.compute_metric_tensor(point, world_state)
            kinetic = 0.5 * velocity.T @ g_ij @ velocity
            
            # 势能: V(z) - 由势能场定义
            potential = self._compute_potential(point, world_state)
            
            # 拉格朗日量: L = T - V
            lagrangian = kinetic - potential
            action += lagrangian * dt
        
        return action
    
    # === 辅助方法 ===
    
    def _level_to_hyperbolic_radius(self, level: int) -> float:
        """层级映射: L5→0, L3→0.5, L1→0.95"""
        mapping = {1: 0.95, 3: 0.5, 5: 0.05}
        return mapping.get(level, 0.5)
    
    def _hash_domain_to_angles(
        self,
        domain: str,
        space_type: str
    ) -> Tuple[float, float]:
        """领域哈希到角度坐标"""
        # 简化版本：使用字符串哈希
        hash_val = hash(domain) % 360
        theta = np.radians(hash_val)
        phi = np.radians((hash_val * 137) % 180)  # Golden angle
        return theta, phi
    
    def _spherical_to_poincare(
        self,
        r: float,
        theta: float,
        phi: float
    ) -> np.ndarray:
        """球坐标 → Poincaré 球坐标"""
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return np.array([x, y, z])
    
    def _compute_eta(
        self,
        point: H3S2RnCoordinate,
        world_state: Dict
    ) -> float:
        """计算效率因子 η = Output/Input
        
        白皮书 3.7.1: RpX 刚度模量
        """
        # TODO: 从 world_state 查询该点的历史数据
        return self.metric_params['eta_friction']
    
    def _compute_gamma(
        self,
        point: H3S2RnCoordinate,
        world_state: Dict
    ) -> float:
        """计算机制因子 γ = Cost_violation/Benefit_violation
        
        白皮书 3.7.2: 引力奇点
        """
        # 阴影检测: W < 0 时 γ 降低
        if point.w_mass < 0:
            return max(0.1, self.metric_params['gamma_curvature'] + point.w_mass)
        return self.metric_params['gamma_curvature']
    
    def _compute_psi(
        self,
        point: H3S2RnCoordinate,
        world_state: Dict
    ) -> float:
        """计算演化势能 Ψ = ∫P(s)·Payoff(s) ds
        
        白皮书 3.7.3: 时空相对论
        """
        # TODO: 基于领域趋势计算
        return self.metric_params['psi_expansion']
    
    def _compute_potential(
        self,
        point: H3S2RnCoordinate,
        world_state: Dict
    ) -> float:
        """计算势能场 V(z)
        
        白皮书 3.2.3: W 轴引力井
        """
        # 阴影引力: W < 0 时产生深井
        if point.w_mass < -0.5:
            return -10.0 * abs(point.w_mass)  # 强引力
        return 0.0
```

### 1.2 集成计划

**文件结构**:
```
cognitive_physics_engine/world_os/kernel/
├── manifold.py              # 保留 v61.0 (向后兼容)
├── manifold_v2.py           # 新实现 ✅
├── coordinates.py           # H3S2RnCoordinate 工具类
├── metric_field.py          # 度量场计算
├── geodesic_solver.py       # 测地线求解器
└── tests/
    ├── test_manifold_v2.py
    └── test_coordinates.py
```

**测试用例**:
```python
# cognitive_physics_engine/world_os/kernel/tests/test_manifold_v2.py

def test_coordinate_encoding():
    """测试语义→流形坐标编码"""
    manifold = CognitiveManifoldV2()
    
    coord = manifold.encode_state(
        level=5,
        domain="Tech",
        stance=0.8,
        intent=0.0,
        time=0.5,
        scale=0.7
    )
    
    assert coord.level == "L5"
    assert coord.domain == "Tech"
    assert 0.0 <= np.linalg.norm(coord.z_hyperbolic) <= 0.1  # 接近球心
    assert -1.0 <= coord.x_spin <= 1.0

def test_geodesic_computation():
    """测试测地线计算"""
    manifold = CognitiveManifoldV2()
    
    start = manifold.encode_state(1, "Tech", 0.5, 0.0, 0.0, 0.0)
    end = manifold.encode_state(5, "Tech", 0.5, 0.0, 1.0, 1.0)
    
    trajectory = manifold.geodesic(start, end, n_steps=50)
    
    assert trajectory.shape == (50, 10)
    # 验证连续性
    distances = np.linalg.norm(np.diff(trajectory, axis=0), axis=1)
    assert np.all(distances < 0.5)  # 连续路径

def test_action_functional():
    """测试作用量计算 (用于 PoM)"""
    manifold = CognitiveManifoldV2()
    
    start = manifold.encode_state(1, "Tech", 0.5, 0.0, 0.0, 0.0)
    end = manifold.encode_state(1, "Tech", 0.5, 0.0, 0.1, 0.0)
    
    trajectory = manifold.geodesic(start, end)
    action = manifold.compute_action_functional(trajectory, world_state={})
    
    assert action < 100.0  # 合理的物理能量
```

---

## Phase 2: 认知引擎重构 (CA Engine)

### 2.1 当前架构问题

**现有实现 (v61.0)**:
```python
# world_os/engine.py
def tick(self, entity_id, context, llm_intervention):
    # 1. 读取状态
    state = self.db.read_entity(entity_id)
    
    # 2. 单阶段演化 (简化)
    new_coords = self.physics.evolve(state['coordinates'])
    
    # 3. LLM 可选干预
    if llm_intervention:
        decision = self.llm.decide(context)
    
    # 4. 写回
    self.db.write_entity(entity_id, new_state)
```

**问题**:
- ❌ 缺少白皮书定义的 4 个阶段
- ❌ 没有混合算力（Transformer + Geomstats + Neural ODE）
- ❌ 没有认知坍缩机制
- ❌ 没有时序平滑
- ❌ 没有递归进化

### 2.2 重构架构

**新架构 (4-Phase CA Engine)**:

```python
# cognitive_physics_engine/world_os/brain/ca_engine.py

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import numpy as np
from enum import Enum

class PhaseStatus(Enum):
    """CA 引擎阶段状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Narrative:
    """剧本数据结构
    
    白皮书 4.1 节：全息繁衍的输出
    """
    narrative_id: str
    coordinates: 'H3S2RnCoordinate'
    content: str
    
    # 混合算力来源
    llm_confidence: float       # Transformer 语义得分
    geometric_feasibility: float  # Geomstats 几何得分
    dynamic_energy: float       # Neural ODE 动力学得分
    
    # 物理属性
    mass: float = 1.0           # 惯性质量
    velocity: np.ndarray = None # 动量
    is_alive: bool = True       # 存活状态

@dataclass
class CAEngineResult:
    """CA 引擎执行结果"""
    phase_1_narratives: List[Narrative]  # 繁衍出的候选剧本
    phase_2_survivor: Optional[Narrative]  # 坍缩后的幸存者
    phase_3_smoothed: Optional[Narrative]  # 平滑后的状态
    phase_4_updated_params: Dict         # 进化后的参数
    
    execution_time: Dict[str, float]
    success: bool
    error_message: str = ""


class CognitiveAlphaEngine:
    """认知阿尔法引擎 (4-Phase Architecture)
    
    白皮书第四章：Engine 核心
    
    Phase I:   全息繁衍 (Holographic Propagation)
    Phase II:  认知坍缩 (Cognitive Collapse / CCP)
    Phase III: 时序平滑 (Temporal Smoothing)
    Phase IV:  递归进化 (Recursive Evolution)
    """
    
    def __init__(
        self,
        manifold: 'CognitiveManifoldV2',
        llm_agent: 'LLMAgent',
        ode_solver: 'NeuralODESolver',
        markdown_db: 'MarkdownDB'
    ):
        self.manifold = manifold
        self.llm = llm_agent
        self.ode = ode_solver
        self.db = markdown_db
        
        # 演化参数 (Phase IV 会动态调整)
        self.meta_params = {
            'propagation_count': 10,  # 繁衍数量
            'collapse_threshold': 0.5, # 坍缩阈值
            'smoothing_momentum': 0.9, # 平滑动量
            'evolution_lr': 0.01       # 学习率
        }
        
        # 历史记录 (用于 Phase IV)
        self.history = {
            'corpses': [],      # 死亡的剧本
            'residuals': [],    # 预测残差
            'performance': []   # 性能指标
        }
    
    def run(
        self,
        seed: 'H3S2RnCoordinate',
        context: Dict,
        full_cycle: bool = True
    ) -> CAEngineResult:
        """执行完整的 CA 循环
        
        Args:
            seed: 初始种子坐标
            context: 上下文信息
            full_cycle: 是否执行完整 4 阶段 (否则仅 Phase I-II)
        """
        import time
        timing = {}
        
        try:
            # Phase I: 全息繁衍
            t0 = time.time()
            narratives = self.phase_1_propagation(seed, context)
            timing['phase_1'] = time.time() - t0
            
            # Phase II: 认知坍缩
            t0 = time.time()
            survivor = self.phase_2_collapse(narratives, context)
            timing['phase_2'] = time.time() - t0
            
            if not full_cycle:
                return CAEngineResult(
                    phase_1_narratives=narratives,
                    phase_2_survivor=survivor,
                    phase_3_smoothed=None,
                    phase_4_updated_params={},
                    execution_time=timing,
                    success=True
                )
            
            # Phase III: 时序平滑
            t0 = time.time()
            smoothed = self.phase_3_smoothing(survivor, context)
            timing['phase_3'] = time.time() - t0
            
            # Phase IV: 递归进化
            t0 = time.time()
            updated_params = self.phase_4_evolution(narratives, survivor, context)
            timing['phase_4'] = time.time() - t0
            
            return CAEngineResult(
                phase_1_narratives=narratives,
                phase_2_survivor=survivor,
                phase_3_smoothed=smoothed,
                phase_4_updated_params=updated_params,
                execution_time=timing,
                success=True
            )
            
        except Exception as e:
            return CAEngineResult(
                phase_1_narratives=[],
                phase_2_survivor=None,
                phase_3_smoothed=None,
                phase_4_updated_params={},
                execution_time=timing,
                success=False,
                error_message=str(e)
            )
    
    # ========================================
    # Phase I: 全息繁衍 (Holographic Propagation)
    # ========================================
    
    def phase_1_propagation(
        self,
        seed: 'H3S2RnCoordinate',
        context: Dict
    ) -> List[Narrative]:
        """六维全息繁衍
        
        白皮书 4.1 节：混合算力矩阵
        - Transformer: 生成语义假设
        - Geomstats: 验证几何约束
        - Neural ODE: 模拟时间演化
        """
        narratives = []
        
        # Dimension 1: Z-Axis (垂直全息 - 层级推演)
        z_narratives = self._propagate_z_axis(seed, context)
        narratives.extend(z_narratives)
        
        # Dimension 2: Y-Axis (跨域共振 - 领域映射)
        y_narratives = self._propagate_y_axis(seed, context)
        narratives.extend(y_narratives)
        
        # Dimension 3: X-Axis (二元纠缠 - 正反对立)
        x_narratives = self._propagate_x_axis(seed, context)
        narratives.extend(x_narratives)
        
        # Dimension 4: W-Axis (阴影层析 - 意图反推)
        w_narratives = self._propagate_w_axis(seed, context)
        narratives.extend(w_narratives)
        
        # Dimension 5: S-Axis (多尺度重整 - 粗粒化)
        s_narratives = self._propagate_s_axis(seed, context)
        narratives.extend(s_narratives)
        
        # Dimension 6: T-Axis (遍历性演化 - 时间光锥)
        t_narratives = self._propagate_t_axis(seed, context)
        narratives.extend(t_narratives)
        
        return narratives
    
    def _propagate_z_axis(
        self,
        seed: 'H3S2RnCoordinate',
        context: Dict
    ) -> List[Narrative]:
        """Z轴繁衍：分形重构 (Fractal Reconstruction)
        
        从 L1 碎片重构 L5 全貌，反向填充 L1 细节
        """
        narratives = []
        
        # LLM: 语义补全
        if seed.level == "L1":
            prompt = f"""
            Given L1 fact: {context.get('seed_text')}
            
            Infer the L5 strategy that explains this fact.
            Generate 3 hypotheses in JSON format:
            [{{"strategy": "...", "confidence": 0.8}}, ...]
            """
            llm_output = self.llm.generate(prompt)
            hypotheses = self._parse_json(llm_output)
            
            for hyp in hypotheses:
                # Geomstats: 几何约束
                l5_coord = self.manifold.encode_state(
                    level=5,
                    domain=seed.domain,
                    stance=seed.x_spin,
                    intent=seed.w_mass,
                    time=seed.t_time,
                    scale=1.0  # Macro
                )
                
                # 验证 L5 → L1 是否几何连通
                path = self.manifold.geodesic(l5_coord, seed, n_steps=20)
                feasibility = self._check_path_smoothness(path)
                
                # Neural ODE: 动力验证
                dynamics_score = self.ode.verify_causality(l5_coord, seed)
                
                narratives.append(Narrative(
                    narrative_id=f"z_l5_{len(narratives)}",
                    coordinates=l5_coord,
                    content=hyp['strategy'],
                    llm_confidence=hyp['confidence'],
                    geometric_feasibility=feasibility,
                    dynamic_energy=dynamics_score
                ))
        
        return narratives
    
    def _propagate_y_axis(
        self,
        seed: 'H3S2RnCoordinate',
        context: Dict
    ) -> List[Narrative]:
        """Y轴繁衍：同胚映射 (Homeomorphic Mapping)
        
        跨领域寻找拓扑同构体
        """
        narratives = []
        
        # LLM: 隐喻检索
        prompt = f"""
        Event: {context.get('seed_text')} in domain {seed.domain}
        
        Find analogies in other domains (Biology, History, Physics).
        Return JSON: [{{"domain": "Biology", "analogy": "...", "similarity": 0.9}}, ...]
        """
        llm_output = self.llm.generate(prompt)
        analogies = self._parse_json(llm_output)
        
        for analogy in analogies:
            # Geomstats: 拓扑对齐
            target_coord = self.manifold.encode_state(
                level=int(seed.level[1]),  # 保持层级
                domain=analogy['domain'],
                stance=seed.x_spin,
                intent=seed.w_mass,
                time=seed.t_time,
                scale=seed.s_scale
            )
            
            # 计算结构相似度 (简化版: 球面距离)
            structural_similarity = self._compute_s2_distance(
                seed.y_spherical,
                target_coord.y_spherical
            )
            
            narratives.append(Narrative(
                narrative_id=f"y_cross_{len(narratives)}",
                coordinates=target_coord,
                content=analogy['analogy'],
                llm_confidence=analogy['similarity'],
                geometric_feasibility=structural_similarity,
                dynamic_energy=0.5  # 中性
            ))
        
        return narratives
    
    def _propagate_x_axis(
        self,
        seed: 'H3S2RnCoordinate',
        context: Dict
    ) -> List[Narrative]:
        """X轴繁衍：对称性破缺 (Symmetry Breaking)
        
        强制生成正反两面的纠缠剧本
        """
        narratives = []
        
        # LLM: 反事实生成
        prompt_bull = f"""
        {context.get('seed_text')}
        
        Generate a BULLISH narrative. Why is this positive?
        """
        prompt_bear = f"""
        {context.get('seed_text')}
        
        Generate a BEARISH narrative. Why is this negative?
        """
        
        bull_text = self.llm.generate(prompt_bull)
        bear_text = self.llm.generate(prompt_bear)
        
        # Geomstats: 确保正交
        bull_coord = seed.copy()
        bull_coord.x_spin = abs(seed.x_spin)  # 正自旋
        
        bear_coord = seed.copy()
        bear_coord.x_spin = -abs(seed.x_spin)  # 负自旋
        
        angle = self._compute_x_angle(bull_coord, bear_coord)
        orthogonality = abs(angle - 90.0) / 90.0  # 接近90度越好
        
        # Neural ODE: 博弈演化
        collision_result = self.ode.simulate_collision(bull_coord, bear_coord)
        
        narratives.extend([
            Narrative(
                narrative_id="x_bull",
                coordinates=bull_coord,
                content=bull_text,
                llm_confidence=0.7,
                geometric_feasibility=orthogonality,
                dynamic_energy=collision_result['bull_energy']
            ),
            Narrative(
                narrative_id="x_bear",
                coordinates=bear_coord,
                content=bear_text,
                llm_confidence=0.7,
                geometric_feasibility=orthogonality,
                dynamic_energy=collision_result['bear_energy']
            )
        ])
        
        return narratives
    
    def _propagate_w_axis(
        self,
        seed: 'H3S2RnCoordinate',
        context: Dict
    ) -> List[Narrative]:
        """W轴繁衍：引力透镜 (Gravitational Lensing)
        
        基于轨迹偏转反推暗物质质量
        """
        narratives = []
        
        # LLM: 阴谋剧本生成
        prompt = f"""
        {context.get('seed_text')}
        
        Hidden Agenda Analysis:
        - Who benefits if this is a scam?
        - What incentives would explain anomalies?
        
        Return JSON: {{"daylight": "...", "shadow": "...", "shadow_probability": 0.3}}
        """
        llm_output = self.llm.generate(prompt)
        analysis = self._parse_json(llm_output)
        
        # Geomstats: 曲率反演
        # 检测历史轨迹是否有异常弯曲
        historical_trajectory = self.db.get_trajectory(context['entity_id'])
        if historical_trajectory is not None:
            curvature_anomaly = self._detect_anomaly(historical_trajectory)
            
            # 反算 W 轴质量
            inferred_w = self._infer_w_mass(curvature_anomaly)
            
            shadow_coord = seed.copy()
            shadow_coord.w_mass = inferred_w
            
            narratives.append(Narrative(
                narrative_id="w_shadow",
                coordinates=shadow_coord,
                content=analysis.get('shadow', ''),
                llm_confidence=analysis.get('shadow_probability', 0.0),
                geometric_feasibility=curvature_anomaly,
                dynamic_energy=-abs(inferred_w)  # 负能量 = 陷阱
            ))
        
        return narratives
    
    def _propagate_s_axis(
        self,
        seed: 'H3S2RnCoordinate',
        context: Dict
    ) -> List[Narrative]:
        """S轴繁衍：多尺度重整 (Multi-Scale Renormalization)
        
        在微观和宏观两个尺度独立建模
        """
        narratives = []
        
        # Geomstats: RG 流
        # 微观视图: S → 0
        micro_coord = seed.copy()
        micro_coord.s_scale = 0.1
        micro_text = self.llm.generate(f"Micro-analysis of {context['seed_text']}")
        
        # 宏观视图: S → 1
        macro_coord = seed.copy()
        macro_coord.s_scale = 0.9
        macro_text = self.llm.generate(f"Macro-analysis of {context['seed_text']}")
        
        # Neural ODE: 双频动力学
        micro_dynamics = self.ode.fit_fast_variable(micro_coord)
        macro_dynamics = self.ode.fit_slow_variable(macro_coord)
        
        narratives.extend([
            Narrative(
                narrative_id="s_micro",
                coordinates=micro_coord,
                content=micro_text,
                llm_confidence=0.6,
                geometric_feasibility=1.0,
                dynamic_energy=micro_dynamics
            ),
            Narrative(
                narrative_id="s_macro",
                coordinates=macro_coord,
                content=macro_text,
                llm_confidence=0.6,
                geometric_feasibility=1.0,
                dynamic_energy=macro_dynamics
            )
        ])
        
        return narratives
    
    def _propagate_t_axis(
        self,
        seed: 'H3S2RnCoordinate',
        context: Dict
    ) -> List[Narrative]:
        """T轴繁衍：路径积分 (Path Integral)
        
        蒙特卡洛生成未来光锥
        """
        narratives = []
        
        # Neural ODE: 蒙特卡洛系综
        future_samples = self.ode.monte_carlo_ensemble(
            seed,
            n_samples=5,
            t_horizon=10.0
        )
        
        for i, sample in enumerate(future_samples):
            # LLM: 情景描述
            scenario_text = self.llm.generate(
                f"Describe the world state at coordinates {sample}"
            )
            
            narratives.append(Narrative(
                narrative_id=f"t_future_{i}",
                coordinates=sample,
                content=scenario_text,
                llm_confidence=0.5,
                geometric_feasibility=0.8,
                dynamic_energy=self._compute_trajectory_energy(seed, sample)
            ))
        
        return narratives
    
    # ========================================
    # Phase II: 认知坍缩 (Cognitive Collapse)
    # ========================================
    
    def phase_2_collapse(
        self,
        narratives: List[Narrative],
        context: Dict
    ) -> Optional[Narrative]:
        """三重清洗：物理、机制、逻辑
        
        白皮书 4.2 节：大逃杀
        """
        if not narratives:
            return None
        
        # Loop 1: 物理清洗 (热寂)
        survivors_1 = self._loop_1_physics_filter(narratives, context)
        print(f"[Collapse] Phase 1: {len(narratives)} → {len(survivors_1)}")
        
        # Loop 2: 机制清洗 (内爆)
        survivors_2 = self._loop_2_governance_filter(survivors_1, context)
        print(f"[Collapse] Phase 2: {len(survivors_1)} → {len(survivors_2)}")
        
        # Loop 3: 逻辑清洗 (湮灭)
        winner = self._loop_3_logic_filter(survivors_2, context)
        print(f"[Collapse] Phase 3: {len(survivors_2)} → {'1' if winner else '0'}")
        
        # 记录尸体 (Phase IV 使用)
        corpses = [n for n in narratives if not n.is_alive]
        self.history['corpses'].extend(corpses)
        
        return winner
    
    def _loop_1_physics_filter(
        self,
        narratives: List[Narrative],
        context: Dict
    ) -> List[Narrative]:
        """物理清洗：能量耗散检测
        
        剧本是否能在环境摩擦下存活？
        """
        survivors = []
        world_state = self.db.get_world_state()
        
        for narrative in narratives:
            # Geomstats: 计算路径能量消耗
            # 假设目标是 context['target']
            if 'target' in context:
                target = context['target']
                path = self.manifold.geodesic(
                    narrative.coordinates,
                    target,
                    n_steps=50
                )
                action = self.manifold.compute_action_functional(path, world_state)
                
                # 判据: action < threshold
                if action < 50.0:  # TODO: 动态阈值
                    narrative.dynamic_energy = action
                    survivors.append(narrative)
                else:
                    narrative.is_alive = False
                    narrative.death_reason = "EXHAUSTION"
            else:
                survivors.append(narrative)
        
        return survivors
    
    def _loop_2_governance_filter(
        self,
        narratives: List[Narrative],
        context: Dict
    ) -> List[Narrative]:
        """机制清洗：潮汐力撕裂检测
        
        剧本是否因内部张力过大而解体？
        """
        survivors = []
        
        for narrative in narratives:
            # LLM: 生成 Shadow 人格
            shadow_prompt = f"""
            {narrative.content}
            
            Devil's Advocate: If this is a scam, what would the exit strategy be?
            """
            shadow_text = self.llm.generate(shadow_prompt)
            
            # Geomstats: 计算张力
            daylight_vector = narrative.coordinates.to_10d_embedding()
            
            # 构建 shadow 坐标 (W轴负移)
            shadow_coord = narrative.coordinates.copy()
            shadow_coord.w_mass = -abs(shadow_coord.w_mass) - 0.5
            shadow_vector = shadow_coord.to_10d_embedding()
            
            # 张量发散度
            divergence = np.linalg.norm(daylight_vector - shadow_vector)
            
            # 判据: divergence < γ_critical
            gamma = self.manifold._compute_gamma(narrative.coordinates, {})
            if divergence < gamma * 5.0:  # 可承受范围
                survivors.append(narrative)
            else:
                narrative.is_alive = False
                narrative.death_reason = "IMPLOSION"
        
        return survivors
    
    def _loop_3_logic_filter(
        self,
        narratives: List[Narrative],
        context: Dict
    ) -> Optional[Narrative]:
        """逻辑清洗：粒子对撞
        
        Bull vs Bear，谁的动量更大？
        """
        if len(narratives) == 0:
            return None
        if len(narratives) == 1:
            return narratives[0]
        
        # 两两对抗，锦标赛
        while len(narratives) > 1:
            a = narratives.pop(0)
            b = narratives.pop(0)
            
            # Geomstats: 计算动量
            mass_a = a.mass
            velocity_a = np.array([a.coordinates.x_spin, a.coordinates.w_mass])
            momentum_a = mass_a * np.linalg.norm(velocity_a)
            
            mass_b = b.mass
            velocity_b = np.array([b.coordinates.x_spin, b.coordinates.w_mass])
            momentum_b = mass_b * np.linalg.norm(velocity_b)
            
            # 碰撞判决
            if momentum_a > momentum_b:
                winner = a
                loser = b
            else:
                winner = b
                loser = a
            
            loser.is_alive = False
            loser.death_reason = "ANNIHILATION"
            
            # 吸收部分动量
            winner.mass += 0.1 * loser.mass
            
            narratives.append(winner)
        
        return narratives[0] if narratives else None
    
    # ========================================
    # Phase III: 时序平滑 (Temporal Smoothing)
    # ========================================
    
    def phase_3_smoothing(
        self,
        survivor: Optional[Narrative],
        context: Dict
    ) -> Optional[Narrative]:
        """惯性推演：抵抗噪音
        
        白皮书 4.3 节：哈密顿流
        """
        if survivor is None:
            return None
        
        # Loop 1: 质量赋予
        survivor.mass = self._assign_mass(survivor, context)
        
        # Loop 2: 动量维持 (平行移动)
        historical_trajectory = self.db.get_trajectory(context['entity_id'])
        if historical_trajectory is not None and len(historical_trajectory) > 1:
            # 计算历史动量
            prev_coord = H3S2RnCoordinate.from_10d_embedding(historical_trajectory[-2])
            curr_coord = survivor.coordinates
            
            velocity = curr_coord.to_10d_embedding() - prev_coord.to_10d_embedding()
            
            # Geomstats: 协变导数 (简化版: 指数映射)
            momentum_factor = self.meta_params['smoothing_momentum']
            inertial_position = curr_coord.to_10d_embedding() + momentum_factor * velocity
            
            survivor.coordinates = H3S2RnCoordinate.from_10d_embedding(inertial_position)
        
        # Loop 3: 变轨判定
        if self._should_change_orbit(survivor, context):
            print("[Smoothing] Orbit change detected!")
            survivor = self._execute_orbit_change(survivor, context)
        
        return survivor
    
    def _assign_mass(self, narrative: Narrative, context: Dict) -> float:
        """历史积分计算质量
        
        存活时间越长，L1证据越多，质量越大
        """
        entity_history = self.db.get_entity_history(context['entity_id'])
        
        # 验证次数
        verification_count = len([
            h for h in entity_history
            if h['status'] == 'verified'
        ])
        
        # 时间衰减
        lambda_decay = 0.001
        total_mass = 1.0
        
        for record in entity_history:
            age_days = (time.time() - record['timestamp']) / 86400
            weight = np.exp(-lambda_decay * age_days)
            total_mass += weight
        
        return min(total_mass, 10000.0)  # 上限
    
    def _should_change_orbit(self, narrative: Narrative, context: Dict) -> bool:
        """逃逸速度判定"""
        # 检测能量冲击
        recent_events = context.get('recent_events', [])
        
        for event in recent_events:
            if event['type'] == 'regulatory' and event['severity'] > 0.8:
                # L5 级别法律重构
                return True
        
        return False
    
    def _execute_orbit_change(
        self,
        narrative: Narrative,
        context: Dict
    ) -> Narrative:
        """范式转移"""
        # LLM: 重写整个叙事
        new_narrative_text = self.llm.generate(f"""
        Paradigm shift detected: {context['shift_reason']}
        
        Rewrite the entire worldview for {context['entity_id']}.
        """)
        
        narrative.content = new_narrative_text
        
        # 切换动力学方程
        # TODO: 从 growth 切换到 decay
        
        return narrative
    
    # ========================================
    # Phase IV: 递归进化 (Recursive Evolution)
    # ========================================
    
    def phase_4_evolution(
        self,
        all_narratives: List[Narrative],
        survivor: Optional[Narrative],
        context: Dict
    ) -> Dict:
        """三层元学习环
        
        白皮书 4.4 节：反向传播
        """
        updated_params = {}
        
        # Loop 1: 语义修正 (Transformer 自优化)
        semantic_update = self._loop_1_semantic_correction(all_narratives)
        updated_params['semantic'] = semantic_update
        
        # Loop 2: 几何修正 (Geomstats 参数调优)
        geometric_update = self._loop_2_geometric_correction(all_narratives, survivor)
        updated_params['geometric'] = geometric_update
        
        # Loop 3: 动力修正 (Neural ODE 拟合新规律)
        dynamic_update = self._loop_3_dynamic_correction(survivor, context)
        updated_params['dynamic'] = dynamic_update
        
        # 应用更新
        self.meta_params.update(updated_params)
        
        return updated_params
    
    def _loop_1_semantic_correction(
        self,
        narratives: List[Narrative]
    ) -> Dict:
        """基于死亡信号优化 Prompt"""
        corpses = [n for n in narratives if not n.is_alive]
        
        if len(corpses) == 0:
            return {}
        
        # 统计死因
        death_reasons = {}
        for corpse in corpses:
            reason = corpse.death_reason
            death_reasons[reason] = death_reasons.get(reason, 0) + 1
        
        # 如果大量死于 EXHAUSTION，说明生成器偏好重资产
        if death_reasons.get('EXHAUSTION', 0) > len(corpses) * 0.8:
            # LLM: 元认知反射
            constraint = self.llm.generate("""
            System analysis: 85% of narratives died from energy exhaustion.
            
            Generate a prompt constraint to prevent heavy-asset models.
            Format: "CONSTRAINT: <rule>"
            """)
            
            # 写入系统提示
            self.db.write_system_prompt('generator_rules', constraint)
            
            return {'constraint_added': constraint}
        
        return {}
    
    def _loop_2_geometric_correction(
        self,
        narratives: List[Narrative],
        survivor: Optional[Narrative]
    ) -> Dict:
        """黎曼梯度下降校准度量"""
        # 检测预测误差
        if survivor is None:
            return {}
        
        predicted_energy = survivor.dynamic_energy
        real_energy = self._get_real_world_outcome()  # TODO: 实现
        
        if real_energy is None:
            return {}
        
        error = (predicted_energy - real_energy) ** 2
        
        # 梯度下降 (简化版)
        if error > 1.0:
            # 如果低估了摩擦，增加 eta
            if predicted_energy < real_energy:
                self.manifold.metric_params['eta_friction'] *= 1.1
            else:
                self.manifold.metric_params['eta_friction'] *= 0.9
            
            return {'eta_adjusted': self.manifold.metric_params['eta_friction']}
        
        return {}
    
    def _loop_3_dynamic_correction(
        self,
        survivor: Optional[Narrative],
        context: Dict
    ) -> Dict:
        """Neural ODE 在线学习"""
        # 收集历史轨迹
        trajectory = self.db.get_trajectory(context['entity_id'])
        
        if trajectory is None or len(trajectory) < 10:
            return {}
        
        # Neural ODE: 拟合新的演化方程
        self.ode.fit_online(trajectory)
        
        return {'ode_updated': True}
    
    # ========================================
    # 辅助方法
    # ========================================
    
    def _parse_json(self, text: str) -> Dict:
        """从 LLM 输出提取 JSON"""
        import json
        import re
        
        # 尝试提取 JSON block
        match = re.search(r'```json\s*(\[.*?\])\s*```', text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        
        # 尝试直接解析
        try:
            return json.loads(text)
        except:
            return {}
    
    def _check_path_smoothness(self, path: np.ndarray) -> float:
        """检查路径连续性"""
        if len(path) < 2:
            return 0.0
        
        distances = np.linalg.norm(np.diff(path, axis=0), axis=1)
        smoothness = 1.0 / (1.0 + np.var(distances))
        return smoothness
    
    def _compute_s2_distance(self, y1: np.ndarray, y2: np.ndarray) -> float:
        """球面测地距离"""
        from geomstats.geometry.hypersphere import Hypersphere
        s2 = Hypersphere(dim=2)
        # 转换为 3D 笛卡尔坐标
        p1 = self._spherical_to_cartesian(y1)
        p2 = self._spherical_to_cartesian(y2)
        distance = s2.metric.dist(p1, p2)
        return float(distance)
    
    def _spherical_to_cartesian(self, angles: np.ndarray) -> np.ndarray:
        """球坐标 → 笛卡尔坐标"""
        theta, phi = angles
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)
        return np.array([x, y, z])
    
    def _compute_x_angle(
        self,
        coord1: 'H3S2RnCoordinate',
        coord2: 'H3S2RnCoordinate'
    ) -> float:
        """计算 X 轴自旋夹角 (度)"""
        angle_rad = np.arccos(
            coord1.x_spin * coord2.x_spin
        )
        return np.degrees(angle_rad)
    
    def _detect_anomaly(self, trajectory: np.ndarray) -> float:
        """检测轨迹曲率异常"""
        # 计算二阶导数 (加速度)
        if len(trajectory) < 3:
            return 0.0
        
        acceleration = np.diff(trajectory, n=2, axis=0)
        anomaly_score = np.linalg.norm(acceleration, axis=1).max()
        return anomaly_score
    
    def _infer_w_mass(self, anomaly: float) -> float:
        """从曲率反算 W 轴质量"""
        # 简化: 曲率越大，阴影质量越大
        return -anomaly / 10.0
    
    def _compute_trajectory_energy(
        self,
        start: 'H3S2RnCoordinate',
        end: 'H3S2RnCoordinate'
    ) -> float:
        """计算轨迹能量"""
        distance = np.linalg.norm(
            end.to_10d_embedding() - start.to_10d_embedding()
        )
        return distance
    
    def _get_real_world_outcome(self) -> Optional[float]:
        """获取真实世界反馈 (用于 Phase IV)"""
        # TODO: 从外部 API 或数据库获取验证结果
        return None
```

### 2.3 集成测试

```python
# cognitive_physics_engine/world_os/brain/tests/test_ca_engine.py

import pytest
from cognitive_physics_engine.world_os.kernel.manifold_v2 import (
    CognitiveManifoldV2,
    H3S2RnCoordinate
)
from cognitive_physics_engine.world_os.brain.ca_engine import (
    CognitiveAlphaEngine,
    Narrative
)
from cognitive_physics_engine.world_os.brain.llm_agent import LLMAgent
from cognitive_physics_engine.world_os.brain.neural_ode import NeuralODESolver
from cognitive_physics_engine.world_os.storage.markdown_db import MarkdownDB

@pytest.fixture
def ca_engine():
    """创建测试用 CA 引擎"""
    manifold = CognitiveManifoldV2()
    llm = LLMAgent(model='gpt-4')  # Mock
    ode = NeuralODESolver()
    db = MarkdownDB(root_dir='test_world_state')
    
    engine = CognitiveAlphaEngine(manifold, llm, ode, db)
    return engine

def test_phase_1_propagation(ca_engine):
    """测试全息繁衍"""
    seed = ca_engine.manifold.encode_state(
        level=1,
        domain="Tech",
        stance=0.5,
        intent=0.0,
        time=0.0,
        scale=0.0
    )
    
    context = {
        'seed_text': "NVIDIA stock price dropped 10%",
        'entity_id': 'nvidia'
    }
    
    narratives = ca_engine.phase_1_propagation(seed, context)
    
    # 验证生成数量
    assert len(narratives) > 0
    
    # 验证包含多维度
    dimensions = set(n.narrative_id.split('_')[0] for n in narratives)
    assert 'z' in dimensions or 'y' in dimensions or 'x' in dimensions

def test_phase_2_collapse(ca_engine):
    """测试认知坍缩"""
    # 创建模拟剧本
    narratives = [
        Narrative(
            narrative_id="test_1",
            coordinates=ca_engine.manifold.encode_state(1, "Tech", 0.5, 0, 0, 0),
            content="Bullish narrative",
            llm_confidence=0.8,
            geometric_feasibility=0.9,
            dynamic_energy=5.0,
            mass=10.0
        ),
        Narrative(
            narrative_id="test_2",
            coordinates=ca_engine.manifold.encode_state(1, "Tech", -0.5, 0, 0, 0),
            content="Bearish narrative",
            llm_confidence=0.7,
            geometric_feasibility=0.8,
            dynamic_energy=3.0,
            mass=5.0
        )
    ]
    
    survivor = ca_engine.phase_2_collapse(narratives, context={})
    
    # 验证只有一个幸存者
    assert survivor is not None
    assert survivor.is_alive
    
    # 验证动量更大的那个胜出
    assert survivor.mass > 5.0

def test_full_ca_cycle(ca_engine):
    """测试完整 4 阶段循环"""
    seed = ca_engine.manifold.encode_state(1, "Tech", 0.5, 0, 0, 0)
    context = {
        'seed_text': "AI revolution",
        'entity_id': 'ai_sector'
    }
    
    result = ca_engine.run(seed, context, full_cycle=True)
    
    assert result.success
    assert result.phase_1_narratives is not None
    assert result.phase_2_survivor is not None
    assert result.phase_3_smoothed is not None
    assert result.phase_4_updated_params is not None
    
    # 验证性能
    assert result.execution_time['phase_1'] < 10.0  # 秒
    assert result.execution_time['phase_2'] < 5.0
```

---

## Phase 3: 存储层标准化

### 3.1 H3S2Rn Protocol 实现

**白皮书定义 (3.6 节)**:
```yaml
---
# === H3S2Rn 坐标头 ===
uuid: "entity_tesla_inc"
type: "Entity"

# 几何层
coordinates:
  z_level: "L3"
  z_confidence: 0.5
  y_domain: ["Auto", "Tech"]
  
# 纤维层
fibers:
  x_spin: -0.4
  w_mass: 0.1
  s_scale: "Macro"
  
# 动力学参数
dynamics:
  velocity: [-0.01, 0.0, -0.05]
  friction_eta: 0.8
  curvature_gamma: 1.2
---

# 叙事层...
```

**新实现**:
```python
# cognitive_physics_engine/world_os/storage/h3s2rn_protocol.py

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import yaml
from pathlib import Path

@dataclass
class H3S2RnEntity:
    """标准 H3S2Rn 实体格式
    
    白皮书 3.6 节: MDVS 数据范式
    """
    # 内核层
    uuid: str
    entity_type: str  # Entity/Event/Concept/Relation
    last_update: str
    consensus_version: str
    
    # 几何层 (Base Space)
    z_level: str  # L1/L3/L5
    z_confidence: float  # 0.0-1.0
    y_domains: List[str]
    y_cross_links: Optional[List[Dict]] = None
    
    # 纤维层 (Fiber Space)
    x_spin: float  # -1.0 ~ 1.0
    w_mass: float  # Shadow < 0, Daylight >= 0
    s_scale: str   # Micro/Meso/Macro
    
    # 动力学层
    velocity: Optional[List[float]] = None
    friction_eta: float = 0.5
    curvature_gamma: float = 1.0
    expansion_psi: float = 0.0
    
    # 叙事层
    narrative: str = ""
    evidence_chain: Optional[List[Dict]] = None
    shadow_audit: Optional[str] = None
    
    def to_markdown(self) -> str:
        """序列化为标准 Markdown 格式"""
        # YAML Frontmatter
        frontmatter = {
            'uuid': self.uuid,
            'type': self.entity_type,
            'last_update': self.last_update,
            'consensus_version': self.consensus_version,
            'coordinates': {
                'z_level': self.z_level,
                'z_confidence': self.z_confidence,
                'y_domain': self.y_domains[0] if self.y_domains else "Generic",
                'y_cross': self.y_domains[1:] if len(self.y_domains) > 1 else []
            },
            'fibers': {
                'x_spin': self.x_spin,
                'w_mass': self.w_mass,
                's_scale': self.s_scale
            },
            'dynamics': {
                'velocity': self.velocity or [0.0, 0.0, 0.0],
                'friction_eta': self.friction_eta,
                'curvature_gamma': self.curvature_gamma,
                'expansion_psi': self.expansion_psi
            }
        }
        
        if self.y_cross_links:
            frontmatter['links'] = self.y_cross_links
        
        yaml_text = yaml.dump(frontmatter, allow_unicode=True)
        
        # Markdown Body
        body_sections = []
        
        # 当前共识
        body_sections.append("## 当前共识 (Current Consensus)\n")
        body_sections.append(f"> **状态**: {self._decode_state()}\n")
        body_sections.append(f"> **置信度**: {self.z_confidence:.2%}\n\n")
        
        if self.narrative:
            body_sections.append("**核心逻辑**:\n")
            body_sections.append(f"{self.narrative}\n\n")
        
        # 证据链
        if self.evidence_chain:
            body_sections.append("## 证据链 (Evidence Chain)\n")
            for evidence in self.evidence_chain:
                level = evidence.get('level', 'L1')
                content = evidence.get('content', '')
                source = evidence.get('source', 'Unknown')
                weight = evidence.get('weight', 0.5)
                body_sections.append(
                    f"- [{level}] {content} (Source: {source}, Weight: {weight:.2f})\n"
                )
            body_sections.append("\n")
        
        # 阴影审计
        if self.shadow_audit:
            body_sections.append("## 阴影审计 (Shadow Audit)\n")
            body_sections.append(f"{self.shadow_audit}\n\n")
        
        # 组装
        return f"---\n{yaml_text}---\n\n{''.join(body_sections)}"
    
    @classmethod
    def from_markdown(cls, md_text: str) -> 'H3S2RnEntity':
        """从 Markdown 反序列化"""
        import re
        
        # 提取 YAML Frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', md_text, re.DOTALL)
        if not match:
            raise ValueError("Invalid H3S2Rn format: missing frontmatter")
        
        yaml_text = match.group(1)
        body_text = match.group(2)
        
        data = yaml.safe_load(yaml_text)
        
        # 解析
        coords = data.get('coordinates', {})
        fibers = data.get('fibers', {})
        dynamics = data.get('dynamics', {})
        
        return cls(
            uuid=data['uuid'],
            entity_type=data.get('type', 'Entity'),
            last_update=data.get('last_update', ''),
            consensus_version=data.get('consensus_version', 'v1'),
            z_level=coords.get('z_level', 'L3'),
            z_confidence=coords.get('z_confidence', 0.5),
            y_domains=[coords.get('y_domain', 'Generic')] + coords.get('y_cross', []),
            y_cross_links=data.get('links'),
            x_spin=fibers.get('x_spin', 0.0),
            w_mass=fibers.get('w_mass', 0.0),
            s_scale=fibers.get('s_scale', 'Meso'),
            velocity=dynamics.get('velocity'),
            friction_eta=dynamics.get('friction_eta', 0.5),
            curvature_gamma=dynamics.get('curvature_gamma', 1.0),
            expansion_psi=dynamics.get('expansion_psi', 0.0),
            narrative=cls._extract_narrative(body_text),
            evidence_chain=cls._extract_evidence(body_text),
            shadow_audit=cls._extract_shadow(body_text)
        )
    
    def _decode_state(self) -> str:
        """解码当前状态描述"""
        stance = "看多" if self.x_spin > 0.3 else "看空" if self.x_spin < -0.3 else "中立"
        shadow = "阴影警告" if self.w_mass < -0.3 else "正常"
        return f"{stance} | {shadow} | {self.s_scale}"
    
    @staticmethod
    def _extract_narrative(body: str) -> str:
        """提取叙事文本"""
        match = re.search(r'核心逻辑.*?:\s*\n(.*?)\n\n', body, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    @staticmethod
    def _extract_evidence(body: str) -> List[Dict]:
        """提取证据链"""
        pattern = r'\[(L\d)\] (.*?) \(Source: (.*?), Weight: ([\d.]+)\)'
        matches = re.findall(pattern, body)
        return [
            {'level': m[0], 'content': m[1], 'source': m[2], 'weight': float(m[3])}
            for m in matches
        ]
    
    @staticmethod
    def _extract_shadow(body: str) -> Optional[str]:
        """提取阴影审计"""
        match = re.search(r'阴影审计.*?:\s*\n(.*?)(?:\n\n|$)', body, re.DOTALL)
        return match.group(1).strip() if match else None
```

---

## 实施时间表

| Phase | 任务 | 工作量 | 优先级 | 状态 |
|-------|------|--------|--------|------|
| Phase 1 | 流形几何引擎重构 | 40小时 | 🔴 Critical | Pending |
| Phase 2.1 | CA Engine - Phase I (全息繁衍) | 60小时 | 🔴 Critical | Pending |
| Phase 2.2 | CA Engine - Phase II (认知坍缩) | 40小时 | 🔴 Critical | Pending |
| Phase 2.3 | CA Engine - Phase III (时序平滑) | 30小时 | 🔴 Critical | Pending |
| Phase 2.4 | CA Engine - Phase IV (递归进化) | 30小时 | 🔴 Critical | Pending |
| Phase 3 | H3S2Rn 存储协议 | 20小时 | 🟡 Important | Pending |
| Phase 4 | 上下行交互界面 | 40小时 | 🟡 Important | Pending |
| Phase 5 | PoM 共识与分片 | 60小时 | 🟢 Nice-to-have | Pending |
| **Total** | | **320小时** (40天 @ 8h/day) | | |

---

## 下一步行动

1. **立即开始 Phase 1**: 实现 `CognitiveManifoldV2`
2. **并行准备**: 安装 `geomstats`, `torch`, `torchdiffeq`
3. **测试驱动开发**: 先写测试用例，再实现代码
4. **保持 v61.0 兼容**: 新代码不影响现有系统

**建议命令**:
```bash
cd /home/user/webapp/cognitive_physics_engine
pip install geomstats torch torchdiffeq pyyaml

# 创建新模块
mkdir -p world_os/kernel_v2
touch world_os/kernel_v2/__init__.py
touch world_os/kernel_v2/manifold.py
touch world_os/kernel_v2/coordinates.py

# 开始实现...
```

---

**THE MANIFOLD IS THE TRUTH. THE CODE IS THE LAW.**
