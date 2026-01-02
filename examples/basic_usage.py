"""
Example: Basic IRH Framework Usage

This script demonstrates the basic usage of the IRH computational framework.
"""

import numpy as np
from irh import IRH_Framework


def main():
    print("=" * 60)
    print("Resonant Substrate: IRH Framework Example")
    print("=" * 60)
    print()
    
    # Initialize framework
    print("Initializing IRH Framework...")
    framework = IRH_Framework(grid_resolution=20)
    print(f"✓ Framework initialized with resolution: {framework.grid_resolution}")
    print()
    
    # Calculate CKM matrix
    print("Computing CKM matrix...")
    ckm = framework.calculate_ckm_matrix()
    print("✓ CKM Matrix (3x3 complex):")
    print(np.abs(ckm))  # Print magnitudes
    print()
    
    # Compute neutrino oscillations
    print("Computing neutrino oscillations...")
    L = 295e3  # T2K baseline (295 km)
    E = 0.6    # Energy (GeV)
    probs = framework.neutrino_oscillations(L, E)
    print(f"✓ Oscillation probabilities at L={L/1e3:.0f} km, E={E} GeV:")
    for flavor, prob in probs.items():
        print(f"  {flavor}: {prob:.4f}")
    print()
    
    # Test field solver with small grid
    print("Testing master equation solver...")
    initial = {
        'strand1': np.random.rand(10, 10, 10) * 0.1,
        'strand2': np.random.rand(10, 10, 10) * 0.1,
        'strand3': np.random.rand(10, 10, 10) * 0.1,
        'strand4': np.random.rand(10, 10, 10) * 0.1,
    }
    
    _ = framework.solve_master_equation(
        initial,
        max_iterations=100,
        tolerance=1e-3
    )
    print("✓ Master equation solved")
    print()
    
    # Parameter optimization
    print("Testing parameter optimization...")
    constraints = {
        'alpha_EM': (1/137.036, 1e-6),
        'alpha_s': (0.118, 0.001),
        'Omega_DM_Omega_b': (5.33, 0.1)
    }
    
    optimized = framework.parameter_optimization(constraints)
    print("✓ Optimized parameters:")
    for param, value in optimized.items():
        if param != 'cost':
            print(f"  {param}: {value:.6f}")
    print(f"  Optimization cost: {optimized['cost']:.6e}")
    print()
    
    # Generate experimental proposals
    print("Generating experimental proposals...")
    proposals = framework.generate_experimental_proposals()
    print(f"✓ Generated {len(proposals)} experimental proposals")
    print()
    print("Top 3 proposals by discovery potential:")
    for i, prop in enumerate(proposals[:3], 1):
        print(f"\n{i}. {prop['name']}")
        print(f"   Discovery Potential: {prop['discovery_potential']}/10")
        print(f"   Feasibility: {prop['feasibility']}/10")
        print(f"   Cost: {prop['cost_estimate']}")
        print(f"   Timeline: {prop['timeline']}")
    
    print()
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
