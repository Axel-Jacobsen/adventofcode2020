#! /usr/bin/env python3


import math


class ShipNavP1:
    x = 0
    y = 0
    heading = 90

    def __repr__(self):
        return f"ShipNav: pos={self.x,self.y}; hdg={self.heading}"

    def step(self, action, val):
        if action == "N":
            self.y += val
        elif action == "S":
            self.y -= val
        elif action == "E":
            self.x += val
        elif action == "W":
            self.x -= val
        elif action == "L":
            self.heading -= val
        elif action == "R":
            self.heading += val
        elif action == "F":
            self.x += round(val * math.sin(self.heading * math.pi / 180), 3)
            self.y += round(val * math.cos(self.heading * math.pi / 180), 3)


class ShipNavP2:
    x = 0
    y = 0
    waypoint_x = 10
    waypoint_y = 1
    waypoint_heading = 0

    def __repr__(self):
        return f"ShipNav: pos={self.x,self.y}; waypoint_pos={self.waypoint_x, self.waypoint_y}; waypoint_hdg={self.waypoint_heading}"

    def update_heading(self):
        """
        Change heading s.t. it matches the waypoint pos
        """
        if self.waypoint_x == 0:
            self.waypoint_heading = 0 if self.waypoint_y > 0 else 180
        else:
            self.waypoint_heading = round(
                180 / math.pi * math.atan(self.waypoint_y / self.waypoint_x), 3
            )

    def update_position(self, val):
        """
        Change position s.t. it matches the waypoint heading
        i.e. apply the rotation matrix
        """
        deg = -math.pi / 180 * val
        wx = self.waypoint_x
        wy = self.waypoint_y
        self.waypoint_x = round(wx * math.cos(deg) - wy * math.sin(deg), 3)
        self.waypoint_y = round(wx * math.sin(deg) + wy * math.cos(deg), 3)

    def step(self, action, val):
        if action == "N":
            self.waypoint_y += val
            self.update_heading()
        elif action == "S":
            self.waypoint_y -= val
            self.update_heading()
        elif action == "E":
            self.waypoint_x += val
            self.update_heading()
        elif action == "W":
            self.waypoint_x -= val
            self.update_heading()
        elif action == "L":
            self.waypoint_heading -= val
            self.update_position(-val)
        elif action == "R":
            self.waypoint_heading += val
            self.update_position(val)
        elif action == "F":
            self.x += val * self.waypoint_x
            self.y += val * self.waypoint_y


def test_SN2():
    SN = ShipNavP2()
    SN.waypoint_x = 1 / math.sqrt(2)
    SN.waypoint_y = 1 / math.sqrt(2)
    SN.update_heading()
    assert SN.waypoint_heading == 45, f"{SN}, should be {45}"

    SN.waypoint_x = -1 / math.sqrt(2)
    SN.waypoint_y = 1 / math.sqrt(2)
    SN.update_heading()
    assert SN.waypoint_heading == -45, f"{SN}, should be {-45}"

    SN.step("R", 45)
    assert SN.waypoint_x == 0, f"SN {SN}, should be x=0"
    assert SN.waypoint_y == 1, f"SN {SN}, should be y=1"

    SN.step("R", 90)
    assert SN.waypoint_x == 1, f"SN {SN}, should be x=1"
    assert SN.waypoint_y == 0, f"SN {SN}, should be y=0"

    SN.step("R", 90)
    assert SN.waypoint_x == 0, f"SN {SN}, should be x=1"
    assert SN.waypoint_y == -1, f"SN {SN}, should be y=0"

    SN.step("R", 90)
    assert SN.waypoint_x == -1, f"SN {SN}, should be x=1"
    assert SN.waypoint_y == 0, f"SN {SN}, should be y=0"


test_SN2()


def p1():
    with open("input.txt", "r") as f:
        avs = [(v[0], int(v[1:])) for v in f.read().split("\n") if v != ""]
        SN = ShipNavP1()
        for act, val in avs:
            SN.step(act, val)
    return abs(SN.x) + abs(SN.y)


def p2():
    with open("input.txt", "r") as f:
        avs = [(v[0], int(v[1:])) for v in f.read().split("\n") if v != ""]
        SN = ShipNavP2()
        SN.update_heading()
        for act, val in avs:
            SN.step(act, val)
    return abs(SN.x) + abs(SN.y)


print(p1(), p2())
