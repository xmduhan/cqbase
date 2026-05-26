import cadquery as cq

# Dimensions in millimeters (CadQuery default):
# 8 cm = 80 mm, height = 27 mm (as specified)
length = 80
width = 80
height = 27

result = cq.Workplane("XY").box(length, width, height)

# For CQ-editor / CadQuery GUI
show_object(result)
