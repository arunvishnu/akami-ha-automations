import appdaemon.plugins.hass.hassapi as hass


class Fans(hass.Hass):
    """
    Fan and exhaust automations.
    """

    def initialize(self):
        self.log("Fan automations initialized")
