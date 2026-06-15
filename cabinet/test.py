import cadquery as cq
from cadquery import exporters

L = 315
W = 310
H = 200
slot_len = 320.0
slot_wid = 25.0
slot_depth = 200.0
slot_border = 10

fillet_r = 1
cut_y = 120
cut_z = 200

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
    (rect0[0][0] + 72, zmax),
    (rect0[1][0] + 72, zmax),
    (rect0[2][0] + 72, zmin),
    (rect0[3][0] + 72, zmin),
]

rect2 = [
    (rect1[0][0] + 36, zmax),
    (rect1[1][0] + 36, zmax),
    (rect1[2][0] + 36, zmin),
    (rect1[3][0] + 36, zmin),
]

rect3 = [
    (rect2[0][0] + 27, zmax),
    (rect2[1][0] + 27, zmax),
    (rect2[2][0] + 27, zmin),
    (rect2[3][0] + 27, zmin),
]

rect4 = [
    (rect3[0][0] + 23, zmax),
    (rect3[1][0] + 23, zmax),
    (rect3[2][0] + 23, zmin),
    (rect3[3][0] + 23, zmin),
]

rect5 = [
    (rect4[0][0] + 21, zmax),
    (rect4[1][0] + 21, zmax),
    (rect4[2][0] + 21, zmin),
    (rect4[3][0] + 21, zmin),
]

rect6 = [
    (rect5[0][0] + 15, zmax),
    (rect5[1][0] + 15, zmax),
    (rect5[2][0] + 15, zmin),
    (rect5[3][0] + 15, zmin),
]

rect7 = [
    (rect6[0][0] + 15, zmax),
    (rect6[1][0] + 15, zmax),
    (rect6[2][0] + 15, zmin),
    (rect6[3][0] + 15, zmin),
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
result = wp.polyline(rect4).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.polyline(rect5).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.polyline(rect6).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.polyline(rect7).close().cutThruAll()

wp = result.faces(">X").workplane(centerOption="CenterOfBoundBox")
result = wp.box(W, H, 10)

wp = result.faces("<X").workplane(centerOption="CenterOfBoundBox")
result = wp.box(W, H, 10)

wp = result.faces("<Z").workplane(centerOption="CenterOfBoundBox")
result = wp.box(L + 10, W, 10)

wp = result.faces(">Y").workplane(centerOption="CenterOfBoundBox")
result = wp.box(L + 10, H+5, 10)

# edge_list = result.edges().vals()
# for e in edge_list:
#     try:
#         result = result.edges(
#             cq.selectors.NearestToPointSelector(e.Center())
#         ).fillet(fillet_r)
#     except:
#         pass

# edges = result.edges()
# result = edges.fillet(fillet_r)

exporters.export(result, "test.stl")

show_object(result)


