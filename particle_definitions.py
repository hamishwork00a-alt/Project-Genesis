"""
粒子定义 - 所有基本粒子的幻方描述
"""

import numpy as np
from core_math import *

class QuantumParticle:
    """量子粒子基类"""
    
    def __init__(self, name, magic_order, quantum_numbers, stability=1.0):
        self.name = name
        self.magic_order = magic_order
        self.quantum_numbers = quantum_numbers
        self.stability = stability
        self.magic_square = self._create_magic_square()
    
    def _create_magic_square(self):
        """创建粒子的本征幻方"""
        if self.magic_order == 3:
            base = generate_magic_square_3x3()
        elif self.magic_order == 5:
            base = generate_magic_square_5x5()
        else:
            base = create_approximate_magic_square(self.magic_order)
        
        # 用量子数调制
        return self._modulate_with_quantum_numbers(base)
    
    def _modulate_with_quantum_numbers(self, base_square):
        """用量子数调制幻方"""
        modulated = base_square.astype(np.float64).copy()
        
        # 电荷调制
        if 'charge' in self.quantum_numbers:
            charge_effect = 1.0 + 0.05 * abs(self.quantum_numbers['charge'])
            modulated *= charge_effect
        
        # 自旋调制  
        if 'spin' in self.quantum_numbers:
            spin_phase = np.exp(1j * self.quantum_numbers['spin'] * np.pi)
            modulated = modulated * spin_phase.real
            
        return modulated * self.stability

# ==================== 基本粒子定义 ====================

class Electron(QuantumParticle):
    def __init__(self):
        super().__init__(
            name="电子",
            magic_order=3,
            quantum_numbers={'charge': -1, 'spin': 1/2, 'lepton_number': 1},
            stability=0.95
        )

class UpQuark(QuantumParticle):
    def __init__(self):
        super().__init__(
            name="上夸克", 
            magic_order=3,
            quantum_numbers={'charge': 2/3, 'spin': 1/2, 'baryon_number': 1/3},
            stability=0.90
        )

class DownQuark(QuantumParticle):
    def __init__(self):
        super().__init__(
            name="下夸克",
            magic_order=3, 
            quantum_numbers={'charge': -1/3, 'spin': 1/2, 'baryon_number': 1/3},
            stability=0.90
        )

class Photon(QuantumParticle):
    def __init__(self):
        super().__init__(
            name="光子",
            magic_order=4,  # 偶数阶 - 力的载体
            quantum_numbers={'charge': 0, 'spin': 1, 'mass': 0},
            stability=1.0
        )

class Proton:
    """质子 - 复合粒子示例"""
    def __init__(self):
        self.name = "质子"
        self.quantum_numbers = {'charge': 1, 'spin': 1/2, 'baryon_number': 1}
        # 质子由2个上夸克和1个下夸克组成
        self.up_quarks = [UpQuark(), UpQuark()]
        self.down_quark = DownQuark()
        self.magic_square = self._combine_quarks()
    
    def _combine_quarks(self):
        """组合夸克形成质子幻方"""
        # 简化的组合逻辑 - 实际应该使用量子耦合
        return create_approximate_magic_square(5)  # 质子为5阶幻方

if __name__ == "__main__":
    # 测试粒子定义
    electron = Electron()
    up_quark = UpQuark()
    photon = Photon()
    
    print("粒子定义测试:")
    print(f"{electron.name}: {electron.magic_order}阶幻方, 稳定性: {electron.stability}")
    print(f"{up_quark.name}: {up_quark.magic_order}阶幻方, 电荷: {up_quark.quantum_numbers['charge']}")
    print(f"{photon.name}: {photon.magic_order}阶幻方 (偶数阶力载体)")
