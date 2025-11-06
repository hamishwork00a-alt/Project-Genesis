"""
Project Genesis 完整演示
展示从基本粒子到原子形成的完整过程
"""

from core_math import *
from particle_definitions import *
from quantum_coupling import QuantumCoupling

def demo_hydrogen_formation():
    """演示氢原子形成过程"""
    print("=" * 50)
    print("氢原子形成演示")
    print("=" * 50)
    
    coupler = QuantumCoupling()
    
    # 创建质子和电子
    proton = Proton()
    electron = Electron()
    
    print(f"初始粒子:")
    print(f"  - 质子: {proton.magic_square.shape[0]}阶幻方")
    print(f"  - 电子: {electron.magic_square.shape[0]}阶幻方")
    
    # 电磁力耦合形成氢原子
    print("\n开始电磁力耦合...")
    result = coupler.couple_particles(proton, electron, "electromagnetic")
    
    if result['success']:
        print(f"\n✅ 氢原子形成成功!")
        print(f"   稳定态: {result['stable_state'].shape[0]}阶幻方")
        print(f"   结合稳定性: {result['stability']:.3f}")
        print(f"   奇偶稳定性: {parity_stability_score(result['stable_state']):.3f}")
    else:
        print(f"\n❌ 氢原子形成失败")
    
    return result

def demo_particle_interactions():
    """演示不同粒子相互作用"""
    print("\n" + "=" * 50)
    print("粒子相互作用演示") 
    print("=" * 50)
    
    coupler = QuantumCoupling()
    particles = [Electron(), UpQuark(), DownQuark(), Photon()]
    
    interactions = [
        ("电子-电子", "electromagnetic"),
        ("上夸克-上夸克", "strong"), 
        ("电子-光子", "electromagnetic"),
        ("上夸克-下夸克", "strong")
    ]
    
    for interaction, force_type in interactions:
        names = interaction.split("-")
        particle_a = next(p for p in particles if p.name == names[0])
        particle_b = next(p for p in particles if p.name == names[1])
        
        print(f"\n{interaction} ({force_type}):")
        result = coupler.couple_particles(particle_a, particle_b, force_type)
        
        if result['success']:
            print(f"  ✅ 耦合成功 - 稳定性: {result['stability']:.3f}")
        else:
            print(f"  ❌ 耦合失败")

def demo_magic_square_properties():
    """演示幻方数学特性"""
    print("\n" + "=" * 50)
    print("幻方数学特性演示")
    print("=" * 50)
    
    ms3 = generate_magic_square_3x3()
    ms5 = generate_magic_square_5x5()
    
    print("3x3幻方:")
    print(ms3)
    print(f"魔数: {np.sum(ms3[0, :])}")
    print(f"奇偶稳定性: {parity_stability_score(ms3):.3f}")
    
    print("\n5x5幻方:")
    print(f"魔数: {np.sum(ms5[0, :])}") 
    print(f"奇偶稳定性: {parity_stability_score(ms5):.3f}")
    
    # 演示奇偶性约束
    print("\n奇偶性约束验证:")
    for order in [3, 4, 5, 6, 7]:
        test_square = create_approximate_magic_square(order)
        stability = parity_stability_score(test_square)
        parity = "奇数" if order % 2 == 1 else "偶数"
        print(f"  {order}阶({parity}): 稳定性 = {stability:.3f}")

if __name__ == "__main__":
    print("Project Genesis - 统一场论演示")
    print("基于幻方约束的量子引力理论框架\n")
    
    demo_magic_square_properties()
    demo_particle_interactions() 
    hydrogen_result = demo_hydrogen_formation()
    
    print("\n" + "=" * 50)
    print("演示完成!")
    print("=" * 50)
