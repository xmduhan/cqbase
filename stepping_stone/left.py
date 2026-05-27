import cadquery as cq
from cadquery import exporters

# Dimensions in millimeters (CadQuery default)
# 27 cm = 270 mm, 8 cm = 80 mm, 9 cm = 90 mm
length = 270
width = 80
height = 90

# Slot (centered on top face)
# Slot width = 4 cm = 40 mm
# Slot depth = 1 cm = 10 mm
slot_width = 40
slot_depth = 10

# Fillet radius (all edges)
# 0.3 cm = 3 mm
fillet_radius = 3

# Build:
# 1) Create base block
# 2) Cut the centered slot on the top face
# 3) Fillet (round) all edges with radius 3mm
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    # Top slot, centered
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .rect(length, slot_width)
    .cutBlind(-slot_depth)
    # Round all edges
    .edges()
    .fillet(fillet_radius)
)

# Export STL
exporters.export(result, "stepping_stone.stl")

# For CQ-editor / CadQuery GUI
show_object(result)
