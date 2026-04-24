import cadquery as cq
from cadquery import exporters
from pathlib import Path

# ---------------- Parameters ----------------
L = 230.0
W = 230.0
H = 100.0

HOLE_D = 15.0
HOLE_R = HOLE_D / 2.0
HOLE_DEPTH = 25.0  # depth from top face downward

EDGE_FILLET = 2.0  # small fillet for nicer edges (optional)

# 4 holes in 2x2 grid, make hole-to-hole spacing ~= hole-to-edge spacing
# Using offsets at L/6 & 5L/6 => margin = L/6, spacing = 4L/6, so equal.
def hole_points(l=L, w=W):
    dx = l / 6.0
    dy = w / 6.0
    xs = [-l / 2.0 + dx, l / 2.0 - dx]
    ys = [-w / 2.0 + dy, w / 2.0 - dy]
    return [(x, y) for x in xs for y in ys]


# ---------------- Build brick0 ----------------
base = cq.Workplane("XY").box(L, W, H, centered=(True, True, True))

# Top face workplane and cut 4 holes
result = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_points())
    .hole(HOLE_D, HOLE_DEPTH)
)

# Optional: soften outside edges
result = result.edges("|Z").fillet(EDGE_FILLET)

# Show in CQ-editor if available
try:
    show_object(result)  # type: ignore  # noqa: F821
except Exception:
    pass

# Export STL
out_path = Path(__file__).with_name("brick0.stl")
exporters.export(result, str(out_path))
print(f"Exported: {out_path.resolve()}")
