import appdaemon.plugins.hass.hassapi as hass


OUTDOOR_LIGHTS    = "light.outdoor"
INTERIOR_LIGHTS   = "light.first_floor_interior"
OFFICE_FRONT      = "light.office_front"
HOLIDAY_LIGHTS    = "switch.foyer_holiday_lights"


class Lighting(hass.Hass):
    """
    Automations:
      - turn_on_outdoor_lights          → sunset
      - turn_off_outdoor_lights_at_11pm → 23:00
      - turn_off_outdoor_lights_at_sunrise → sunrise
      - turn_on_interior_lights         → sunset
      - turn_off_interior_lights        → 22:00
      - turn_on_office_front            → 09:00 Thu & Fri only
      - turn_off_office_front           → 17:15 Thu & Fri only
      - holiday_lights_on               → sunset
      - holiday_lights_off_at_11pm      → 23:00
    """

    def initialize(self):
        # Outdoor
        self.run_at_sunset(self.turn_on_outdoor)
        self.run_daily(self.turn_off_outdoor_11pm, "23:00:00")
        self.run_at_sunrise(self.turn_off_outdoor_sunrise)

        # Interior
        self.run_at_sunset(self.turn_on_interior)
        self.run_daily(self.turn_off_interior, "22:00:00")

        # Office front — Thu & Fri only
        self.run_daily(self.turn_on_office_front, "09:00:00")
        self.run_daily(self.turn_off_office_front, "17:15:00")

        # Holiday
        self.run_at_sunset(self.turn_on_holiday)
        self.run_daily(self.turn_off_holiday_11pm, "23:00:00")

        self.log("Lighting automations initialized")

    # ── Outdoor ───────────────────────────────────────────

    def turn_on_outdoor(self, kwargs):
        self.turn_on(OUTDOOR_LIGHTS)
        self.log("Outdoor lights on (sunset)")

    def turn_off_outdoor_11pm(self, kwargs):
        self.turn_off(OUTDOOR_LIGHTS)
        self.log("Outdoor lights off (11 PM)")

    def turn_off_outdoor_sunrise(self, kwargs):
        self.turn_off(OUTDOOR_LIGHTS)
        self.log("Outdoor lights off (sunrise)")

    # ── Interior ──────────────────────────────────────────

    def turn_on_interior(self, kwargs):
        self.turn_on(INTERIOR_LIGHTS)
        self.log("Interior lights on (sunset)")

    def turn_off_interior(self, kwargs):
        self.turn_off(INTERIOR_LIGHTS)
        self.log("Interior lights off (10 PM)")

    # ── Office ────────────────────────────────────────────

    def turn_on_office_front(self, kwargs):
        if self.date().weekday() in (3, 4):  # Thu, Fri
            self.turn_on(OFFICE_FRONT)
            self.log("Office front light on (9 AM Thu/Fri)")

    def turn_off_office_front(self, kwargs):
        if self.date().weekday() in (3, 4):  # Thu, Fri
            self.turn_off(OFFICE_FRONT)
            self.log("Office front light off (5:15 PM Thu/Fri)")

    # ── Holiday ───────────────────────────────────────────

    def turn_on_holiday(self, kwargs):
        self.call_service("switch/turn_on", entity_id=HOLIDAY_LIGHTS)
        self.log("Holiday lights on (sunset)")

    def turn_off_holiday_11pm(self, kwargs):
        self.call_service("switch/turn_off", entity_id=HOLIDAY_LIGHTS)
        self.log("Holiday lights off (11 PM)")
