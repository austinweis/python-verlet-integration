INERTIA = 0.99
GRAVITY = 0.05
BOUNCE  = 1

class Rag:
    def __init__(self, rag):
        self.points = [p + p for p in rag["points"]]# [x, y, old-x, old-y]
        self.statics = [s for s in rag["statics"]]    # references to points that don't move

        self.sticks = [s for s in rag["sticks"]]    # references to two points that are connected

        # calculate and append stick lengths
        for s in self.sticks:
            p0 = self.points[s[0]]
            p1 = self.points[s[1]]

            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]
            distance = (dx * dx + dy * dy)**0.5
            s.append(distance)

    def move_dynamic_points(self):
        for i, p in enumerate(self.points):
            if i not in self.statics:
                vx = (p[0] - p[2]) * INERTIA
                vy = (p[1] - p[3]) * INERTIA
                p[2] = p[0]
                p[3] = p[1]
                p[0] += vx
                p[1] += vy
                p[1] += GRAVITY

    # move static point and all connected static points
    def move_static_point(self, index, pos, exception=None):
            for s in self.sticks:       
                p0 = self.points[s[0]]
                p1 = self.points[s[1]]

                if index == s[0] and s[1] in self.statics and exception != s[1]:
                    self.move_static_point(s[1], (p1[0] + (pos[0] - p0[0]), p1[1] + (pos[1] - p0[1])), exception=s[0])
                elif index == s[1] and s[0] in self.statics and exception != s[0]:
                    self.move_static_point(s[0], (p0[0] + (pos[0] - p1[0]), p0[1] + (pos[1] - p1[1])), exception=s[1])

            self.points[index] = [pos[0], pos[1]] * 2

    def constrain_points(self, bounds):
        width, height = bounds[0], bounds[1]
        for i, p in enumerate(self.points):
            if i not in self.statics:
                vx = (p[0] - p[2]) * INERTIA
                vy = (p[1] - p[3]) * INERTIA

                # if point is too far right
                if p[0] > width:
                    p[0] = width
                    p[2] = p[0] + vx * BOUNCE
                # if point is too far left
                if p[0] < 0:
                    p[0] = 0
                    p[2] = p[0] + vx * BOUNCE
                # if point is too low
                if p[1] > height:
                    p[1] = height
                    p[3] = p[1] + vy * BOUNCE
                # if point is too high
                if p[1] < 0:
                    p[1] = 0
                    p[3] = p[1] + vy * BOUNCE

    def update_sticks(self):
        for s in self.sticks:
            p0 = self.points[s[0]]
            p1 = self.points[s[1]]
            length = s[2]

            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]
            distance = (dx * dx + dy * dy)**0.5
            difference = length - distance
            try:
                percent = difference/distance/2
            except: 
                percent = 0 # prevent division by zero error
            offsetX = dx * percent
            offsetY = dy * percent

            if s[0] not in self.statics:
                p0[0] -= offsetX
                p0[1] -= offsetY
            if s[1] not in self.statics:
                p1[0] += offsetX
                p1[1] += offsetY 
