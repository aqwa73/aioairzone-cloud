"""Airzone Cloud API Device."""

from __future__ import annotations

from abc import abstractmethod
import logging
from typing import TYPE_CHECKING, Any

from .common import OperationMode, parse_bool, parse_int, parse_str, parse_float
from .const import (
    API_AQ_ACTIVE,
    API_AQ_PM_1,
    API_AQ_PM_2P5,
    API_AQ_PM_10,
    API_AQ_CO2,
    API_AQ_TVOC,
    API_AQ_HUMIDITY,
    API_AQ_TEMP,
    API_AQ_TEMP_CELSIUS,
    API_AQ_PRESENT,
    API_AQ_QUALITY,
    API_AQ_QUALITY_LEVELS,
    API_AQ_SCORE,
    API_AUTO_MODE,
    API_CONFIG,
    API_DEVICE_ID,
    API_DOUBLE_SET_POINT,
    API_DUAL_SP_CONF,
    API_ERRORS,
    API_IS_CONNECTED,
    API_META,
    API_MODE,
    API_MODE_AVAIL,
    API_SIMULATOR_MODE,
    API_SYSTEM_NUMBER,
    API_WARNINGS,
    API_WS_CONNECTED,
    AZD_AQ_ACTIVE,
    AZD_AQ_QUALITY,
    AZD_AQ_SCORE,
    AZD_AQ_PM_1,
    AZD_AQ_PM_2P5,
    AZD_AQ_PM_10,
    AZD_AQ_CO2,
    AZD_AQ_TVOC,
    AZD_AQ_HUMIDITY,
    AZD_AQ_TEMP,
    AZD_AQ_PRESENT,

    AZD_AVAILABLE,
    AZD_DOUBLE_SET_POINT,
    AZD_DUAL_SP_CONF,
    AZD_ERRORS,
    AZD_ID,
    AZD_INSTALLATION,
    AZD_IS_CONNECTED,
    AZD_MODE,
    AZD_MODE_AUTO,
    AZD_MODES,
    AZD_NAME,
    AZD_PROBLEMS,
    AZD_SIMULATOR_MODE,
    AZD_WARNINGS,
    AZD_WEBSERVER,
    AZD_WS_CONNECTED,
)
from .entity import Entity, EntityUpdate

if TYPE_CHECKING:
    from .air_quality import AirQuality

_LOGGER = logging.getLogger(__name__)


class Device(Entity):
    """Airzone Cloud Device."""

    def __init__(self, inst_id: str, ws_id: str, device_data: dict[str, Any]):
        """Airzone Cloud Device init."""
        super().__init__()

        self.air_quality: AirQuality | None = None
        self.auto_mode: OperationMode | None = None
        self.aq_active: bool | None = None
        self.aq_pm_1: int | None = None
        self.aq_pm_2p5: int | None = None
        self.aq_pm_10: int | None = None
        self.aq_co2: int | None = None
        self.aq_tvoc: int | None = None
        self.aq_humidity: int | None = None
        self.aq_temp: float | None = None
        self.aq_present: bool | None = None
        self.aq_quality: str | None = None
        self.aq_score: int | None = None
        self.double_set_point: bool | None = None
        self.dual_sp_conf: bool | None = None
        self.errors: list[str] = []
        self.id = str(device_data[API_DEVICE_ID])
        self.installation_id = inst_id
        self.mode: OperationMode | None = None
        self.modes: list[OperationMode] = []
        self.name: str = "Device"
        self.simulator_mode: bool | None = None
        self.warnings: list[str] = []
        self.webserver_id = ws_id
        self.ws_connected: bool = True

        is_connected = parse_bool(device_data.get(API_IS_CONNECTED))
        if is_connected is not None:
            self.is_connected = is_connected
        else:
            self.is_connected = True

    def sub_data(self, device_data: dict[str, Any]) -> dict[str, Any]:
        """Get Device sub data."""
        if API_META in device_data:
            meta: dict[str, Any] = device_data.get(API_META) or {}
            if API_SYSTEM_NUMBER in meta:
                return meta

        if API_CONFIG in device_data:
            config: dict[str, Any] = device_data.get(API_CONFIG) or {}
            if API_SYSTEM_NUMBER in config:
                return config

        return device_data

    def data(self) -> dict[str, Any]:
        """Return Device data."""
        data: dict[str, Any] = {
            AZD_AVAILABLE: self.get_available(),
            AZD_DOUBLE_SET_POINT: self.get_double_set_point(),
            AZD_ID: self.get_id(),
            AZD_INSTALLATION: self.get_installation(),
            AZD_IS_CONNECTED: self.get_is_connected(),
            AZD_NAME: self.get_name(),
            AZD_PROBLEMS: self.get_problems(),
            AZD_WEBSERVER: self.get_webserver(),
            AZD_WS_CONNECTED: self.get_ws_connected(),
        }

        aq_active = self.get_aq_active()
        if aq_active is not None:
            data[AZD_AQ_ACTIVE] = aq_active

        aq_quality = self.get_aq_quality()
        if aq_quality is not None:
            for key, value in API_AQ_QUALITY_LEVELS.items():
                if aq_quality == key:
                    data[AZD_AQ_QUALITY] = value

        aq_score = self.get_aq_score()
        if aq_score is not None:
            data[AZD_AQ_SCORE] = aq_score

        aq_pm_1 = self.get_aq_pm_1()
        if aq_pm_1 is not None:
            data[AZD_AQ_PM_1] = aq_pm_1

        aq_pm_2p5 = self.get_aq_pm_2p5()
        if aq_pm_2p5 is not None:
            data[AZD_AQ_PM_2P5] = aq_pm_2p5

        aq_pm_10 = self.get_aq_pm_10()
        if aq_pm_10 is not None:
            data[AZD_AQ_PM_10] = aq_pm_10

        aq_co2 = self.get_aq_co2()
        if aq_co2 is not None:
            data[AZD_AQ_CO2] = aq_co2

        aq_tvoc = self.get_aq_tvoc()
        if aq_tvoc is not None:
            data[AZD_AQ_TVOC] = aq_tvoc

        aq_humidity = self.get_aq_humidity()
        if aq_humidity is not None:
            data[AZD_AQ_HUMIDITY] = aq_humidity

        aq_temp = self.get_aq_temp()
        if aq_temp is not None:
            data[AZD_AQ_TEMP] = aq_temp

        aq_present = self.get_aq_present()
        if aq_present is not None:
            data[AZD_AQ_PRESENT] = aq_present

        dual_sp_conf = self.get_dual_sp_conf()
        if dual_sp_conf is not None:
            data[AZD_DUAL_SP_CONF] = dual_sp_conf

        errors = self.get_errors()
        if len(errors) > 0:
            data[AZD_ERRORS] = errors

        mode = self.get_mode()
        if mode is not None:
            data[AZD_MODE] = mode

        mode_auto = self.get_mode_auto()
        if mode_auto is not None:
            data[AZD_MODE_AUTO] = mode_auto

        modes = self.get_modes()
        if modes is not None:
            data[AZD_MODES] = modes

        simulator_mode = self.get_simulator_mode()
        if simulator_mode is not None:
            data[AZD_SIMULATOR_MODE] = simulator_mode

        warnings = self.get_warnings()
        if len(warnings) > 0:
            data[AZD_WARNINGS] = warnings

        return data

    def get_aq_active(self) -> bool | None:
        """Return HVAC device Air Quality active status."""
        if self.air_quality is not None:
            return self.air_quality.aq_active
        return self.aq_active

    def get_aq_quality(self) -> str | None:
        """Return HVAC device Air Quality quality."""
        if self.air_quality is not None:
            return self.air_quality.aq_quality
        return self.aq_quality

    def get_aq_status(self) -> int | None:
        """Return HVAC device Air Quality index."""
        aq_status = self.get_aq_status()
        if aq_status is not None:
            for key, value in API_AQ_STATUS.items():
                if aq_status == key:
                    return value
        return None

    def get_aq_score(self) -> int | None:
        """Return HVAC device Air Quality SCORE."""
        if self.air_quality is not None:
            return self.air_quality.aq_score
        return self.aq_score

    def get_aq_pm_1(self) -> int | None:
        """Return HVAC device Air Quality PM 1."""
        if self.air_quality is not None:
            return self.air_quality.aq_pm_1
        return self.aq_pm_1

    def get_aq_pm_2p5(self) -> int | None:
        """Return HVAC device Air Quality PM 2.5."""
        if self.air_quality is not None:
            return self.air_quality.aq_pm_2p5
        return self.aq_pm_2p5

    def get_aq_pm_10(self) -> int | None:
        """Return HVAC device Air Quality PM 10."""
        if self.air_quality is not None:
            return self.air_quality.aq_pm_10
        return self.aq_pm_10

    def get_aq_co2(self) -> int | None:
        """Return HVAC device Air Quality CO2."""
        if self.air_quality is not None:
            return self.air_quality.aq_co2
        return self.aq_co2

    def get_aq_tvoc(self) -> int | None:
        """Return HVAC device Air Quality TVOC."""
        if self.air_quality is not None:
            return self.air_quality.aq_tvoc
        return self.aq_tvoc

    def get_aq_temp(self) -> int | None:
        """Return HVAC device Air Quality Temperature."""
        if self.air_quality is not None:
            return self.air_quality.aq_temp
        return self.aq_temp

    def get_aq_humidity(self) -> int | None:
        """Return HVAC device Air Quality Humidity."""
        if self.air_quality is not None:
            return self.air_quality.aq_humidity
        return self.aq_humidity

    def get_aq_present(self) -> bool | None:
        """Return HVAC device Air Quality present."""
        if self.air_quality is not None:
            return self.air_quality.aq_present
        return self.aq_present

    def get_available(self) -> bool:
        """Return availability status."""
        return self.is_connected and self.ws_connected

    def get_double_set_point(self) -> bool:
        """Return Device double set point."""
        if self.double_set_point is not None:
            return self.double_set_point
        return False

    def get_dual_sp_conf(self) -> bool | None:
        """Return Device dual set point config."""
        return self.dual_sp_conf

    def get_errors(self) -> list[str]:
        """Return Device errors."""
        return self.errors

    def get_id(self) -> str:
        """Return Device ID."""
        return self.id

    def get_installation(self) -> str:
        """Return Installation ID."""
        return self.installation_id

    def get_is_connected(self) -> bool:
        """Return Device connection status."""
        return self.is_connected

    def get_mode(self) -> OperationMode | None:
        """Return Device mode."""
        return self.mode

    def get_mode_auto(self) -> OperationMode | None:
        """Return current auto mode."""
        return self.auto_mode

    def get_modes(self) -> list[OperationMode] | None:
        """Return Device modes."""
        if len(self.modes) > 0:
            return self.modes
        return None

    def get_name(self) -> str:
        """Return Device name."""
        return self.name

    def get_problems(self) -> bool:
        """Return Device problems."""
        return bool(self.errors) or bool(self.warnings)

    def get_simulator_mode(self) -> bool | None:
        """Return Device simulator mode."""
        return self.simulator_mode

    def get_warnings(self) -> list[str]:
        """Return Device warnings."""
        return self.warnings

    def get_webserver(self) -> str:
        """Return WebServer ID."""
        return self.webserver_id

    def get_ws_connected(self) -> bool:
        """Return WebServer connection status."""
        return self.ws_connected

    def set_air_quality(self, air_quality: AirQuality) -> None:
        """Set Air Quality."""
        self.air_quality = air_quality

    def set_mode(self, mode: int | OperationMode) -> None:
        """Set device operation mode."""
        _mode = OperationMode(mode)
        if _mode in self.modes:
            self.mode = _mode
        else:
            _LOGGER.error("%s: mode %s not in %s", self.id, _mode, self.modes)

    @abstractmethod
    def set_param(self, param: str, data: dict[str, Any]) -> None:
        """Update device parameter from API request."""

    def update_data(self, update: EntityUpdate) -> None:
        """Update Device data."""
        data = update.get_data()

        is_connected = parse_bool(data.get(API_IS_CONNECTED))
        if is_connected is not None:
            self.is_connected = is_connected
        ws_connected = parse_bool(data.get(API_WS_CONNECTED))
        if ws_connected is not None:
            self.ws_connected = ws_connected

        aq_active = parse_bool(data.get(API_AQ_ACTIVE))
        if aq_active is not None:
            self.aq_active = aq_active

        aq_pm_1 = parse_int(data.get(API_AQ_PM_1))
        if aq_pm_1 is not None:
            self.aq_pm_1 = aq_pm_1

        aq_pm_2p5 = parse_int(data.get(API_AQ_PM_2P5))
        if aq_pm_2p5 is not None:
            self.aq_pm_2p5 = aq_pm_2p5

        aq_pm_10 = parse_int(data.get(API_AQ_PM_10))
        if aq_pm_10 is not None:
            self.aq_pm_10 = aq_pm_10

        aq_co2 = parse_int(data.get(API_AQ_CO2))
        if aq_co2 is not None:
            self.aq_co2 = aq_co2

        aq_tvoc = parse_int(data.get(API_AQ_TVOC))
        if aq_tvoc is not None:
            self.aq_tvoc = aq_tvoc

        aq_humidity = parse_int(data.get(API_AQ_HUMIDITY))
        if aq_humidity is not None:
            self.aq_humidity = aq_humidity

        aq_temp = data.get(API_AQ_TEMP)
        if aq_temp is not None:
            aq_temp = parse_float(aq_temp.get(API_AQ_TEMP_CELSIUS))
            self.aq_temp = aq_temp

        aq_present = parse_bool(data.get(API_AQ_PRESENT))
        if aq_present is not None:
            self.aq_present = aq_present

        aq_quality = parse_str(data.get(API_AQ_QUALITY))
        if aq_quality is not None:
            self.aq_quality = aq_quality

        aq_score = parse_str(data.get(API_AQ_SCORE))
        if aq_score is not None:
            self.aq_score = aq_score

        auto_mode = data.get(API_AUTO_MODE)
        if auto_mode is not None:
            self.auto_mode = OperationMode(auto_mode)

        double_set_point = parse_bool(data.get(API_DOUBLE_SET_POINT))
        if double_set_point is not None:
            self.double_set_point = double_set_point

        dual_sp_conf = parse_bool(data.get(API_DUAL_SP_CONF))
        if dual_sp_conf is not None:
            self.dual_sp_conf = dual_sp_conf

        errors = data.get(API_ERRORS)
        if errors is not None:
            self.errors = []
            for error in errors:
                self.errors += [error]

        mode = data.get(API_MODE)
        if mode is not None:
            self.mode = OperationMode(mode)
        mode_avail = data.get(API_MODE_AVAIL)
        if mode_avail is not None and len(mode_avail) > 0:
            modes = []
            for mode in mode_avail:
                modes += [OperationMode(mode)]
            self.modes = modes

        simulator_mode = parse_bool(data.get(API_SIMULATOR_MODE))
        if simulator_mode is not None:
            self.simulator_mode = simulator_mode

        warnings = data.get(API_WARNINGS)
        if warnings is not None:
            self.warnings = []
            for warning in warnings:
                self.warnings += [warning]
