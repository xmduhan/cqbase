import cadquery as cq
result = cq.Workplane("XY" ).box(350, 250, 120).edges("|Z").fillet(5)
show_object(result)