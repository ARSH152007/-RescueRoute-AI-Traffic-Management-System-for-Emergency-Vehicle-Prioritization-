class TrafficManager:

    def __init__(self):
        self.state = "NORMAL"
        self.emergency_timer = 0
        self.cooldown = 5   # steps to stay in emergency

    def update_state(self, emergency_detected):

        # 🚑 Emergency trigger
        if emergency_detected:
            self.state = "EMERGENCY"
            self.emergency_timer = self.cooldown
            return "EMERGENCY"

        # ⏳ Stay in emergency for some time
        if self.state == "EMERGENCY":
            self.emergency_timer -= 1

            if self.emergency_timer <= 0:
                self.state = "NORMAL"
                return "NORMAL"

            return "EMERGENCY"

        return "NORMAL"