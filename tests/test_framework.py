"""
Tests for IRH Framework core functionality
"""

import numpy as np

from irh.core import IRH_Framework, IRHConstants


class TestIRHFramework:
    """Test suite for IRH_Framework class"""

    def setup_method(self):
        """Set up test framework instance"""
        self.framework = IRH_Framework(grid_resolution=10)

    def test_initialization(self):
        """Test framework initialization"""
        assert self.framework.grid_resolution == 10
        assert isinstance(self.framework.constants, IRHConstants)
        assert len(self.framework.grid_points) == 10

    def test_four_strand_laplacian(self):
        """Test Laplacian calculation"""
        field = np.random.rand(10, 10, 10)
        laplacian = self.framework.four_strand_laplacian(field, 0)

        assert laplacian.shape == field.shape
        assert not np.any(np.isnan(laplacian))
        assert not np.any(np.isinf(laplacian))

    def test_cymatic_kernel(self):
        """Test cymatic kernel computation"""
        g = np.array([0.5, 0.3, 0.7, 1.2])
        h = np.array([0.6, 0.4, 0.8, 1.1])

        kernel = self.framework.cymatic_kernel(g, h)

        assert isinstance(kernel, complex)
        # Kernel should have reasonable magnitude based on Gaussian envelope
        # For small distances, amplitude can approach 1
        assert abs(kernel) >= 0.0
        assert not np.isnan(kernel)
        assert not np.isinf(kernel)

    def test_ckm_matrix(self):
        """Test CKM matrix calculation"""
        ckm = self.framework.calculate_ckm_matrix()

        assert ckm.shape == (3, 3)
        assert ckm.dtype == complex

        # Check unitarity (CKM^† × CKM ≈ I)
        unitarity_check = np.dot(ckm.conj().T, ckm)
        identity = np.eye(3)
        assert np.allclose(unitarity_check, identity, atol=5e-3)

    def test_neutrino_oscillations(self):
        """Test neutrino oscillation calculations"""
        L = 295e3  # 295 km baseline
        E = 3.0    # 3 GeV

        probs = self.framework.neutrino_oscillations(L, E)

        # Check all probabilities are present
        required_keys = ['P_ee', 'P_emu', 'P_etau', 'P_mumu', 'P_mutau', 'P_tautau']
        for key in required_keys:
            assert key in probs

        # Check probabilities are in valid range (allow small numerical errors)
        for prob in probs.values():
            assert -1e-10 <= prob <= 1.0 + 1e-10

        # Check probability conservation
        assert np.isclose(probs['P_ee'] + probs['P_emu'] + probs['P_etau'], 1.0, atol=1e-6)

    def test_parameter_optimization(self):
        """Test parameter optimization"""
        constraints = {
            'alpha_EM': (1/137.036, 1e-8),
            'alpha_s': (0.118, 0.001),
        }

        result = self.framework.parameter_optimization(constraints)

        assert 'alpha_EM' in result
        assert 'alpha_s' in result
        assert 'cost' in result
        assert result['cost'] >= 0

    def test_experimental_proposals(self):
        """Test experimental proposal generation"""
        proposals = self.framework.generate_experimental_proposals()

        assert len(proposals) > 0

        for proposal in proposals:
            assert 'name' in proposal
            assert 'description' in proposal
            assert 'discovery_potential' in proposal
            assert 'feasibility' in proposal

            # Check discovery potential is in valid range
            assert 0 <= proposal['discovery_potential'] <= 10
            assert 0 <= proposal['feasibility'] <= 10


class TestIRHConstants:
    """Test suite for IRHConstants class"""

    def test_physical_constants(self):
        """Test physical constants are reasonable"""
        constants = IRHConstants()

        # Speed of light
        assert 2.9e8 < constants.c < 3.1e8

        # Planck constant
        assert 1e-35 < constants.hbar < 1e-33

        # Gravitational constant
        assert 6e-11 < constants.G < 7e-11

    def test_coupling_constants(self):
        """Test coupling constants"""
        constants = IRHConstants()

        # Fine structure constant
        assert 0.007 < constants.alpha_EM < 0.008

        # Strong coupling
        assert 0.1 < constants.alpha_s < 0.13

    def test_strand_couplings(self):
        """Test strand coupling strengths"""
        constants = IRHConstants()

        assert constants.g1 == 1.0
        assert constants.g2 == 1.0
        assert constants.g3 == 1.0
        assert constants.g4 == 1.0


def test_import():
    """Test that package can be imported"""
    import irh
    assert hasattr(irh, 'IRH_Framework')
    assert hasattr(irh, '__version__')
