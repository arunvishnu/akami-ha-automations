import appdaemon.plugins.hass.hassapi as hass


class Lighting(hass.Hass):
    """
    All lighting automations.
    Automations will be added here once timing is confirmed.
    """

    def initialize(self):
        self.log("Lighting automations initialized")
