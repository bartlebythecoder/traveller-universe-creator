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

class LuminosityClassStrategy(ABC):
    @abstractmethod
    def get_primary_luminosity_class(self, star_details: "StarDetails") -> LuminosityClass:
        pass

    @abstractmethod
    def get_companion_luminosity_class(self, star_details: "StarDetails") -> LuminosityClass:
        pass


class GurpsLuminosityClassStrategy(LuminosityClassStrategy):
    def get_gurps_primary_luminosity_probabilities(self) -> tuple:
        # returns the die rolls required for a lum class of III and V
        lum_iii_chance = 3
        lum_v_chance = 14
        return lum_iii_chance, lum_v_chance

    def get_primary_luminosity_class(self, star_details: "StarDetails") -> tuple[LuminosityClass, int]:
        lum_chance_iii, lum_chance_v = self.get_gurps_primary_luminosity_probabilities()
        lum_roll = roll_dice_clean((3))
        if lum_roll <= lum_chance_iii:
            rolled_lum = LuminosityClass.III
        elif lum_roll <= lum_chance_v:
            rolled_lum = LuminosityClass.V
        else:
            rolled_lum = LuminosityClass.D

        return rolled_lum, lum_roll

    def get_companion_luminosity_class(self, star_details: "StarDetails") -> tuple[LuminosityClass, int]:
        primary_class = star_details.primary_luminosity_class
        lum_class_list = [LuminosityClass.I, LuminosityClass.III, LuminosityClass.V, LuminosityClass.X]

        if primary_class == LuminosityClass.D:
            star.luminosity_class = LuminosityClass.D
            spec = 'w'
        else:
            sec_lum_roll_a = roll_dice(1, 'comp lum class #1', location, conn, c)
            if sec_lum_roll_a <= 4:
                star.luminosity_class = stellar_dict["luminosity_class"]
                csd_spec_roll = roll_dice(1, 'comp spec roll', location, conn, c)
                spec = find_csd_spectral_type(csd_spec_roll, stellar_dict["spectral_type"])
            else:
                lum_class_index = lum_class_list.index(stellar_dict["luminosity_class"])
                if sec_lum_roll_a == 5:
                    lum_class_index += 1
                else:
                    lum_class_index += 2

                if lum_class_index < 3:
                    star.luminosity_class = lum_class_list[lum_class_index]
                else:
                    sec_lum_roll_b = roll_dice(1, 'comp lum class #2', location, conn, c)
                    if sec_lum_roll_b <= 4:
                        star.luminosity_class = LuminosityClass.V

                    else:
                        star.luminosity_class = LuminosityClass.D

                if star.luminosity_class == LuminosityClass.D:
                    spec = 'w'
                elif star.luminosity_class in lum_class_list:
                    csd_spec_roll = roll_dice(1, 'comp spec roll', location, conn, c)
                    spec = find_csd_spectral_type(csd_spec_roll, stellar_dict["spectral_type"])
                else:
                    star.luminosity_class = LuminosityClass.X
                    spec = 'X'

        return rolled_lum, lum_roll


class MongooseLuminosityClassStrategy(LuminosityClassStrategy):
    def get_mongoose_primary_luminosity_probabilities(self) -> tuple:
        # returns the die rolls required for a lum class of III and V
        lum_iii_chance = 3
        lum_v_chance = 14
        return lum_iii_chance, lum_v_chance

    def get_primary_luminosity_class(self, star_details: "StarDetails") -> tuple[LuminosityClass, int]:
        lum_chance_iii, lum_chance_v = self.get_mongoose_primary_luminosity_probabilities()
        lum_roll = roll_dice_clean((3))
        if lum_roll <= lum_chance_iii:
            rolled_lum = LuminosityClass.III
        elif lum_roll <= lum_chance_v:
            rolled_lum = LuminosityClass.V
        else:
            rolled_lum = LuminosityClass.D

        return rolled_lum, lum_roll

    def get_companion_luminosity_class(self, star_details: "StarDetails") -> tuple[LuminosityClass, int]:
        lum_chance_iii, lum_chance_v = self.get_mongoose_primary_luminosity_probabilities()
        lum_roll = roll_dice_clean((3))
        if lum_roll <= lum_chance_iii:
            rolled_lum = LuminosityClass.III
        elif lum_roll <= lum_chance_v:
            rolled_lum = LuminosityClass.V
        else:
            rolled_lum = LuminosityClass.D

        return rolled_lum, lum_roll

class StarDetails:
    def __init__(self, luminosity_class_strategy: LuminosityClassStrategy,
                       companion_no: int = 0,
                       primary_luminosity_class = LuminosityClass.X):
        self._luminosity_class_strategy = luminosity_class_strategy
        self.companion_no = companion_no
        self.primary_luminosity_class = primary_luminosity_class

    def calculate_luminosity_class(self) -> tuple[LuminosityClass, int]:
        if not hasattr(self, "luminosity_class") & self.companion_no ==0:
            self.luminosity_class, self.roll = self._luminosity_class_strategy.get_primary_luminosity_class(self)
            return self.luminosity_class, self.roll
        else:
            self.luminosity_class, self.roll = self._luminosity_class_strategy.get_companion_luminosity_class(self)
            return self.luminosity_class, self.roll


