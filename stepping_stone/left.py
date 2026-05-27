import cadquery as cq
from cadquery import exporters

# Units: millimeters (CadQuery default)
# Base block: 27cm x 8cm x 9cm
L = 270
W = 80
H = 90

# Slots (top face)
slot_depth = 10  # 1cm

# A-end slot (centered), width 4cm, length 4cm
a_len = 40
a_wid = 40

# B-end slot (on centerline's left side), width 2cm, length 26cm
b_len = 260
b_wid = 20

# Fillet radius: 0.3cm
fillet_r = 3

# Build base
wp = cq.Workplane("XY").box(L, W, H)

# Coordinate convention on top face workplane (after centerOption COM):
# X along length, Y along width.
# "Left side" interpreted as negative Y.

# A-end slot placement: centered in Y, near the +X end.
# Slot spans x in [L/2 - a_len, L/2]
ax_center = (L / 2) - (a_len / 2)
ay_center = 0

# B-end slot placement: length 26cm, shifted to the left of centerline.
# Keep it inside the block: start near -X end, end at x = -L/2 + b_len
# Slot spans x in [-L/2, -L/2 + b_len]
bx_center = (-L / 2) + (b_len / 2)
# Shift left by half its width so its right edge lies on Y=0 centerline
by_center = -(b_wid / 2)

# Cut both slots from top; ensure they connect by overlapping in X region:
# A is near +X end, B reaches to x = -L/2 + 260 = +65mm, so it overlaps A.
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
