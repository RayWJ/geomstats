"""
Manifold Visualization Backend
===============================

生成流形可视化所需的数据，供前端 Three.js 渲染

功能：
1. Poincaré disk projection (双曲空间可视化)
2. Sphere projection (领域空间可视化)
3. Agent trajectories (Agent 轨迹)
4. Geodesic curves (测地线)
5. Metric tensor heatmap (度量张量热图)

Author: Raywu Paradigm Implementation Team
Date: 2026-02-01
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import json

try:
    from raywu_manifold import RaywuCognitiveManifold
    GEOMSTATS_AVAILABLE = True
except ImportError:
    GEOMSTATS_AVAILABLE = False


class ManifoldVisualizer:
    """
    流形可视化器
    
    将高维流形投影到可视化空间
    """
    
    def __init__(self, manifold: Optional['RaywuCognitiveManifold'] = None):
        if manifold is None and GEOMSTATS_AVAILABLE:
            self.manifold = RaywuCognitiveManifold()
        else:
            self.manifold = manifold
        
        # 颜色映射
        self.level_colors = {
            1: "#FF6B6B",  # L1: Red (事实)
            3: "#4ECDC4",  # L3: Cyan (逻辑)
            5: "#95E1D3",  # L5: Green (战略)
        }
        
        self.stance_colors = {
            "bull": "#2ECC71",   # Green
            "neutral": "#95A5A6", # Gray
            "bear": "#E74C3C",   # Red
        }
    
    # ==================== POINCARÉ DISK PROJECTION ====================
    
    def project_to_poincare_disk(self, points: np.ndarray) -> np.ndarray:
        """
        将双曲空间中的点投影到 Poincaré disk (2D圆盘)
        
        输入: points shape (N, 2) - 双曲空间坐标
        输出: disk_points shape (N, 2) - 圆盘坐标 (x, y) ∈ [-1, 1]²
        """
        # Poincaré ball 模型: 点已经在 ball 中，直接返回 x, y
        # 确保在单位圆内
        points = np.array(points)
        if points.ndim == 1:
            points = points.reshape(1, -1)
        
        # 只取前两维（如果有更多维）
        disk_points = points[:, :2]
        
        # 确保在单位圆内（Poincaré disk 边界是 r < 1）
        radii = np.linalg.norm(disk_points, axis=1, keepdims=True)
        radii = np.maximum(radii, 1e-8)  # 避免除以零
        
        # 如果超出边界，缩放回来
        scale = np.where(radii >= 0.95, 0.95 / radii, 1.0)
        disk_points = disk_points * scale
        
        return disk_points
    
    def generate_poincare_grid(self, n_circles: int = 8, n_rays: int = 16) -> Dict[str, Any]:
        """
        生成 Poincaré disk 的网格线（双曲几何网格）
        
        返回：
        - circles: 同心圆（测地圆）
        - rays: 从中心发出的射线（测地线）
        """
        grid = {
            "circles": [],
            "rays": []
        }
        
        # 同心圆（在双曲几何中，这些不是真正的测地圆，但便于可视化）
        for i in range(1, n_circles + 1):
            r = i / (n_circles + 1)
            circle_points = []
            for theta in np.linspace(0, 2*np.pi, 100):
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                circle_points.append([x, y])
            grid["circles"].append(circle_points)
        
        # 径向射线
        for i in range(n_rays):
            theta = 2 * np.pi * i / n_rays
            ray_points = []
            for r in np.linspace(0, 0.95, 50):
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                ray_points.append([x, y])
            grid["rays"].append(ray_points)
        
        return grid
    
    # ==================== SPHERE PROJECTION ====================
    
    def project_to_sphere(self, points: np.ndarray) -> np.ndarray:
        """
        将 S² 上的点投影到 3D 球面坐标
        
        输入: points shape (N, 3) - 单位球面坐标 (x, y, z)
        输出: sphere_points shape (N, 3) - 3D 坐标
        """
        points = np.array(points)
        if points.ndim == 1:
            points = points.reshape(1, -1)
        
        # 取前 3 维
        sphere_points = points[:, :3]
        
        # 归一化到单位球面
        norms = np.linalg.norm(sphere_points, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-8)
        sphere_points = sphere_points / norms
        
        return sphere_points
    
    def generate_sphere_grid(self, n_lat: int = 12, n_lon: int = 24) -> Dict[str, Any]:
        """
        生成球面网格线（经纬线）
        """
        grid = {
            "latitude": [],
            "longitude": []
        }
        
        # 纬线
        for i in range(1, n_lat):
            phi = np.pi * i / n_lat
            lat_points = []
            for theta in np.linspace(0, 2*np.pi, 100):
                x = np.sin(phi) * np.cos(theta)
                y = np.sin(phi) * np.sin(theta)
                z = np.cos(phi)
                lat_points.append([x, y, z])
            grid["latitude"].append(lat_points)
        
        # 经线
        for i in range(n_lon):
            theta = 2 * np.pi * i / n_lon
            lon_points = []
            for phi in np.linspace(0, np.pi, 50):
                x = np.sin(phi) * np.cos(theta)
                y = np.sin(phi) * np.sin(theta)
                z = np.cos(phi)
                lon_points.append([x, y, z])
            grid["longitude"].append(lon_points)
        
        return grid
    
    # ==================== AGENT VISUALIZATION ====================
    
    def visualize_agents(self, agents: List[Any]) -> Dict[str, Any]:
        """
        可视化 Agent 的位置和状态
        
        返回：
        {
            "poincare": [...],  # Poincaré disk 上的投影
            "sphere": [...],    # 球面上的投影
            "agents": [...]     # Agent 详细信息
        }
        """
        if not self.manifold:
            return {"error": "Manifold not available"}
        
        viz_data = {
            "poincare": [],
            "sphere": [],
            "agents": []
        }
        
        for agent in agents:
            # 提取流形坐标
            position = agent.position
            
            # 解码语义信息
            decoded = self.manifold.decode_agent_state(position)
            
            # Poincaré disk 投影（Z 轴：Level）
            poincare_coords = position[:2]  # 前两维是双曲空间
            disk_point = self.project_to_poincare_disk(poincare_coords)[0]
            
            # Sphere 投影（Y 轴：Domain）
            # 从角度重建球面坐标
            domain_map = {"tech": 0, "finance": 1, "politics": 2}
            domain_idx = domain_map.get(decoded['domain'], 0)
            theta = 2 * np.pi * domain_idx / 3
            phi = np.pi / 2  # 赤道
            
            sphere_point = [
                np.sin(phi) * np.cos(theta),
                np.sin(phi) * np.sin(theta),
                np.cos(phi)
            ]
            
            # Agent 信息
            agent_info = {
                "id": agent.id,
                "level": agent.level,
                "domain": agent.domain,
                "stance": agent.stance,
                "intent": agent.intent,
                "confidence": agent.confidence,
                "color": self.level_colors.get(agent.level, "#FFFFFF"),
                "poincare": disk_point.tolist(),
                "sphere": sphere_point,
                "position_9d": position.tolist()
            }
            
            viz_data["poincare"].append({
                "point": disk_point.tolist(),
                "agent_id": agent.id,
                "level": agent.level,
                "color": self.level_colors.get(agent.level, "#FFFFFF")
            })
            
            viz_data["sphere"].append({
                "point": sphere_point,
                "agent_id": agent.id,
                "domain": agent.domain,
                "color": self.stance_colors.get(agent.stance, "#FFFFFF")
            })
            
            viz_data["agents"].append(agent_info)
        
        return viz_data
    
    # ==================== GEODESIC VISUALIZATION ====================
    
    def compute_geodesic(self, point1: np.ndarray, point2: np.ndarray, n_steps: int = 50) -> np.ndarray:
        """
        计算两点之间的测地线
        
        输入: 两个流形上的点
        输出: 测地线上的点序列
        """
        if not self.manifold:
            # Fallback: 线性插值
            t = np.linspace(0, 1, n_steps).reshape(-1, 1)
            geodesic_points = (1 - t) * point1 + t * point2
            return geodesic_points
        
        # 使用流形的指数映射和对数映射
        try:
            # 简化版：使用线性插值作为近似
            # 真正的测地线需要求解测地方程
            t = np.linspace(0, 1, n_steps).reshape(-1, 1)
            geodesic_points = (1 - t) * point1 + t * point2
            
            # 投影回流形（保持在 Poincaré ball 内）
            # 对于双曲分量
            for i in range(len(geodesic_points)):
                pt = geodesic_points[i]
                # 双曲部分（前2维）
                hyperbolic_part = pt[:2]
                r = np.linalg.norm(hyperbolic_part)
                if r >= 0.95:
                    hyperbolic_part = hyperbolic_part * (0.95 / r)
                    pt[:2] = hyperbolic_part
                
                # 球面部分（2-5维，实际是2-4）
                sphere_part = pt[2:5]
                r_sphere = np.linalg.norm(sphere_part)
                if r_sphere > 0:
                    sphere_part = sphere_part / r_sphere
                    pt[2:5] = sphere_part
            
            return geodesic_points
        
        except Exception as e:
            print(f"⚠️  Geodesic computation failed: {e}")
            t = np.linspace(0, 1, n_steps).reshape(-1, 1)
            return (1 - t) * point1 + t * point2
    
    def visualize_geodesics(self, agents: List[Any], max_connections: int = 10) -> List[Dict[str, Any]]:
        """
        可视化 Agent 之间的测地线
        
        返回测地线列表，每条包含：
        - points: 测地线上的点
        - distance: 测地距离
        - agents: 连接的两个 Agent
        """
        if len(agents) < 2:
            return []
        
        geodesics = []
        
        # 计算所有距离对
        distances = []
        for i in range(len(agents)):
            for j in range(i+1, len(agents)):
                if self.manifold:
                    dist = self.manifold.cognitive_distance(
                        agents[i].position, 
                        agents[j].position
                    )
                else:
                    dist = np.linalg.norm(agents[i].position - agents[j].position)
                
                distances.append((i, j, dist))
        
        # 选择距离最近的前 N 对
        distances.sort(key=lambda x: x[2])
        top_pairs = distances[:max_connections]
        
        for i, j, dist in top_pairs:
            # 计算测地线
            geodesic_points = self.compute_geodesic(
                agents[i].position, 
                agents[j].position, 
                n_steps=30
            )
            
            # 投影到 Poincaré disk
            poincare_geodesic = []
            for pt in geodesic_points:
                disk_pt = self.project_to_poincare_disk(pt[:2])[0]
                poincare_geodesic.append(disk_pt.tolist())
            
            geodesics.append({
                "points_poincare": poincare_geodesic,
                "distance": float(dist),
                "agent1": agents[i].id,
                "agent2": agents[j].id,
                "color": "#FFD700" if dist < 1.0 else "#888888"
            })
        
        return geodesics
    
    # ==================== METRIC TENSOR HEATMAP ====================
    
    def generate_metric_heatmap(self, resolution: int = 30) -> Dict[str, Any]:
        """
        生成度量张量的热图
        
        在 Poincaré disk 上采样，计算每个点的度量行列式
        
        返回：
        {
            "grid": [[det(g) at each point]],
            "x": [...],
            "y": [...],
            "min": ...,
            "max": ...
        }
        """
        if not self.manifold:
            return {"error": "Manifold not available"}
        
        # 在 Poincaré disk 上采样
        x = np.linspace(-0.9, 0.9, resolution)
        y = np.linspace(-0.9, 0.9, resolution)
        
        heatmap_data = np.zeros((resolution, resolution))
        
        for i, xi in enumerate(x):
            for j, yj in enumerate(y):
                # 检查是否在单位圆内
                r = np.sqrt(xi**2 + yj**2)
                if r >= 0.95:
                    heatmap_data[i, j] = np.nan
                    continue
                
                # 构造流形上的点
                # 双曲部分
                hyperbolic_part = np.array([xi, yj])
                # 球面部分（默认）
                sphere_part = np.array([1.0, 0.0, 0.0])  # 归一化
                # 欧几里得部分（中性）
                euclidean_part = np.array([0.0, 0.0, 0.0, 0.0])
                
                # 组合成 9D 点
                point = np.concatenate([
                    hyperbolic_part, 
                    sphere_part, 
                    euclidean_part
                ])
                
                # 计算度量张量
                try:
                    g = self.manifold.metric.metric_matrix(point)
                    det_g = abs(np.linalg.det(g))
                    
                    # 取对数以便可视化
                    heatmap_data[i, j] = np.log10(det_g + 1e-10)
                
                except Exception as e:
                    heatmap_data[i, j] = 0.0
        
        return {
            "grid": heatmap_data.tolist(),
            "x": x.tolist(),
            "y": y.tolist(),
            "min": float(np.nanmin(heatmap_data)),
            "max": float(np.nanmax(heatmap_data))
        }
    
    # ==================== COMPLETE VISUALIZATION ====================
    
    def generate_complete_visualization(self, agents: List[Any]) -> Dict[str, Any]:
        """
        生成完整的可视化数据包
        
        包含：
        - Poincaré disk grid
        - Sphere grid
        - Agent positions
        - Geodesics
        - Metric heatmap
        """
        return {
            "poincare_grid": self.generate_poincare_grid(),
            "sphere_grid": self.generate_sphere_grid(),
            "agents": self.visualize_agents(agents),
            "geodesics": self.visualize_geodesics(agents),
            "metric_heatmap": self.generate_metric_heatmap(),
            "metadata": {
                "n_agents": len(agents),
                "timestamp": "2026-02-01",
                "manifold_type": "H²×S²×R⁴"
            }
        }


# ==================== DEMO ====================

if __name__ == "__main__":
    print("=" * 80)
    print("MANIFOLD VISUALIZER TEST")
    print("=" * 80)
    
    if not GEOMSTATS_AVAILABLE:
        print("\n⚠️  Geomstats not available.")
        exit(1)
    
    # 创建可视化器
    manifold = RaywuCognitiveManifold()
    visualizer = ManifoldVisualizer(manifold)
    
    # 创建测试 Agent
    from deep_state_agent_geometric import Agent, AgentRole
    
    test_agents = []
    for i, (level, domain, stance) in enumerate([
        (1, "tech", "bull"),
        (3, "finance", "bear"),
        (5, "politics", "neutral"),
    ]):
        position = manifold.encode_agent_state(
            level=level,
            domain=domain,
            stance=0.8 if stance=="bull" else (-0.8 if stance=="bear" else 0.0),
            intent=0.5,
            time=0.0,
            scale=0.5
        )
        
        agent = Agent(
            id=f"agent_{i}",
            role=AgentRole.CONCEPT_AGENT if level==5 else AgentRole.INSTANCE_AGENT,
            position=position,
            level=level,
            domain=domain,
            stance=stance,
            intent="daylight"
        )
        test_agents.append(agent)
    
    # 生成可视化数据
    print("\n📊 Generating visualization data...\n")
    
    viz_data = visualizer.generate_complete_visualization(test_agents)
    
    print(f"✓ Poincaré grid: {len(viz_data['poincare_grid']['circles'])} circles, {len(viz_data['poincare_grid']['rays'])} rays")
    print(f"✓ Sphere grid: {len(viz_data['sphere_grid']['latitude'])} lat, {len(viz_data['sphere_grid']['longitude'])} lon")
    print(f"✓ Agents visualized: {len(viz_data['agents']['agents'])}")
    print(f"✓ Geodesics computed: {len(viz_data['geodesics'])}")
    print(f"✓ Metric heatmap: {len(viz_data['metric_heatmap']['x'])}×{len(viz_data['metric_heatmap']['y'])} grid")
    
    # 保存到文件
    output_path = "visualization_data.json"
    with open(output_path, 'w') as f:
        json.dump(viz_data, f, indent=2)
    
    print(f"\n✅ Visualization data saved to: {output_path}")
    print("=" * 80)
