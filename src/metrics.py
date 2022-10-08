from typing import List, Generator
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily

METRIC_PREFIX="solis"

class REG:
    def collect(self, vals):
        self._parse(vals)
        yield from vars(self).values()

    def _parse(self, vals):
        return NotImplementedError

class REG_33022(REG):
    REGISTER_LENGTH = 19
    def __init__(self) -> None:
        super().__init__()
        self.system_year = GaugeMetricFamily(f"{METRIC_PREFIX}_system_year", "System Year")
        self.system_month = GaugeMetricFamily(f"{METRIC_PREFIX}_system_month", "System Month")
        self.system_day = GaugeMetricFamily(f"{METRIC_PREFIX}_system_day", "System Day")
        self.system_hour = GaugeMetricFamily(f"{METRIC_PREFIX}_system_hour", "System Hour")
        self.system_minute = GaugeMetricFamily(f"{METRIC_PREFIX}_system_minute", "System Minute")
        self.system_second = GaugeMetricFamily(f"{METRIC_PREFIX}_system_second", "System Second")
        self.generated_total = CounterMetricFamily(f"{METRIC_PREFIX}_generated", "Total Generation", unit="watt_hours", labels=["unit"])
        self.generated_current_month = GaugeMetricFamily(f"{METRIC_PREFIX}_generated_current_month", "Generated This Month", unit="watt_hours", labels=["unit"])
        self.generated_previous_month = GaugeMetricFamily(f"{METRIC_PREFIX}_generated_previous_month", "Generated Last Month", unit="watt_hours", labels=["unit"])
        self.generated_today = GaugeMetricFamily(f"{METRIC_PREFIX}_generated_today", "Generated Today", unit="watt_hours")
        self.generated_yesterday = GaugeMetricFamily(f"{METRIC_PREFIX}_generated_yesterday", "Generated Yesterday", unit="watt_hours")
        self.generated_current_year = GaugeMetricFamily(f"{METRIC_PREFIX}_generated_current_year", "Generated This Year", unit="watt_hours", labels=["unit"])
        self.generated_previous_year = GaugeMetricFamily(f"{METRIC_PREFIX}_generated_previous_year", "Generated Previous Year", unit="watt_hours", labels=["unit"])

    # def __parse(self, vals: List[float]):
    def _parse(self, vals):
        self.system_year.add_metric([], vals[0])
        self.system_month.add_metric([], vals[1])
        self.system_day.add_metric([], vals[2])
        self.system_hour.add_metric([], vals[3])
        self.system_minute.add_metric([], vals[4])
        self.system_second.add_metric([], vals[5])
        # vals[6] not used
        self.generated_total.add_metric(["1"], vals[7] * 1000)
        self.generated_total.add_metric(["2"], vals[8] * 1000)
        self.generated_current_month.add_metric(["1"], vals[9] * 1000)
        self.generated_current_month.add_metric(["2"], vals[10] * 1000)
        self.generated_previous_month.add_metric(["1"], vals[11] * 1000)
        self.generated_previous_month.add_metric(["2"], vals[12] * 1000)
        self.generated_today.add_metric([""], vals[13] * 100)
        self.generated_yesterday.add_metric([""], vals[14] * 100)
        self.generated_current_year.add_metric(["1"], vals[15] * 1000)
        self.generated_current_year.add_metric(["2"], vals[16] * 1000)
        self.generated_previous_year.add_metric(["1"], vals[17] * 1000)
        self.generated_previous_year.add_metric(["2"], vals[18] * 1000)

class REG_33049(REG):
    REGISTER_LENGTH = 10
    def __init__(self) -> None:
        super().__init__()
        self.dc_voltage = GaugeMetricFamily(f"{METRIC_PREFIX}_dc", "DC Voltage", unit="voltage", labels=["unit"])
        self.dc_current = GaugeMetricFamily(f"{METRIC_PREFIX}_dc", "DC Current", unit="amperes", labels=["unit"])
        self.dc_input = CounterMetricFamily(f"{METRIC_PREFIX}_dc_input_power", "DC Input Power", unit="watts", labels=["unit"])

    def _parse(self, regs):
        self.dc_voltage.add_metric(["1"], regs[0] * 10)
        self.dc_current.add_metric(["1"], regs[1] * 10)
        self.dc_voltage.add_metric(["2"], regs[2] * 10)
        self.dc_current.add_metric(["2"], regs[3] * 10)
        self.dc_voltage.add_metric(["3"], regs[4] * 10)
        self.dc_current.add_metric(["3"], regs[5] * 10)
        self.dc_voltage.add_metric(["4"], regs[6] * 10)
        self.dc_current.add_metric(["5"], regs[7] * 10)
        self.dc_input.add_metric(["1"], regs[8])
        self.dc_input.add_metric(["2"], regs[9])

class REG_33071(REG):
    REGISTER_LENGTH = 14
    def __init__(self) -> None:
        super().__init__()
        self.dc_bus_voltage = GaugeMetricFamily(f"{METRIC_PREFIX}_dc_bus", "DC Bus Voltage", unit="voltage")
        self.dc_bus_half_voltage = GaugeMetricFamily(f"{METRIC_PREFIX}_dc_bus_half", "DC Bus Half Voltage", unit="voltage")
        self.phase_voltage = GaugeMetricFamily(f"{METRIC_PREFIX}_phase", "Phase Voltage", unit="voltage", labels=["letter"])
        self.phase_current = GaugeMetricFamily(f"{METRIC_PREFIX}_phase", "Phase Current", unit="amperes", labels=["letter"])
        self.active_power = GaugeMetricFamily(f"{METRIC_PREFIX}_active_power", "Active Power", unit="watts", labels=["unit"])
        self.reactive_power = GaugeMetricFamily(f"{METRIC_PREFIX}_reactive_power", "Reactive Power", unit="volt_amperes", labels=["unit"])
        self.apparent_power = GaugeMetricFamily(f"{METRIC_PREFIX}_apparent_power", "Apparent Power", unit="volt_amperes", labels=["unit"])
    
    def _parse(self, vals):
        self.dc_bus_voltage.add_metric([], vals[0] * 10)
        self.dc_bus_half_voltage.add_metric([], vals[1] * 10)
        self.phase_voltage.add_metric(["a"], vals[2] * 10)
        self.phase_voltage.add_metric(["b"], vals[3] * 10)
        self.phase_voltage.add_metric(["c"], vals[4] * 10)
        self.phase_current.add_metric(["a"], vals[5] * 10)
        self.phase_current.add_metric(["b"], vals[6] * 10)
        self.phase_current.add_metric(["c"], vals[7] * 10)
        self.active_power.add_metric(["1"], vals[8])
        self.active_power.add_metric(["2"], vals[9])
        self.reactive_power.add_metric(["1"], vals[10])
        self.reactive_power.add_metric(["2"], vals[11])
        self.apparent_power.add_metric(["1"], vals[12])
        self.apparent_power.add_metric(["2"], vals[13])

class REG_33091(REG):
    REGISTER_LENGTH = 5
    def __init__(self) -> None:
        super().__init__()
        # self.standard_working_mode = ????
        # self.national_standard = ????
        self.inverter_temperature = GaugeMetricFamily(f"{METRIC_PREFIX}_inverter_temperature", "Inverter Temperature", unit="celcius")
        self.grid_frequency = GaugeMetricFamily(f"{METRIC_PREFIX}_grid_frequency", "Grid Frequency", unit="hertz")
        # self.inverter_current_state = ????
    
    def _parse(self, vals):
        # self.standard_working_mode.add_metric([], vals[0])
        # self.national_standard.add_metric([], vals[1])
        self.inverter_temperature.add_metric([], vals[2] * 10)
        self.grid_frequency.add_metric([], vals[3] * 100)
        # self.inverter_current_state.add_metric([], vals[4])

class REG_33100(REG):
    REGISTER_LENGTH = 7
    def __init__(self) -> None:
        super().__init__()
        self.output_limit_active_power = GaugeMetricFamily(f"{METRIC_PREFIX}_output_limit_active_power", "Limit Active Power Outpur", unit="watts", labels=["unit"])
        self.output_limit_reactive_power = GaugeMetricFamily(f"{METRIC_PREFIX}_limit_reactive_power", "Limit Reactive Power Output", unit="watts", labels=["unit"])
        self.actual_power_limited_percentage = GaugeMetricFamily(f"{METRIC_PREFIX}_actual_power_limited_percentage", "Actual Power Limited Power", unit="percentage")
        # self.actual_adjustment_value = ???
        # self.limit_reactive_power = ???
    
    def _parse(self, vals):
        pass

class REG_33126(REG):
    REGISTER_LENGTH = 25
    def __init__(self) -> None:
        super().__init__()
        
    
    def _parse(self, vals):
        pass

class REG_33161(REG):
    REGISTER_LENGTH = 20
    def __init__(self) -> None:
        super().__init__()
        
    
    def _parse(self, vals):
        pass

class REG_33251(REG):
    REGISTER_LENGTH = 36
    def __init__(self) -> None:
        super().__init__()
        
    
    def _parse(self, vals):
        pass

METRICS = {
    33022: REG_33022,
    33049: REG_33049,
    33071: REG_33071,
    33091: REG_33091,
    33100: REG_33100,
    33126: REG_33126,
    33161: REG_33161,
    33251: REG_33251
}