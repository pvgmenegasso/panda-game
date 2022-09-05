    def handleMouseClick(self):
        # When the mouse is clicked, if the simulation is running pause all the
        # planets and sun, otherwise resume it
        if self.simRunning:
            print("Pausing Simulation")
            # changing the text to reflect the change from "RUNNING" to
            # "PAUSED"
            self.mouse1EventText.setText(
                "Mouse Button 1: Toggle entire Solar System [PAUSED]")
            # For each planet, check if it is moving and if so, pause it
            # Sun
            if self.day_period_sun.isPlaying():
                self.togglePlanet("Sun", self.day_period_sun, None,
                                  self.skeyEventText)
            if self.day_period_mercury.isPlaying():
                self.togglePlanet("Mercury", self.day_period_mercury,
                                  self.orbit_period_mercury, self.ykeyEventText)
            # Venus
            if self.day_period_venus.isPlaying():
                self.togglePlanet("Venus", self.day_period_venus,
                                  self.orbit_period_venus, self.vkeyEventText)
            #Earth and moon
            if self.day_period_earth.isPlaying():
                self.togglePlanet("Earth", self.day_period_earth,
                                  self.orbit_period_earth, self.ekeyEventText)
                self.togglePlanet("Moon", self.day_period_moon,
                                  self.orbit_period_moon)
            # Mars
            if self.day_period_mars.isPlaying():
                self.togglePlanet("Mars", self.day_period_mars,
                                  self.orbit_period_mars, self.mkeyEventText)
        else:
            #"The simulation is paused, so resume it
            print("Resuming Simulation")
            self.mouse1EventText.setText(
                "Mouse Button 1: Toggle entire Solar System [RUNNING]")
            # the not operator does the reverse of the previous code
            if not self.day_period_sun.isPlaying():
                self.togglePlanet("Sun", self.day_period_sun, None,
                                  self.skeyEventText)
            if not self.day_period_mercury.isPlaying():
                self.togglePlanet("Mercury", self.day_period_mercury,
                                  self.orbit_period_mercury, self.ykeyEventText)
            if not self.day_period_venus.isPlaying():
                self.togglePlanet("Venus", self.day_period_venus,
                                  self.orbit_period_venus, self.vkeyEventText)
            if not self.day_period_earth.isPlaying():
                self.togglePlanet("Earth", self.day_period_earth,
                                  self.orbit_period_earth, self.ekeyEventText)
                self.togglePlanet("Moon", self.day_period_moon,
                                  self.orbit_period_moon)
            if not self.day_period_mars.isPlaying():
                self.togglePlanet("Mars", self.day_period_mars,
                                  self.orbit_period_mars, self.mkeyEventText)
        # toggle self.simRunning
        self.simRunning = not self.simRunning