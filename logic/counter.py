class RepCounter:
    def __init__(self, min_angle=70, max_angle=160):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.direction = "down"
        self.count = 0

    def update(self, angle):
        if angle < self.min_angle and self.direction == "down":
            self.direction = "up"
        elif angle > self.max_angle and self.direction == "up":
            self.direction = "down"
            self.count += 1
