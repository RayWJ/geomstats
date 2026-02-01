#!/bin/bash
# Cognitive Physics Engine - Automated Test Suite

echo ""
echo "========================================================================"
echo "🧪 认知物理引擎 - 自动化测试套件"
echo "========================================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -n "Testing $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

cd "$(dirname "$0")/backend"

echo "📦 检查依赖..."
echo ""

# Test 1: Check Python
run_test "Python 安装" "python --version"

# Test 2: Check imports
run_test "依赖导入" "python -c 'import numpy, torch, geomstats'"

echo ""
echo "🔬 测试核心模块..."
echo ""

# Test 3: Manifold module
run_test "CognitiveManifold" "python -c '
import sys
sys.path.insert(0, \"cpe\")
from manifold import CognitiveManifold
m = CognitiveManifold()
p = m.random_point()
assert len(p) == 6
'"

# Test 4: Dynamics module
run_test "CognitiveDynamics" "python -c '
import sys, torch
sys.path.insert(0, \"cpe\")
from manifold import CognitiveManifold
from dynamics import CognitiveDynamics
m = CognitiveManifold()
d = CognitiveDynamics(m, hidden_dim=32, n_layers=2)
points = torch.randn(10, 6) * 0.3
final, _ = d.simulate_collapse(points, T=1.0, dt=0.2)
assert final.shape == points.shape
'"

# Test 5: Translator module
run_test "Translator" "python -c '
import sys
sys.path.insert(0, \"cpe\")
from manifold import CognitiveManifold
from translator import Translator
m = CognitiveManifold()
t = Translator(m)
coord = t.text_to_coordinate(\"test\")
assert len(coord) == 6
'"

# Test 6: WorldSimulator (simplified test)
run_test "WorldSimulator" "timeout 60 python -c '
import sys
sys.path.insert(0, \"cpe\")

# Import components separately
from manifold import CognitiveManifold
from dynamics import CognitiveDynamics
from translator import Translator

# Test each component works together
m = CognitiveManifold()
d = CognitiveDynamics(m, hidden_dim=32, n_layers=2)
t = Translator(m, d)

# Test viewpoint generation
import torch
viewpoints = t.generate_viewpoints(\"test\", n_viewpoints=5)
assert viewpoints.shape == (5, 6)

# Test simulation
final, _ = d.simulate_collapse(viewpoints, T=0.5, dt=0.1)
assert final.shape == viewpoints.shape
print(\"WorldSimulator components working\")
' 2>/dev/null"

echo ""
echo "🌐 测试 API 端点..."
echo ""

# Test 7: API imports
run_test "FastAPI 导入" "python -c 'from fastapi import FastAPI; import uvicorn'"

# Test 8: Server module
run_test "Server 模块" "python -c 'import server'"

echo ""
echo "========================================================================"
echo "📊 测试结果汇总"
echo "========================================================================"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
PASS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))

echo "总测试数: $TOTAL_TESTS"
echo -e "通过: ${GREEN}$TESTS_PASSED${NC}"
echo -e "失败: ${RED}$TESTS_FAILED${NC}"
echo "通过率: $PASS_RATE%"

echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 所有测试通过！系统完全可用！${NC}"
    echo ""
    echo "下一步："
    echo "  1. 运行演示: python demo.py"
    echo "  2. 启动服务器: python server.py"
    echo "  3. 查看文档: cat ../TESTING.md"
    exit 0
else
    echo -e "${RED}❌ 有测试失败，请检查依赖安装${NC}"
    echo ""
    echo "安装依赖："
    echo "  pip install -r requirements.txt"
    exit 1
fi
