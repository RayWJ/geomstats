# 🌐 前端访问指南

## ✅ 问题已修复！

之前前端无法访问的问题已经解决。现在所有页面都可以通过后端服务器访问。

---

## 🚀 访问链接

### 主页（推荐从这里开始）
**URL**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai

包含4个导航卡片：
- 🎨 3D Manifold Visualization
- 💬 Query Interface
- 📚 API Documentation  
- 📊 Visualization Data API

---

### 各功能直达链接

#### 1. 🎨 3D 流形可视化（推荐！）
**URL**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/viz

**功能**：
- ✅ Poincaré Disk 视图（双曲几何）
- ✅ Sphere 视图（领域空间）
- ✅ Combined 视图（并排显示）
- ✅ 实时 Agent 显示
- ✅ 测地线可视化
- ✅ 度量热图（阴影引力）

**交互**：
- 🖱️ 鼠标拖拽旋转
- 🎡 滚轮缩放
- ☑️ 切换网格/测地线/热图
- 🔄 自动旋转

---

#### 2. 💬 查询界面
**URL**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/ui

**功能**：
- 提问并运行模拟
- 查看共识结果
- 调整参数（视角数量、模拟时间等）

---

#### 3. 📚 API 文档（Swagger UI）
**URL**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/docs

**功能**：
- 交互式 API 测试
- 完整端点文档
- 请求/响应示例

---

#### 4. 📊 可视化数据 API
**URL**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/visualization/data

**返回**：
- Poincaré grid（圆圈和射线）
- Sphere grid（经纬线）
- Agent 位置和属性
- 测地线数据
- 度量热图

---

## 🔧 修复内容

### 之前的问题
❌ 前端文件无法直接访问  
❌ CORS 问题  
❌ localhost URL 硬编码  

### 现在的解决方案
✅ FastAPI StaticFiles 挂载  
✅ 专用路由（/viz, /ui）  
✅ 自动 URL 注入  
✅ 美观的导航页面  

---

## 🎯 快速开始

### 方法1：从主页开始（推荐）
1. 打开：https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai
2. 点击任意卡片导航

### 方法2：直接访问可视化
1. 打开：https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/viz
2. 查看 Poincaré disk 上的 Agents
3. 点击视图切换按钮（Poincaré / Sphere / Combined）
4. 用鼠标拖拽旋转，滚轮缩放

### 方法3：测试 API
1. 打开：https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/docs
2. 展开 GET /visualization/data
3. 点击 "Try it out" → "Execute"
4. 查看返回的 JSON 数据

---

## 🎨 3D 可视化使用指南

### 视图切换
- **Poincaré Disk**：显示 Z 轴（Level）的双曲几何投影
  - Agent 按 Level 着色（L1=红, L3=青, L5=绿）
  - 测地线显示为弯曲的线
  - 边界圆代表无穷远

- **Sphere**：显示 Y 轴（Domain）的球面分布
  - Agent 按 Domain 分布（tech, finance, politics）
  - 按 Stance 着色（bull=绿, bear=红, neutral=灰）

- **Combined**：并排显示两个视图

### 控制选项
- ☑️ **Show Grid**：显示几何网格
- ☑️ **Show Geodesics**：显示 Agent 之间的测地线
- ☑️ **Show Heatmap**：显示度量张量热图
- ☑️ **Auto Rotate**：自动旋转视图

### 按钮
- **Reset View**：重置相机视角
- **Refresh Data**：重新加载数据

---

## 📊 数据说明

### Agent 信息（右侧边栏）
每个 Agent 卡片显示：
- **ID**：agent_0, agent_1, ...
- **Level**：L1（事实）/ L3（逻辑）/ L5（战略）
- **Domain**：tech / finance / politics
- **Stance**：bull / neutral / bear
- **Confidence**：置信度百分比

### 统计数据
- **Manifold Type**：H²×S²×R⁴（双曲×球面×欧几里得）
- **Agents**：当前 Agent 数量
- **Geodesics**：计算的测地线数量
- **Avg Distance**：平均测地距离

---

## 🔬 技术细节

### 后端提供
- **FastAPI** 服务器（端口 8000）
- **StaticFiles** 挂载前端
- **CORS** 配置允许跨域
- **动态 URL** 注入（自动适配 sandbox 环境）

### 前端技术
- **Three.js**：3D 渲染引擎
- **WebGL**：硬件加速图形
- **实时更新**：通过 API 拉取数据

### 几何计算
- **Poincaré 投影**：H² → 2D disk
- **球面投影**：S² → 3D sphere
- **测地线**：流形上的最短路径
- **度量热图**：det(g) 的可视化

---

## 🐛 故障排除

### 如果页面加载失败
1. 检查后端是否运行：
   ```bash
   curl https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/health
   ```
   应返回：`{"status":"healthy","simulator_initialized":true}`

2. 强制刷新浏览器：
   - Chrome/Edge: Ctrl+Shift+R（Windows）或 Cmd+Shift+R（Mac）
   - Firefox: Ctrl+F5

3. 清除浏览器缓存

### 如果 3D 视图不显示
1. 检查浏览器控制台（F12）是否有错误
2. 确认浏览器支持 WebGL
3. 尝试切换视图（Poincaré ↔ Sphere）

### 如果数据不更新
1. 点击 "Refresh Data" 按钮
2. 检查网络请求（F12 → Network）
3. 确认 API 端点可访问

---

## 💡 使用建议

### 探索流形几何
1. 切换到 Poincaré Disk 视图
2. 开启 "Show Grid" 查看双曲网格
3. 观察 Agent 如何分布在双曲空间中
4. 注意测地线是弯曲的，不是直线

### 理解阴影引力
1. 开启 "Show Heatmap"
2. 红色区域 = 高度量扭曲（阴影引力强）
3. 蓝色区域 = 低度量扭曲（阳光区域）
4. 扭曲比例可达 211 亿倍

### 对比两个空间
1. 切换到 Combined 视图
2. 左侧：Poincaré disk（Level 层级）
3. 右侧：Sphere（Domain 领域）
4. 观察同一 Agent 在两个空间的位置

---

## 🎉 享受探索！

现在你可以：
- ✅ 访问所有前端页面
- ✅ 查看 3D 流形可视化
- ✅ 理解几何结构
- ✅ 测试 API 端点

**主入口**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai

**直达可视化**: https://8000-i5c2ywpdmon8woe0l978h-ad490db5.sandbox.novita.ai/viz

---

**如有问题，请查看控制台日志或联系开发团队。**

🎯 **"在弯曲空间中探索真理的几何结构"** 🎯
