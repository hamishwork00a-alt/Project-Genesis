"""
核合成模拟 - 从氢到氦的宇宙核形成过程
"""

import numpy as np
from core_math import *
from particle_definitions import *
from quantum_coupling import QuantumCoupling

class NucleosynthesisSimulator:
    """核合成模拟器"""
    
    def __init__(self, temperature=1e9):  # 温度单位: K
        self.temperature = temperature
        self.coupler = QuantumCoupling()
        
    def hydrogen_fusion(self, num_reactions=100):
        """氢聚变：p + p → d + e⁺ + νₑ"""
        success_count = 0
        energy_release = []
        
        for i in range(num_reactions):
            proton = Proton()
            another_proton = Proton()
            
            # 模拟质子-质子碰撞
            result = self.coupler.couple_particles(proton, another_proton, "strong")
            
            if result['success'] and result['stability'] > 0.8:
                success_count += 1
                # 结合能估算
                binding_energy = result['stability'] * 10  # MeV量级
                energy_release.append(binding_energy)
        
        success_rate = success_count / num_reactions
        avg_energy = np.mean(energy_release) if energy_release else 0
        
        return {
            'reaction': 'p + p → d + e⁺ + νₑ',
            'success_rate': success_rate,
            'average_energy_mev': avg_energy,
            'qty_deuterium_produced': success_count
        }
    
    def deuterium_fusion(self, deuterium_list):
        """氘核融合：d + d → ³He 或 t + p"""
        helium3_count = 0
        tritium_count = 0
        
        for i in range(0, len(deuterium_list)-1, 2):
            d1 = deuterium_list[i]
            d2 = deuterium_list[i+1]
            
            result = self.coupler.couple_particles(d1, d2, "strong")
            
            if result['success']:
                # 根据稳定性决定产物
                if result['stability'] > 0.85:
                    helium3_count += 1  # d + d → ³He + n
                else:
                    tritium_count += 1   # d + d → t + p
        
        return {
            'helium3_produced': helium3_count,
            'tritium_produced': tritium_count
        }
    
    def helium_formation(self, deuterium, protons, neutrons):
        """氦形成：d + p → ³He 或 d + n → t 等路径"""
        helium4_count = 0
        
        # 简化模拟：直接组合2个质子和2个中子
        if len(protons) >= 2 and len(neutrons) >= 2:
            # 模拟α粒子形成
            alpha_candidate = create_approximate_magic_square(8)  # 氦-4使用8阶幻方
            stability = parity_stability_score(alpha_candidate)
            
            if stability > 0.7:
                helium4_count = min(len(protons)//2, len(neutrons)//2)
        
        return {
            'helium4_produced': helium4_count,
            'description': '4He (α粒子)形成'
        }
    
    def simulate_big_bang_nucleosynthesis(self, initial_hydrogen=1000):
        """模拟大爆炸核合成"""
        print("模拟大爆炸核合成")
        print("=" * 40)
        
        # 初始条件：大量质子和电子（氢）
        protons = [Proton() for _ in range(initial_hydrogen)]
        electrons = [Electron() for _ in range(initial_hydrogen)]
        
        # 步骤1: 氢聚变形成氘
        print("阶段1: 氢聚变 → 氘")
        fusion_result = self.hydrogen_fusion(len(protons)//2)
        deuterium_nuclei = [Deuteron() for _ in range(fusion_result['qty_deuterium_produced'])]
        
        print(f"  产生氘核: {len(deuterium_nuclei)}个")
        print(f"  聚变成功率: {fusion_result['success_rate']:.3f}")
        
        # 步骤2: 氘核进一步融合
        print("阶段2: 氘核融合 → ³He/氚")
        d_fusion_result = self.deuterium_fusion(deuterium_nuclei)
        
        print(f"  产生³He: {d_fusion_result['helium3_produced']}个")
        print(f"  产生氚: {d_fusion_result['tritium_produced']}个")
        
        # 步骤3: 形成氦-4
        print("阶段3: 形成氦-4")
        remaining_protons = protons[len(protons)//2:]
        neutrons = [Neutron() for _ in range(len(remaining_protons))]
        
        helium_result = self.helium_formation(deuterium_nuclei, remaining_protons, neutrons)
        
        print(f"  产生⁴He: {helium_result['helium4_produced']}个")
        
        # 计算结果丰度
        total_nuclei = initial_hydrogen
        helium4_abundance = helium_result['helium4_produced'] / total_nuclei * 100
        deuterium_abundance = len(deuterium_nuclei) / total_nuclei * 100
        
        return {
            'temperature_k': self.temperature,
            'initial_hydrogen': initial_hydrogen,
            'helium4_abundance_percent': helium4_abundance,
            'deuterium_abundance_percent': deuterium_abundance,
            'predicted_helium4': "~25%" if 20 <= helium4_abundance <= 30 else "异常",
            'consistency_with_observation': "符合" if 20 <= helium4_abundance <= 30 else "不符合"
        }

def demo_nucleosynthesis():
    """演示核合成过程"""
    simulator = NucleosynthesisSimulator(temperature=1e9)  # 10^9 K，典型核合成温度
    
    print("宇宙核合成演示")
    print("=" * 50)
    
    result = simulator.simulate_big_bang_nucleosynthesis(initial_hydrogen=1000)
    
    print(f"\n核合成结果:")
    for key, value in result.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    demo_nucleosynthesis()
