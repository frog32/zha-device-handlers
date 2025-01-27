"""Module for Xiaomi Aqara quirks implementations."""
import math
from zigpy.zcl.clusters.measurement import (IlluminanceMeasurement, TemperatureMeasurement)
from zhaquirks import CustomCluster


class IlluminanceMeasurementCluster(CustomCluster, IlluminanceMeasurement):
    """Multistate input cluster."""

    cluster_id = IlluminanceMeasurement.cluster_id

    def _update_attribute(self, attrid, value):
        if attrid == 0 and value > 0:
            value = 10000 * math.log10(value) + 1
        super()._update_attribute(attrid, value)


class TemperatureMeasurementCluster(CustomCluster, TemperatureMeasurement):
    """Temperature input cluster that restricts values to filter out bogus
    values."""

    cluster_id = TemperatureMeasurement.cluster_id

    def _update_attribute(self, attrid, value):
        # drop values above and below documented range for this sensor
        if attrid == 0 and (value >= -20 or value <= 60):
            super()._update_attribute(attrid, value)
