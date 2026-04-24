import cadquery as cq

# ---------------- Parameters ----------------
L = 230.0
W = 230.0
H = 100.0

PEG_D = 14.6
PEG_H = 25.0

EDGE_FILLET = 2.0

def hole_points(l=L, w=W):
    dx = l / 6.0
    dy = w / 6.0
    xs = [-l / 2.0 + dx, l / 2.0 - dx]
    ys = [-w / 2.0 + dy, w / 2.0 - dy]
    return [(x, y) for x in xs for y in ys]


# ---------------- Build brick2 ----------------
# brick2: top platform (flat), bottom has pegs to insert into brick1 top holes
brick = cq.Workplane("XY").box(L, W, H, centered=(True, True, True))

brick = (
    brick.faces("<Z")
    .workplane()
    .pushPoints(hole_points())
    .circle(PEG_D / 2.0)
    .extrude(-PEG_H)
)

brick = brick.edges("|Z").fillet(EDGE_FILLET)

show_object(brick)
