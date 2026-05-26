import cadquery as cq

# Dimensions in millimeters (CadQuery default)
# 27 cm = 270 mm, 8 cm = 80 mm, 9 cm = 90 mm
# Fillet radius 0.5 cm = 5 mm
length = 270
width = 80
height = 90
fillet_radius = 5

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    # Fillet all edges (all corners)
    .edges()
    .fillet(fillet_radius)
)

# For CQ-editor / CadQuery GUI
show_object(result)
