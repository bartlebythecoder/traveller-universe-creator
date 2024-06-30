# Created on 2024-05-31
# Under construction
# Classes and Functions for Stellar bodies will go here

from dataclasses import dataclass
from enum import Enum, auto
from abc import ABC, abstractmethod
from traveller_functions import roll_dice_clean
import logging


class LuminosityClass(Enum):
    """Star Luminosity Class"""
    I = auto()
    III = auto()
    V = auto()
    D = auto()
    X = auto()


class SpectralClass(Enum):
    O = auto()
    B = auto()
    A0 = auto()
    F0 = auto()
    G0 = auto()
    K0 = auto()
    M0 = auto()
    A5 = auto()
    F5 = auto()
    G5 = auto()
    K5 = auto()
    M5 = auto()
    XX = auto()
    w = auto()


class OrbitSeparationClass(Enum):
    VeryClose = auto()
    Close = auto()
    Moderate = auto()
    Wide = auto()
    Distant = auto()


class StarDetailsStrategy(ABC):
    @abstractmethod
    def get_primary_details(self, star_details: "StarDetails") -> tuple[LuminosityClass, int, SpectralClass, int, int]:
        pass

    @abstractmethod
    def get_companion_details(self, star_details: "StarDetails") -> tuple[
        LuminosityClass, int, SpectralClass, int, int]:
        pass


class GurpsStarDetailsStrategy(StarDetailsStrategy):
    # ... your existing Gurps logic ...

    def get_primary_details(self, star_details: "StarDetails") -> tuple[
            LuminosityClass, int,
            SpectralClass, int, int]:
        lum_class, lum_roll = self.get_primary_luminosity_class(star_details)
        spec_class, spec_roll, subspec_roll = self.get_primary_spectral_class(star_details)
        return lum_class, lum_roll, spec_class, spec_roll, subspec_roll

    def get_companion_details(self, star_details: "StarDetails") -> tuple[
            LuminosityClass, int,
            SpectralClass, int, int]:
        return LuminosityClass.XX, -1, SpectralClass.XX, -1, -1

    def get_primary_luminosity_probabilities(self) -> tuple[int, int]:
        # returns the die rolls required for a lum class of III and V
        lum_iii_target = 3
        lum_v_target = 14
        return lum_iii_target, lum_v_target

    def get_primary_luminosity_class(self, star_details: "StarDetails") -> tuple[LuminosityClass, int]:
        lum_chance_iii, lum_chance_v = self.get_primary_luminosity_probabilities()
        lum_roll = roll_dice_clean((3))
        if lum_roll <= lum_chance_iii:
            rolled_lum = LuminosityClass.III
        elif lum_roll <= lum_chance_v:
            rolled_lum = LuminosityClass.V
        else:
            rolled_lum = LuminosityClass.D

        return rolled_lum, lum_roll

    def get_companion_luminosity_class(self, star_details: "StarDetails") -> tuple[LuminosityClass, int]:
        # Under construction - currently duplicates primary algorithm

        lum_chance_iii, lum_chance_v = self.get_primary_luminosity_probabilities()
        lum_roll = roll_dice_clean((3))
        if lum_roll <= lum_chance_iii:
            rolled_lum = LuminosityClass.III
        elif lum_roll <= lum_chance_v:
            rolled_lum = LuminosityClass.V
        else:
            rolled_lum = LuminosityClass.D

        return rolled_lum, lum_roll

    def get_primary_spectral_class_probabilities(self) -> tuple[int, int, int, int]:
        # returns the die rolls required for the various spectral class types
        spec_class_a_target = 4
        spec_class_f_target = 6
        spec_class_g_target = 8
        spec_class_k_target = 10
        return spec_class_a_target, spec_class_f_target, spec_class_g_target, spec_class_k_target

    def get_primary_spectral_class(self, star_details: "StarDetails") -> tuple[SpectralClass, int, int]:
        spec_a, spec_f, spec_g, spec_k = self.get_primary_spectral_class_probabilities()
        # spec_roll = roll_dice_clean((3))  # Ready for Spectral Class implementation
        # subspec_roll = roll_dice_clean((1))  # Ready for Spectral Class implementation

        spec_roll = 7
        subspec_roll = 4

        #   A function that returns the spectral class
        if spec_roll <= spec_a and subspec_roll < 4:
            spec = SpectralClass.A0
        elif spec_roll <= spec_a and subspec_roll >= 4:
            spec = SpectralClass.A5
        elif spec_roll <= spec_f and subspec_roll < 4:
            spec = SpectralClass.F0
        elif spec_roll <= spec_f and subspec_roll >= 4:
            spec = SpectralClass.F5
        elif spec_roll <= spec_g and subspec_roll < 4:
            spec = SpectralClass.G0
        elif spec_roll <= spec_g and subspec_roll >= 4:
            spec = SpectralClass.G5
        elif spec_roll <= spec_k and subspec_roll < 4:
            spec = SpectralClass.K0
        elif spec_roll <= spec_k and subspec_roll >= 4:
            spec = SpectralClass.K5
        elif subspec_roll < 4:
            spec = SpectralClass.M0
        else:
            spec = SpectralClass.M5


        return spec, spec_roll, subspec_roll


class MongooseStarDetailsStrategy(StarDetailsStrategy):

    def get_primary_details(self, star_details: "StarDetails") -> tuple[LuminosityClass, int, SpectralClass, int, int]:
        return LuminosityClass.X, -1, SpectralClass.XX, -1, -1

    def get_companion_details(self, star_details: "StarDetails") -> (
            tuple)[LuminosityClass, int, SpectralClass, int, int]:
        return LuminosityClass.X, -1, SpectralClass.XX, -1, -1


class StarDetails:
    def __init__(self, star_details_strategy: StarDetailsStrategy, location: str, companion_no: int):
        self._star_details_strategy = star_details_strategy
        self.location = location
        self.companion_no = companion_no

    def calculate_luminosity_class(self):
        if self.companion_no == 0:
            self.luminosity_class, self.lum_roll = self._star_details_strategy.get_primary_luminosity_class(self)
        else:
            self.luminosity_class, self.lum_roll = self._star_details_strategy.get_companion_luminosity_class(self)

    def calculate_spectral_class(self):
        # Now you have access to self.luminosity_class
        if self.companion_no == 0:
            self.spectral_class, self.spec_roll, self.subspec_roll = self._star_details_strategy.get_primary_spectral_class(self)
        else:
            # You might need a separate method for companions in your strategy
            pass  # Or similar logic

    def calculate_all_details(self):
        self.calculate_luminosity_class()
        self.calculate_spectral_class()


