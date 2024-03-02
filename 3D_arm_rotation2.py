#!/usr/bin/env python
# coding: utf-8

import numpy as np
from vedo import *
import time

# Rotation matrices
def RotationMatrix(theta, axis_name):
    c = np.cos(np.radians(theta))
    s = np.sin(np.radians(theta))

    if axis_name == 'x':
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    elif axis_name == 'y':
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    elif axis_name == 'z':
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

# creating the coordinate frame
def createCoordinateFrameMesh():
    _shaft_radius = 0.05
    _head_radius = 0.10
    _alpha = 1

    x_axisArrow = Arrow(start_pt=(0, 0, 0), end_pt=(1, 0, 0), shaft_radius=_shaft_radius, head_radius=_head_radius, c='red', alpha=_alpha)
    y_axisArrow = Arrow(start_pt=(0, 0, 0), end_pt=(0, 1, 0), shaft_radius=_shaft_radius, head_radius=_head_radius, c='green', alpha=_alpha)
    z_axisArrow = Arrow(start_pt=(0, 0, 0), end_pt=(0, 0, 1), shaft_radius=_shaft_radius, head_radius=_head_radius, c='blue', alpha=_alpha)
    originDot = Sphere(pos=[0, 0, 0], c="black", r=0.10)

    return x_axisArrow + y_axisArrow + z_axisArrow + originDot

def getLocalFrameMatrix(R_ij, t_ij):
    return np.block([[R_ij, t_ij], [np.zeros((1, 3)), 1]])

# function to animate the movement of the joints
def animate():
    plotter = Plotter(interactive=False, axes=1)

    L1, L2 = 5, 8
    base_height = 1

    # Base of the arm
    base = Cylinder(r=0.5, height=base_height, pos=(0, 0, base_height/2), c="gray", alpha=.8)

    while True:  # Infinite loop for continuous animation
        for angle in range(0, 360, 5):
            plotter.clear()

            phi1 = angle
            phi2 = -angle / 2
            phi3 = angle / 3

            R_01 = RotationMatrix(phi1, 'z')
            p1 = np.array([[0], [0], [1.0]])
            T_01 = getLocalFrameMatrix(R_01, p1)

            Frame1 = createCoordinateFrameMesh() + Cylinder(r=0.4, height=L1, pos=(L1 / 2, 0, 0), c="yellow", alpha=.8, axis=(1, 0, 0))
            Frame1.apply_transform(T_01)

            R_12 = RotationMatrix(phi2, 'z')
            p2 = np.array([[L1], [0.0], [0.0]])
            T_12 = getLocalFrameMatrix(R_12, p2)
            T_02 = T_01 @ T_12

            Frame2 = createCoordinateFrameMesh() + Cylinder(r=0.4, height=L2, pos=(L2 / 2, 0, 0), c="red", alpha=.8, axis=(1, 0, 0))
            Frame2.apply_transform(T_02)

            R_23 = RotationMatrix(phi3, 'z')
            p3 = np.array([[L2], [0.0], [0.0]])
            T_23 = getLocalFrameMatrix(R_23, p3)
            T_03 = T_01 @ T_12 @ T_23

            Frame3 = createCoordinateFrameMesh()
            Frame3.apply_transform(T_03)

            # Adding a ball as the end effector
            end_effector = Sphere(pos=T_03[:3, 3], r=0.5, c="blue")

            plotter.show([base, Frame1, Frame2, Frame3, end_effector], viewup="z")
            time.sleep(0.1)  # Small delay to control animation speed

animate()



















