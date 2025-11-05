"""
将基本相互作用重新解释为幻方耦合规则
"""

import numpy as np
from mathematics.magic_coupling import MagicCoupling, parity_stability_score

class ForceCouplingRules:
    """基本力的幻方耦合规则"""
    
    def __init__(self):
        self.coupler = MagicCoupling()
        
        # 定义各力的耦合强度范围
        self.force_strengths = {
            'strong': 1.0,      # 强相互作用
            'electromagnetic': 0.1,  # 电磁力
            'weak': 0.01,       # 弱相互作用  
            'gravitational': 1e-39  # 引力
        }
        
        # 各力的作用距离特征（幻方耦合的"范围"）
        self.force_ranges = {
            'strong': 1,        # 短程
            'electromagnetic': 100,  # 长程
            'weak': 0.1,        # 很短程
            'gravitational': 10000  # 无限远
        }
    
    def apply_force_coupling(self, particle_a, particle_b, force_type):
        """
        应用特定类型的力耦合
        
        Args:
            particle_a, particle_b: 要耦合的粒子
            force_type: 力类型 ('strong', 'electromagnetic', 'weak', 'gravitational')
            
        Returns:
            dict: 耦合结果
        """
        strength = self.force_strengths.get(force_type, 0.01)
        
        # 获取粒子的本征幻方
        magic_a = particle_a.magic_square
        magic_b = particle_b.magic_square
        
        # 应用力特定的耦合规则
        if force_type == 'strong':
            return self._strong_force_coupling(magic_a, magic_b, strength)
        elif force_type == 'electromagnetic':
            return self._em_force_coupling(magic_a, magic_b, strength)
        elif force_type == 'weak':
            return self._weak_force_coupling(magic_a, magic_b, strength)
        elif force_type == 'gravitational':
            return self._gravity_coupling(magic_a, magic_b, strength)
        else:
            return self.coupler.couple_squares(magic_a, magic_b, strength)
    
    def _strong_force_coupling(self, a, b, strength):
        """强相互作用耦合规则 - 形成最稳定的结合"""
        # 强力的特点是形成稳定的奇数阶结合
        result = self.coupler.couple_squares(a, b, strength)
        
        # 强力偏好3阶和5阶幻方（对应最稳定的核子结合）
        if result['stable_state'] is not None:
            stable_order = result['stable_state'].shape[0]
            if stable_order in [3, 5]:  # 这些阶数特别稳定
                result['stability_score'] = min(1.0, result['stability_score'] + 0.3)
                
        return result
    
    def _em_force_coupling(self, a, b, strength):
        """电磁相互作用耦合规则 - 依赖于电荷"""
        # 电磁力可以形成稳定结合，但强度较弱
        result = self.coupler.couple_squares(a, b, strength)
        
        # 电磁力允许偶数和奇数阶的稳定结合
        # 这解释了为什么原子和分子都能稳定存在
        return result
    
    def _weak_force_coupling(self, a, b, strength):
        """弱相互作用耦合规则 - 导致幻方阶数变化"""
        result = self.coupler.couple_squares(a, b, strength)
        
        # 弱力的特点是改变幻方的"味"（flavor）
        # 这对应着粒子类型的改变
        if result['stable_state'] is not None:
            # 弱力作用后，稳定态的阶数可能发生变化
            # 这对应着β衰变等过程
            result['flavor_changed'] = True
        else:
            result['flavor_changed'] = False
            
        return result
    
    def _gravity_coupling(self, a, b, strength):
        """引力耦合规则 - 最弱但普适的耦合"""
        # 引力耦合很弱，但总是存在
        result = self.coupler.couple_squares(a, b, strength)
        
        # 引力不要求形成稳定的奇数阶结合
        # 它更像是背景级的连续耦合
        result['gravity_specific'] = {
            'universal': True,
            'always_attractive': True,
            'couples_even_unstable': True
        }
        
        return result
    
    def predict_binding_energy(self, coupling_result):
        """根据耦合结果预测结合能"""
        if coupling_result['stable_state'] is None:
            return 0.0  # 无稳定结合
            
        # 结合能正比于稳定性评分和幻方阶数
        stability = coupling_result['stability_score']
        order = coupling_result['stable_order']
        
        # 经验公式：结合能 ~ 稳定性 * log(阶数)
        binding_energy = stability * np.log(order + 1)
        
        return binding_energy

# 力的统一描述
class UnifiedForceTheory:
    """基于幻方耦合的力统一理论"""
    
    def __init__(self):
        self.rules = ForceCouplingRules()
        
    def unify_forces_at_high_energy(self, energy_scale):
        """
        在特定能标下统一力
        
        Args:
            energy_scale: 能标 (GeV)
            
        Returns:
            dict: 统一力的参数
        """
        # 随着能标升高，力的强度收敛
        if energy_scale > 1e15:  # GUT能标
            return {
                'unified': True,
                'effective_strength': 0.5,
                'magic_order_preference': [3, 7, 11]  # 大质数阶数
            }
        else:
            return {
                'unified': False,
                'forces': self.rules.force_strengths
            }

# 测试代码
if __name__ == "__main__":
    from physics.particles.intrinsic_magic_squares.particle_magic_definitions import get_particle_magic_square
    
    # 创建测试粒子
    electron = get_particle_magic_square('electron')
    up_quark = get_particle_magic_square('up_quark')
    
    rules = ForceCouplingRules()
    
    print("电磁力耦合测试 (电子-电子):")
    em_result = rules.apply_force_coupling(electron, electron, 'electromagnetic')
    print(f"稳定态阶数: {em_result['stable_order']}")
    print(f"稳定性: {em_result['stability_score']:.3f}")
    print(f"结合能: {rules.predict_binding_energy(em_result):.3f}")
    
    print("\n强力耦合测试 (上夸克-上夸克):")
    strong_result = rules.apply_force_coupling(up_quark, up_quark, 'strong')
    print(f"稳定态阶数: {strong_result['stable_order']}")
    print(f"稳定性: {strong_result['stability_score']:.3f}")
    print(f"结合能: {rules.predict_binding_energy(strong_result):.3f}")
