import cadquery as cq
from cadquery import exporters

# Units: millimeters (CadQuery default)
# Base block: 300mm x 80mm x 86.5mm
L = 300
W = 80
H = 86.5

# Slots (top face)
slot_depth = 10  # depth 10mm

# A-end slot (centered), width 40mm, length 40mm
a_len = 40
a_wid = 40

# B-end slot (left of centerline), width 20mm, length 260mm
b_len = 260
b_wid = 20

# Fillet radius: 3mm
fillet_r = 3

# Build base
wp = cq.Workplane("XY").box(L, W, H)

# Coordinate convention on top face workplane (centerOption COM):
# X along length, Y along width.
# "Left side" interpreted as negative Y.

# Place slots so they are connected (overlap in X):
# B slot spans x in [-L/2, -L/2 + b_len] = [-150, 110]
# A slot near +X end spans x in [L/2 - a_len, L/2] = [110, 150]
# They touch/meet at x=110.

# A-end slot placement: centered in Y, near the +X end.
ax_center = (L / 2) - (a_len / 2)  # 130
ay_center = 0

# B-end slot placement: shifted left so its right edge lies on Y=0 centerline.
bx_center = (-L / 2) + (b_len / 2)  # -20
by_center = -(b_wid / 2)  # -10

result = (
    wp
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    # B-end slot
    .center(bx_center, by_center)
    .rect(b_len, b_wid)
    .cutBlind(-slot_depth)
    # A-end slot
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .center(ax_center, ay_center)
    .rect(a_len, a_wid)
    .cutBlind(-slot_depth)
    # Fillet all edges
    .edges()
    .fillet(fillet_r)
)

# Export STL
exporters.export(result, "left.stl")

# For CQ-editor / CadQuery GUI
show_object(result)
