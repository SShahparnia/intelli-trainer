class FormChecker:
    def __init__(self, min_back_angle=160):
        self.min_back_angle = min_back_angle

    def check_back_angle(self, angle):
        return "Good" if angle >= self.min_back_angle else "Keep Back Straight"
