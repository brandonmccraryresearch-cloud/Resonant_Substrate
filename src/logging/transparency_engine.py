"""
Transparency Engine for IRH v24.0 Computational Framework

This module provides the TransparencyEngine class for logging computational
derivations with complete theoretical provenance. All computations that derive
physical observables MUST use this engine to emit step-by-step derivations,
component breakdowns, and validation checks.

The Transparency Engine ensures that every numerical output includes:
1. Complete theoretical provenance chain
2. Manuscript section and equation references  
3. Uncertainty decomposition by source
4. Dimensional consistency verification
5. Known limit validation

References
----------
IRH v24.0 Manuscript, Section 8.3: Transparency Requirements
.github/copilot-instructions.md: Theoretical Correspondence Mandate
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import numpy as np


@dataclass
class ProvenanceInfo:
    """Complete provenance information for a computation."""

    manuscript_section: str
    equation_number: Optional[str] = None
    formula_latex: Optional[str] = None
    input_sources: List[str] = field(default_factory=list)
    computational_method: str = "numerical"
    assumptions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ValidationInfo:
    """Validation checks performed on computed value."""

    dimensional_consistency: bool = True
    known_limits_checked: List[str] = field(default_factory=list)
    error_bounds_computed: bool = False
    convergence_verified: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class ComputationRecord:
    """Complete record of a single computation."""

    name: str
    value: Optional[Union[float, complex, np.ndarray]]
    units: Optional[str] = None
    uncertainty: Optional[float] = None
    components: Dict[str, Any] = field(default_factory=dict)
    provenance: Optional[ProvenanceInfo] = None
    validation: Optional[ValidationInfo] = None
    notes: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            'name': self.name,
            'value': self._serialize_value(self.value),
            'units': self.units,
            'uncertainty': self.uncertainty,
            'components': self.components,
            'notes': self.notes
        }
        
        if self.provenance:
            result['provenance'] = self.provenance.to_dict()
        
        if self.validation:
            result['validation'] = self.validation.to_dict()
        
        return result
    
    def _serialize_value(self, value: Any) -> Any:
        """Serialize numpy arrays and complex numbers."""
        if isinstance(value, np.ndarray):
            return value.tolist()
        elif isinstance(value, complex):
            return {'real': value.real, 'imag': value.imag}
        elif isinstance(value, (np.integer, np.floating)):
            return float(value)
        else:
            return value


class TransparencyEngine:
    """
    Engine for transparent, traceable computational derivations.
    
    The TransparencyEngine maintains a complete audit trail of all computations,
    ensuring that every derived quantity includes:
    - Theoretical reference (manuscript section, equation)
    - Input provenance
    - Intermediate steps
    - Validation checks
    - Error bounds
    
    This implements the "zero tolerance for black box computations" mandate
    from the IRH v24.0 Theoretical Correspondence Protocol.
    
    Examples
    --------
    >>> engine = TransparencyEngine()
    >>> with engine.computation("fine_structure_constant") as comp:
    ...     comp.set_provenance(
    ...         manuscript_section="Section 3.4",
    ...         equation_number="Eq. 3.7",
    ...         formula_latex=r"\alpha^{-1} = Z \times (2\pi^2/V_{eff})"
    ...     )
    ...     comp.add_component("Z_bare", 121.8)
    ...     comp.add_component("V_eff", 17.8)
    ...     result = 121.8 * (2 * np.pi**2 / 17.8)
    ...     comp.set_result(result, uncertainty=0.001)
    ...     comp.validate(dimensional_consistency=True)
    
    References
    ----------
    IRH v24.0, Section 8.3: Computational Transparency Requirements
    """

    def __init__(self, log_file: Optional[Path] = None, verbose: bool = False):
        """
        Initialize TransparencyEngine.
        
        Parameters
        ----------
        log_file : Path, optional
            Path to write computation logs
        verbose : bool, optional
            Enable verbose console output
        """
        self.records: List[ComputationRecord] = []
        self.log_file = log_file
        self.verbose = verbose
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger('IRH.TransparencyEngine')
        logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[TRANSPARENCY] %(levelname)s: %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def computation(self, name: str) -> 'ComputationContext':
        """
        Create a computation context for transparent derivation.
        
        Parameters
        ----------
        name : str
            Name of the quantity being computed
            
        Returns
        -------
        ComputationContext
            Context manager for the computation
        """
        return ComputationContext(self, name)
    
    def record_computation(self, record: ComputationRecord) -> None:
        """
        Store a computation record.
        
        Parameters
        ----------
        record : ComputationRecord
            Complete record of the computation
        """
        self.records.append(record)
        
        if self.verbose:
            self.logger.info(f"Computed {record.name} = {record.value}")
            if record.provenance:
                self.logger.debug(
                    f"  Reference: {record.provenance.manuscript_section}"
                )
        
        # Write to log file if configured
        if self.log_file:
            self._write_log(record)
    
    def _write_log(self, record: ComputationRecord) -> None:
        """Write record to log file."""
        try:
            with open(self.log_file, 'a') as f:
                json.dump(record.to_dict(), f)
                f.write('\n')
        except Exception as e:
            self.logger.error(f"Failed to write log: {e}")
    
    def export_records(self, output_path: Path) -> None:
        """
        Export all computation records to JSON.
        
        Parameters
        ----------
        output_path : Path
            Path to write JSON export
        """
        with open(output_path, 'w') as f:
            json.dump(
                [record.to_dict() for record in self.records],
                f,
                indent=2
            )
        
        self.logger.info(f"Exported {len(self.records)} records to {output_path}")


class ComputationContext:
    """Context manager for a single transparent computation."""

    def __init__(self, engine: TransparencyEngine, name: str):
        self.engine = engine
        self.name = name
        self.record = ComputationRecord(name=name, value=None)
        
    def __enter__(self):
        """Enter computation context."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit computation context and record result."""
        if exc_type is None:
            self.engine.record_computation(self.record)
        return False
    
    def set_provenance(
        self,
        manuscript_section: str,
        equation_number: Optional[str] = None,
        formula_latex: Optional[str] = None,
        input_sources: Optional[List[str]] = None,
        computational_method: str = "numerical",
        assumptions: Optional[List[str]] = None
    ) -> None:
        """Set provenance information for this computation."""
        self.record.provenance = ProvenanceInfo(
            manuscript_section=manuscript_section,
            equation_number=equation_number,
            formula_latex=formula_latex,
            input_sources=input_sources or [],
            computational_method=computational_method,
            assumptions=assumptions or []
        )
    
    def add_component(self, name: str, value: Any) -> None:
        """Add an intermediate computation component."""
        self.record.components[name] = value
    
    def set_result(
        self,
        value: Union[float, complex, np.ndarray],
        units: Optional[str] = None,
        uncertainty: Optional[float] = None
    ) -> None:
        """Set the final computed result."""
        self.record.value = value
        self.record.units = units
        self.record.uncertainty = uncertainty
    
    def validate(
        self,
        dimensional_consistency: bool = True,
        known_limits: Optional[List[str]] = None,
        error_bounds_computed: bool = False,
        convergence_verified: bool = False
    ) -> None:
        """Record validation checks performed."""
        self.record.validation = ValidationInfo(
            dimensional_consistency=dimensional_consistency,
            known_limits_checked=known_limits or [],
            error_bounds_computed=error_bounds_computed,
            convergence_verified=convergence_verified
        )
    
    def add_note(self, note: str) -> None:
        """Add a note about this computation."""
        self.record.notes.append(note)


# Global singleton instance
_default_engine: Optional[TransparencyEngine] = None


def get_transparency_engine() -> TransparencyEngine:
    """
    Get the default TransparencyEngine instance.
    
    Returns
    -------
    TransparencyEngine
        The default engine instance
    """
    global _default_engine
    if _default_engine is None:
        _default_engine = TransparencyEngine()
    return _default_engine


def reset_transparency_engine() -> None:
    """Reset the default engine (useful for testing)."""
    global _default_engine
    _default_engine = None
