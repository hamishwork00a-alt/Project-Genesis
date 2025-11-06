"""
核心数学模块 - 幻方运算和量子约束
"""

import numpy as np

# ==================== 幻方生成 ====================
def generate_magic_square_3x3():
    """生成标准的3x3幻方（洛书）"""
    return np.array([[8, 1, 6],
                     [3, 5, 7], 
                     [4, 9, 2]], dtype=np.float64)

def generate_magic_square_5x5():
    """生成标准的5x5幻方"""
    return np.array([[17, 24, 1, 8, 15],
                     [23, 5, 7, 14, 16],
                     [4, 6, 13, 20, 22],
                     [10, 12, 19, 21, 3],
                     [11, 18, 25, 2, 9]], dtype=np.float64)

def create_approximate_magic_square(order):
    """为任意阶数创建近似幻方"""
    magic_sum = order * (order**2 + 1) / 2
    avg_value = magic_sum / order
    
    base = np.full((order, order), avg_value)
    variation = np.random.normal(0, avg_value * 0.1, (order, order))
    candidate = base + variation
    
    # 粗略调整行和列的和
    for i in range(order):
        row_sum = np.sum(candidate[i, :])
        candidate[i, :] *= magic_sum / row_sum
        
    for j in range(order):
        col_sum = np.sum(candidate[:, j])
        candidate[:, j] *= magic_sum / col_sum
        
    return candidate

# ==================== 幻方验证 ====================
def is_magic_square(matrix, tolerance=1e-10):
    """验证是否为幻方"""
    n = matrix.shape[0]
    if n == 0:
        return False
        
    magic_constant = np.sum(matrix[0, :])
    
    # 检查行和列
    for i in range(n):
        if abs(np.sum(matrix[i, :]) - magic_constant) > tolerance:
            return False
        if abs(np.sum(matrix[:, i]) - magic_constant) > tolerance:
            return False
    
    # 检查对角线
    if abs(np.sum(np.diag(matrix)) - magic_constant) > tolerance:
        return False
    if abs(np.sum(np.diag(np.fliplr(matrix))) - magic_constant) > tolerance:
        return False
    
    return True

def calculate_imbalance(matrix):
    """计算矩阵的不平衡度"""
    n = matrix.shape[0]
    if n == 0:
        return 0
    
    magic_constant = n * (n**2 + 1) / 2
    imbalance = 0
    
    for i in range(n):
        imbalance += abs(np.sum(matrix[i, :]) - magic_constant)
        imbalance += abs(np.sum(matrix[:, i]) - magic_constant)
    
    imbalance += abs(np.sum(np.diag(matrix)) - magic_constant)
    imbalance += abs(np.sum(np.diag(np.fliplr(matrix))) - magic_constant)
    
    return imbalance

def parity_stability_score(magic_square):
    """基于幻方阶数奇偶性的稳定性评分"""
    if magic_square is None:
        return 0.0
        
    n = magic_square.shape[0]
    if n % 2 == 1:  # 奇数阶
        base_stability = 0.8 + 0.2 * (1 - 1/n)
    else:  # 偶数阶
        base_stability = 0.5 + 0.2 * (1 - 1/n)
        
    imbalance = calculate_imbalance(magic_square)
    imbalance_penalty = imbalance / (n * 1000)
    
    return max(0.0, base_stability - imbalance_penalty)

if __name__ == "__main__":
    # 测试核心数学功能
    ms3 = generate_magic_square_3x3()
    ms5 = generate_magic_square_5x5()
    
    print("核心数学模块测试:")
    print(f"3x3幻方验证: {is_magic_square(ms3)}")
    print(f"5x5幻方验证: {is_magic_square(ms5)}")
    print(f"3x3奇偶稳定性: {parity_stability_score(ms3):.3f}")
    print(f"5x5奇偶稳定性: {parity_stability_score(ms5):.3f}")
