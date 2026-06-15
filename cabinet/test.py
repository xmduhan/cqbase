import cadquery as cq
from cadquery import exporters

L = 360
W = 270
H = 200
slot_len = 320.0
slot_wid = 25.0
slot_depth = 180.0
slot_border = 10

fillet_r = 2
cut_y = 120   
cut_z = 180   

ymin, ymax = -W/2, W/2
zmin, zmax = -H/2, H/2

tri_lb = [(ymin, zmin), (ymin + cut_y, zmin), (ymin, zmin + cut_z)]
tri_rt = [(ymax, zmax), (ymax - cut_y, zmax), (ymax, zmax - cut_z)]

rect0 = [
    (ymin + slot_border, zmax), 
    (ymin + slot_border + slot_wid, zmax), 
    (ymin + cut_y + slot_wid + slot_border, zmin),
    (ymin + cut_y + slot_border, zmin), 
]

rect1 = [
    (rect0[0][0] + 61, zmax), 
    (rect0[1][0] + 61, zmax), 
    (rect0[2][0] + 61, zmin),
    (rect0[3][0] + 61, zmin), 
]

rect2 = [
    (rect1[0][0] + 32, zmax), 
    (rect1[1][0] + 32, zmax), 
    (rect1[2][0] + 32, zmin),
    (rect1[3][0] + 32, zmin), 
]

rect3 = [
    (rect1[0][0] + 58, zmax), 
    (rect1[1][0] + 58, zmax), 
    (rect1[2][0] + 58, zmin),
    (rect1[3][0] + 58, zmin), 
]

result = cq.Workplane("XY")
result = result.box(L, W, H)

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.polyline(tri_lb).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.polyline(tri_rt).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.polyline(rect0).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.polyline(rect1).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.polyline(rect2).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.polyline(rect3).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.box(W, H, 10)

wp = result.faces("<X").workplane(centerOption="CenterOfBoundBox")
result = wp.box(W, H, 10)

wp = result.faces("<Z").workplane(centerOption="CenterOfBoundBox")
result = wp.box(L +10, W, 10)

wp = result.faces(">Y").workplane(centerOption="CenterOfBoundBox")
result = wp.box(L + 10, H + 5, 10)

edge_list = result.edges().vals()
for e in edge_list:
    try:
        result = result.edges(
            cq.selectors.NearestToPointSelector(e.Center())
        ).fillet(fillet_r)
    except:
        pass
# edges = result.edges()
# result = edges.fillet(fillet_r)

exporters.export(result, "test.stl")

show_object(result)


