"""Every actuated joint of the CR12 URDF needs a transmission.

ros_control / gazebo_ros_control only expose joints that have a
<transmission>, so a revolute joint without one is not controllable.
"""
import os
import xml.etree.ElementTree as ET

URDF = os.path.join(os.path.dirname(__file__), "..", "urdf", "cr12.urdf")


def _robot():
    return ET.parse(URDF).getroot()


def test_every_revolute_joint_has_a_transmission():
    robot = _robot()
    revolute = {j.get("name") for j in robot.findall("joint")
                if j.get("type") in ("revolute", "continuous", "prismatic")}
    transmitted = {j.get("name") for t in robot.findall("transmission")
                   for j in t.findall("joint")}
    assert revolute - transmitted == set()


def test_transmissions_reference_existing_joints():
    robot = _robot()
    joints = {j.get("name") for j in robot.findall("joint")}
    transmitted = {j.get("name") for t in robot.findall("transmission")
                   for j in t.findall("joint")}
    assert transmitted - joints == set()
