import appdaemon.plugins.hass.hassapi as hass


MASTER_BATH_FAN = "switch.master_bath_exhaust_fan_sonoff_1000987cf3"
FAN_TIMER_MINS  = 30


class Fans(hass.Hass):
    """
    Automations:
      - master_bath_exhaust_fan_30_mins_timer
        Fan turns on → auto off after 30 minutes.
        Manually turning it off cancels the timer.
    """

    def initialize(self):
        self._timer = None
        self.listen_state(self.fan_state_changed, MASTER_BATH_FAN)
        self.log("Fan automations initialized")

    def fan_state_changed(self, entity, attribute, old, new, kwargs):
        if new == "on":
            if self._timer is not None:
                self.cancel_timer(self._timer)
            self._timer = self.run_in(self.auto_off, FAN_TIMER_MINS * 60)
            self.log(f"Master bath fan on — auto-off in {FAN_TIMER_MINS} min")

        elif new == "off":
            if self._timer is not None:
                self.cancel_timer(self._timer)
                self._timer = None
                self.log("Master bath fan turned off manually — timer cancelled")

    def auto_off(self, kwargs):
        self.call_service("switch/turn_off", entity_id=MASTER_BATH_FAN)
        self._timer = None
        self.log(f"Master bath fan auto-off after {FAN_TIMER_MINS} minutes")
