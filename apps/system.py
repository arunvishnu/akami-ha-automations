import appdaemon.plugins.hass.hassapi as hass


class System(hass.Hass):
    """
    Automations:
      - ha_daily_restart → 3:00 AM
    """

    def initialize(self):
        self.run_daily(self.daily_restart, "03:00:00")
        self.log("System automations initialized — deploy pipeline test v3")

    def daily_restart(self, kwargs):
        self.log("Initiating daily HA restart")
        self.call_service("homeassistant/restart")
