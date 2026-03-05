"""Material driver package — imports all concrete drivers for registry."""

from src.materials.drivers.base import MaterialDriver, MaterialSystemType
from src.materials.drivers.acoustic import AcousticMetamaterialDriver
from src.materials.drivers.olfactory import OlfactorySynthesisDriver
from src.materials.drivers.electrochromic import ElectrochromicSurfaceDriver
from src.materials.drivers.haptic import HapticSurfaceDriver
from src.materials.drivers.projection import ProjectionMappingDriver
from src.materials.drivers.thermal import PhaseChangePanelDriver
from src.materials.drivers.shape_memory import ShapeMemoryElementDriver
from src.materials.drivers.deployable_4d import Deployable4DDriver
from src.materials.drivers.bioluminescent import BioluminescentCoatingDriver

DRIVER_REGISTRY: dict[MaterialSystemType, type[MaterialDriver]] = {
    MaterialSystemType.ACOUSTIC_METAMATERIAL: AcousticMetamaterialDriver,
    MaterialSystemType.HAPTIC_SURFACE: HapticSurfaceDriver,
    MaterialSystemType.OLFACTORY_SYNTHESIS: OlfactorySynthesisDriver,
    MaterialSystemType.ELECTROCHROMIC_SURFACE: ElectrochromicSurfaceDriver,
    MaterialSystemType.PROJECTION_MAPPING: ProjectionMappingDriver,
    MaterialSystemType.PHASE_CHANGE_PANEL: PhaseChangePanelDriver,
    MaterialSystemType.SHAPE_MEMORY_ELEMENT: ShapeMemoryElementDriver,
    MaterialSystemType.DEPLOYABLE_4D: Deployable4DDriver,
    MaterialSystemType.BIOLUMINESCENT_COATING: BioluminescentCoatingDriver,
}