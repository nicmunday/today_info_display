#!/usr/bin/env python3
from skyfield import api
from skyfield import almanac
import datetime

class MoonPhase:
    def __init__(self, time):

        my_timescale = api.load.timescale()
        my_ephemeris = api.load('de421.bsp')
        t = my_timescale.utc(time.year,
                             time.month, time.day,
                             time.hour, time.minute)

        phase = almanac.moon_phase(my_ephemeris, t)
        self.degrees = phase.degrees

    def get_phase(self, ):
        moon_phase = ""

        if self.degrees >= 360 or self.degrees < 45:
            moon_phase = "New Moon"
        if self.degrees >= 45 and self.degrees < 90:
            moon_phase = "Waxing Crescent"
        if self.degrees >= 90 and self.degrees < 135:
            moon_phase = "First Quarter"
        if self.degrees >= 135 and self.degrees < 180:
            moon_phase = "Waxing Gibbous"
        if self.degrees >= 180 and self.degrees < 225:
            moon_phase = "Full Moon"
        if self.degrees >= 225 and self.degrees < 270:
            moon_phase = "Waning Gibbous"
        if self.degrees >= 270 and self.degrees < 315:
            moon_phase = "Third Quarter"
        if self.degrees >= 315 and self.degrees < 360:
            moon_phase = "Waning Crescent"

        return moon_phase