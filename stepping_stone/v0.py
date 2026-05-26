import cadquery as cq

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

# Build:
# 1) Create base block
# 2) Cut the centered slot on the top face
#
# Note: The previous version tried to fillet all edges; some CadQuery/OCC
# combinations can fail edge selection/fillet execution and raise:
# "There are no suitable edges for chamfer or fillet".
# The user requirements do NOT request fillets, so we omit filleting.
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    # Top slot, centered
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .rect(length, slot_width)
    .cutBlind(-slot_depth)
)

# For CQ-editor / CadQuery GUI
show_object(result)
