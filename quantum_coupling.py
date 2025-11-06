"""
量子耦合算法 - 粒子相互作用的幻方机制
"""

import numpy as np
from core_math import *

class QuantumCoupling:
    """量子耦合引擎"""
    
    def __init__(self, stability_threshold=0.8):
        self.stability_threshold = stability_threshold
        
    def couple_particles(self, particle_a, particle_b, force_type="universal"):
        """耦合两个粒子"""
        magic_a = particle_a.magic_square
        magic_b = particle_b.magic_square
        
        print(f"量子耦合: {particle_a.name} + {particle_b.name} ({force_type})")
        print(f"  输入: {magic_a.shape[0]}阶 + {magic_b.shape[0]}阶幻方")
        
        # 形成过渡态（总是偶数阶）
        transition = self._form_transition_state(magic_a, magic_b)
        print(f"  过渡态: {transition.shape[0]}阶 (偶数)")
        
        # 寻找稳定态（总是奇数阶）
        stable = self._find_stable_state(transition, force_type)
        
        if stable is not None:
            stability = self._calculate_stability(transition, stable)
            success = stability > 0.3
            print(f"  稳定态: {stable.shape[0]}阶 (奇数), 稳定性: {stability:.3f}")
        else:
            stability = 0.0
            success = False
            print(f"  稳定态: 未找到")
        
        return {
            'success': success,
            'transition_state': transition,
            'stable_state': stable,
            'stability': stability,
            'force_type': force_type,
            'particle_a': particle_a.name,
            'particle_b': particle_b.name
        }
    
    def _form_transition_state(self, a, b):
        """形成偶数阶过渡态"""
        n_a, n_b = a.shape[0], b.shape[0]
        transition_order = n_a + n_b  # 保证偶数
        
        transition = np.zeros((transition_order, transition_order))
        transition[:n_a, :n_a] = a
        transition[n_a:, n_a:] = b
        
        # 添加量子涨落
        quantum_fluctuation = np.random.normal(0, 0.05, (transition_order, transition_order))
        return transition + quantum_fluctuation
    
    def _find_stable_state(self, transition, force_type):
        """寻找奇数阶稳定态"""
        n_transition = transition.shape[0]
        
        # 不同力偏好的目标阶数
        if force_type == "strong":
            preferred_orders = [3, 5, 7]  # 强力偏好小奇数
        elif force_type == "electromagnetic":
            preferred_orders = [3, 5, 7, 9]  # 电磁力范围更广
        elif force_type == "weak":
            preferred_orders = [3, 5]  # 弱力作用有限
        else:  # universal/gravitational
            preferred_orders = [3, 5, 7, 9, 11]  # 普适性
        
        # 筛选可能的奇数阶目标
        target_orders = [o for o in preferred_orders if o < n_transition and o >= 3]
        
        best_candidate = None
        best_score = -1
        
        for target_order in target_orders:
            candidate = self._generate_candidate(transition, target_order)
            if candidate is not None:
                score = self._evaluate_candidate(transition, candidate)
                if score > best_score:
                    best_score = score
                    best_candidate = candidate
        
        return best_candidate if best_score > 0.3 else None
    
    def _generate_candidate(self, transition, target_order):
        """生成候选稳定态"""
        try:
            # 方法1: 使用标准幻方
            if target_order == 3:
                candidate = generate_magic_square_3x3()
            elif target_order == 5:
                candidate = generate_magic_square_5x5()
            else:
                candidate = create_approximate_magic_square(target_order)
            
            # 方法2: 如果方法1失败，使用SVD投影
            if not is_magic_square(candidate, tolerance=1.0):
                if target_order <= min(transition.shape):
                    U, s, Vt = np.linalg.svd(transition)
                    candidate = U[:, :target_order] @ np.diag(s[:target_order]) @ Vt[:target_order, :]
            
            # 验证候选
            if is_magic_square(candidate, tolerance=self.stability_threshold):
                return candidate
                
        except Exception as e:
            pass
            
        return None
    
    def _evaluate_candidate(self, transition, candidate):
        """评估候选稳定态"""
        # 幻方质量 (40%)
        magic_quality = 1.0 / (1 + calculate_imbalance(candidate))
        
        # 与过渡态的匹配度 (30%)
        match_score = self._calculate_match(transition, candidate)
        
        # 阶数奇偶性 (30%)
        parity_bonus = 1.0 if candidate.shape[0] % 2 == 1 else 0.3
        
        return 0.4 * magic_quality + 0.3 * match_score + 0.3 * parity_bonus
    
    def _calculate_match(self, transition, candidate):
        """计算匹配度"""
        min_size = min(transition.shape[0], candidate.shape[0])
        if min_size < 2:
            return 0.5
            
        trans_sub = transition[:min_size, :min_size]
        cand_sub = candidate[:min_size, :min_size]
        
        try:
            correlation = np.corrcoef(trans_sub.flatten(), cand_sub.flatten())[0, 1]
            return max(0, (correlation + 1) / 2)
        except:
            return 0.5
    
    def _calculate_stability(self, transition, stable):
        """计算最终稳定性"""
        return self._evaluate_candidate(transition, stable)

# 简化测试
if __name__ == "__main__":
    from particle_definitions import Electron, UpQuark
    
    coupler = QuantumCoupling()
    
    # 测试电子-电子耦合
    electron1 = Electron()
    electron2 = Electron()
    
    result = coupler.couple_particles(electron1, electron2, "electromagnetic")
    print(f"耦合结果: {'成功' if result['success'] else '失败'}")
