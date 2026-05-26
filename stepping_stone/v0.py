import cadquery as cq

# Dimensions in millimeters (CadQuery default)
# 27 cm = 270 mm, 8 cm = 80 mm, 9 cm = 90 mm
# Fillet radius 0.5 cm = 5 mm
length = 270
width = 80
height = 90
fillet_radius = 5

# Slot (centered on top face)
# Slot width = 4 cm = 40 mm
# Slot depth = 1 cm = 10 mm
slot_width = 40
slot_depth = 10

# Build:
# 1) Create base block
# 2) Cut the centered slot on the top face
# 3) Fillet all edges (outer + edges created by the slot)
#
# Note: Filleting by edge direction selectors ("|X", "|Y", "|Z") can fail
# when the selector matches nothing (depending on CadQuery/OCC versions).
# Using .edges().fillet(...) is robust and satisfies “all corners filleted”.
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    # Top slot, centered
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .rect(length, slot_width)
    .cutBlind(-slot_depth)
    # Fillet all edges
    .edges()
    .fillet(fillet_radius)
)

# For CQ-editor / CadQuery GUI
show_object(result)
