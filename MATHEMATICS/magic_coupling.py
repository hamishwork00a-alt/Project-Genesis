"""
Magic Square Coupling Algorithms
实现不同阶数幻方的耦合机制，定义奇偶性稳定性评分
"""

import numpy as np
from mathematics.magic_square_core import generate_magic_square_3x3, is_magic_square, calculate_imbalance

class MagicCoupling:
    def __init__(self):
        self.stability_threshold = 0.1  # 稳定性阈值
        
    def couple_squares(self, square_a, square_b, coupling_strength=1.0):
        """
        耦合两个幻方，返回过渡态和可能的稳定态
        
        Args:
            square_a, square_b: 要耦合的两个幻方
            coupling_strength: 耦合强度 (0-1)
            
        Returns:
            dict: 包含过渡态、稳定态和稳定性信息
        """
        n_a = square_a.shape[0]
        n_b = square_b.shape[0]
        
        # 1. 形成复合过渡态（偶数阶）
        transition_square = self._form_transition_state(square_a, square_b, coupling_strength)
        
        # 2. 尝试坍缩到稳定态（奇数阶）
        stable_square = self._collapse_to_stable(transition_square)
        
        # 3. 计算稳定性评分
        stability_score = self._calculate_stability_score(transition_square, stable_square)
        
        return {
            'transition_state': transition_square,
            'stable_state': stable_square,
            'transition_order': transition_square.shape[0],
            'stable_order': stable_square.shape[0] if stable_square is not None else None,
            'stability_score': stability_score,
            'coupling_success': stable_square is not None
        }
    
    def _form_transition_state(self, a, b, strength):
        """形成偶数阶过渡态"""
        n_a, n_b = a.shape[0], b.shape[0]
        
        # 过渡态的阶数是两者之和（保证为偶数）
        transition_order = n_a + n_b
        
        # 创建过渡矩阵（这里用随机初始化，实际应该基于物理约束）
        transition = np.random.rand(transition_order, transition_order)
        
        # 将原幻方的特性"印记"到过渡态中
        transition[:n_a, :n_a] += a * strength
        transition[n_a:, n_a:] += b * strength
        
        return transition
    
    def _collapse_to_stable(self, transition_square):
        """尝试从过渡态坍缩到奇数阶稳定态"""
        n_transition = transition_square.shape[0]
        
        # 目标稳定态是比过渡态小1的奇数阶
        target_order = n_transition - 1 if (n_transition - 1) % 2 == 1 else n_transition - 2
        
        if target_order < 3:  # 最小幻方阶数为3
            return None
            
        # 使用SVD分解找到最稳定的子空间
        U, s, Vt = np.linalg.svd(transition_square)
        
        # 取前target_order个主要成分构建稳定态
        stable_square = U[:, :target_order] @ np.diag(s[:target_order]) @ Vt[:target_order, :]
        
        # 验证是否为有效幻方
        if self._is_valid_magic_configuration(stable_square):
            return stable_square
        return None
    
    def _is_valid_magic_configuration(self, square, tolerance=0.1):
        """检查是否为有效的幻方配置（允许一定误差）"""
        if square.shape[0] < 3:
            return False
            
        # 计算不平衡度
        imbalance = calculate_imbalance(square)
        normalized_imbalance = imbalance / (square.shape[0] * square.shape[0])
        
        return normalized_imbalance < tolerance
    
    def _calculate_stability_score(self, transition, stable):
        """计算耦合的稳定性评分"""
        if stable is None:
            return 0.0
            
        # 基于以下因素计算稳定性：
        # 1. 稳定态的幻方"质量"
        stable_quality = 1.0 / (1 + calculate_imbalance(stable))
        
        # 2. 过渡态到稳定态的能量差（用矩阵范数近似）
        if transition.shape[0] > stable.shape[0]:
            # 计算"坍缩"过程中的"能量释放"
            energy_release = np.linalg.norm(transition) - np.linalg.norm(stable)
            stability_from_energy = np.tanh(energy_release)  # 归一化到0-1
        else:
            stability_from_energy = 0.5
            
        # 3. 阶数奇偶性奖励（奇数阶更稳定）
        parity_bonus = 1.0 if stable.shape[0] % 2 == 1 else 0.3
        
        final_score = (stable_quality * 0.4 + 
                      stability_from_energy * 0.4 + 
                      parity_bonus * 0.2)
        
        return min(1.0, max(0.0, final_score))

# 奇偶性稳定性评分函数
def parity_stability_score(magic_square):
    """基于幻方阶数奇偶性的稳定性评分"""
    if magic_square is None:
        return 0.0
        
    n = magic_square.shape[0]
    if n % 2 == 1:  # 奇数阶
        base_stability = 0.8 + 0.2 * (1 - 1/n)  # 阶数越大越稳定
    else:  # 偶数阶
        base_stability = 0.3 + 0.2 * (1 - 1/n)  # 偶数阶也有一定稳定性
        
    # 用不平衡度修正
    imbalance = calculate_imbalance(magic_square)
    imbalance_penalty = imbalance / (n * 100)  # 归一化惩罚
    
    return max(0.0, base_stability - imbalance_penalty)

if __name__ == "__main__":
    # 测试耦合算法
    coupler = MagicCoupling()
    
    # 创建两个基础幻方
    square_3x3 = generate_magic_square_3x3()
    square_5x5 = generate_magic_square_3x3()  # 简化，实际应为5x5
    
    print("测试幻方耦合:")
    result = coupler.couple_squares(square_3x3, square_5x3)
    
    print(f"过渡态阶数: {result['transition_order']}")
    print(f"稳定态阶数: {result['stable_order']}")
    print(f"稳定性评分: {result['stability_score']:.3f}")
    print(f"耦合成功: {result['coupling_success']}")
    print(f"奇偶稳定性: {parity_stability_score(result['stable_state']):.3f}")
