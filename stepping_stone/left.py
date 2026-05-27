import cadquery as cq
from cadquery import exporters

# Units: millimeters (CadQuery default)

# --------------------
# Parameters
# --------------------
L = 300.0
W = 80.0
H = 86.5

slot_len = 300.0
slot_wid = 20.0
slot_depth = 10.0

fillet_r = 3.0

# --------------------
# Build base solid
# --------------------
result = cq.Workplane("XY")
result = result.box(L, W, H)

# --------------------
# Cut centered slot on top face
# --------------------
wp_top = result.faces(">Z")
wp_top = wp_top.workplane(centerOption="CenterOfMass")

wp_slot = wp_top.rect(slot_len, slot_wid)
result = wp_slot.cutBlind(-slot_depth)

# --------------------
# Fillet all edges (including slot edges)
# --------------------
all_edges = result.edges()
result = all_edges.fillet(fillet_r)

# --------------------
# Export STL
# --------------------
exporters.export(result, "left.stl")

# For CQ-editor / CadQuery GUI
show_object(result)
