"""
基本粒子的本征幻方定义
为每个已知基本粒子分配幻方参数
"""

import numpy as np
from mathematics.magic_square_core import generate_magic_square_3x3

class IntrinsicMagicSquare:
    """粒子的本征幻方类"""
    
    def __init__(self, particle_type, magic_order, quantum_numbers, stability_factor=1.0):
        self.particle_type = particle_type
        self.magic_order = magic_order  # 幻方阶数
        self.quantum_numbers = quantum_numbers  # 量子数字典
        self.stability_factor = stability_factor
        self._generate_intrinsic_square()
    
    def _generate_intrinsic_square(self):
        """根据粒子类型生成本征幻方"""
        # 这里使用简化的生成方法，实际应根据量子数精确构造
        if self.magic_order == 3:
            base_square = generate_magic_square_3x3()
        else:
            # 对于更高阶，创建近似的幻方结构
            base_square = np.random.rand(self.magic_order, self.magic_order)
            # 调整使其接近幻方条件
            
        # 用量子数"调制"基础幻方
        self.magic_square = self._modulate_with_quantum_numbers(base_square)
    
    def _modulate_with_quantum_numbers(self, base_square):
        """用量子数调制幻方结构"""
        modulated = base_square.copy()
        
        # 用电荷调制
        if 'charge' in self.quantum_numbers:
            charge_factor = 1.0 + 0.1 * abs(self.quantum_numbers['charge'])
            modulated *= charge_factor
            
        # 用自旋调制
        if 'spin' in self.quantum_numbers:
            spin_phase = np.exp(1j * self.quantum_numbers['spin'] * np.pi)
            modulated = modulated * spin_phase.real
            
        return modulated

# 基本粒子的本征幻方定义
PARTICLE_MAGIC_DEFINITIONS = {
    # 轻子
    'electron': {
        'magic_order': 3,
        'quantum_numbers': {'charge': -1, 'spin': 1/2, 'lepton_number': 1},
        'stability_factor': 0.95
    },
    'muon': {
        'magic_order': 5, 
        'quantum_numbers': {'charge': -1, 'spin': 1/2, 'lepton_number': 1},
        'stability_factor': 0.15  # 不稳定
    },
    'tau': {
        'magic_order': 7,
        'quantum_numbers': {'charge': -1, 'spin': 1/2, 'lepton_number': 1},
        'stability_factor': 0.05  # 更不稳定
    },
    
    # 夸克
    'up_quark': {
        'magic_order': 3,
        'quantum_numbers': {'charge': 2/3, 'spin': 1/2, 'baryon_number': 1/3},
        'stability_factor': 0.90
    },
    'down_quark': {
        'magic_order': 3,
        'quantum_numbers': {'charge': -1/3, 'spin': 1/2, 'baryon_number': 1/3},
        'stability_factor': 0.90
    },
    
    # 规范玻色子
    'photon': {
        'magic_order': 4,  # 偶数阶，反映其作为力的载体
        'quantum_numbers': {'charge': 0, 'spin': 1, 'mass': 0},
        'stability_factor': 1.0
    },
    'gluon': {
        'magic_order': 4,
        'quantum_numbers': {'charge': 0, 'spin': 1, 'mass': 0},
        'stability_factor': 1.0
    }
}

def get_particle_magic_square(particle_name):
    """获取指定粒子的本征幻方"""
    if particle_name not in PARTICLE_MAGIC_DEFINITIONS:
        raise ValueError(f"未知粒子: {particle_name}")
    
    definition = PARTICLE_MAGIC_DEFINITIONS[particle_name]
    return IntrinsicMagicSquare(
        particle_name,
        definition['magic_order'],
        definition['quantum_numbers'],
        definition['stability_factor']
    )

# 测试代码
if __name__ == "__main__":
    electron = get_particle_magic_square('electron')
    photon = get_particle_magic_square('photon')
    
    print("电子本征幻方:")
    print(f"阶数: {electron.magic_order} (奇数)")
    print(f"稳定性因子: {electron.stability_factor}")
    print("幻方形状:", electron.magic_square.shape)
    
    print("\n光子本征幻方:")
    print(f"阶数: {photon.magic_order} (偶数 - 力的载体)")
    print(f"稳定性因子: {photon.stability_factor}")
