import cadquery as cq
from math import isfinite

# -----------------------------
# Parameters (copied from FreeCAD macro)
# -----------------------------
L, W = 250.0, 150.0

bottom_h = 100.0
top_h = 35.0
H = bottom_h + top_h
z_split = bottom_h

t = 10.0

outer_fillet_r = 6.0
seal_fillet_r = 0.8

# Boolean-ish parameters (CadQuery typically doesn't need eps, but keep for safety)
eps = 0.05

# Seal rib/groove
rib_w = 4.0
rib_h = 3.0

groove_d = 4.0
clearance_total = 1.0
groove_w = rib_w + clearance_total  # 5.0

ring_offset_from_inner = 0.0  # around inner opening

# Top finger pocket (internal, not through outside)
pocket_w = 60.0
pocket_d = 16.0
pocket_skin = 2.0
pocket_top_margin = 6.0
pocket_from_split = 1.2
pocket_fillet_r = 3.0

# Bottom front lip notch (from outside Y=0, do not cut through to cavity)
lip_w = pocket_w
lip_cut_in = 7.0
lip_keep = 2.0
lip_h = 14.0
lip_from_split_down = 10.0  # (kept for parity; FreeCAD script actually used lip_h only)
lip_fillet_r = 2.5


def _check_params():
    if lip_cut_in >= (t - lip_keep):
        raise ValueError(
            f"lip_cut_in={lip_cut_in} too large; must satisfy lip_cut_in < t - lip_keep = {t - lip_keep}"
        )
    inner_L = L - 2 * t
    inner_W = W - 2 * t
    inner_H = H - 2 * t
    if inner_L <= 0 or inner_W <= 0 or inner_H <= 0:
        raise ValueError("Wall thickness t is too large; inner size <= 0.")
    pocket_z0 = z_split + pocket_from_split
    pocket_z1 = H - pocket_top_margin - pocket_skin
    if pocket_z1 - pocket_z0 <= 1.0:
        raise ValueError("Top too short for finger pocket (pocket_skin/pocket_top_margin too large).")


def _safe_fillet(solid: cq.Workplane, r: float, selector: str, label: str):
    """
    Try a fillet; if it fails, return original.
    selector is a CadQuery edge selector string (e.g. '|Z', '>Z', etc.) or
    a chained selection expression on the passed workplane.
    """
    if r is None or r <= 0 or not isfinite(r):
        return solid
    try:
        return solid.edges(selector).fillet(r)
    except Exception as e:
        print(f"[WARN] fillet failed {label} (r={r}, selector={selector}): {e}")
        return solid


def build_storage_box():
    _check_params()

    # Coordinate convention:
    # - Use a box from (0,0,0) to (L,W,H)
    # - Front is Y=0, back is Y=W
    # - Split plane at Z=z_split
    #
    # CadQuery default .box() is centered; we explicitly build via extrusions with origins.
    outer = cq.Workplane("XY").box(L, W, H, centered=(False, False, False))
    inner = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(t, t, t))
        .box(L - 2 * t, W - 2 * t, H - 2 * t, centered=(False, False, False))
    )
    shell = outer.cut(inner)

    # Outer fillet: FreeCAD macro filleted "outer edges only" with a heuristic.
    # In CadQuery, a robust approximation is to fillet only the vertical outer edges (parallel to Z).
    # This avoids filleting interior/opening edges which can cause failures.
    shell = _safe_fillet(shell, outer_fillet_r, "|Z", "(outer vertical edges)")

    # Split into bottom/top with boxes (common/intersect) to avoid plane split issues.
    bottom_clip = (
        cq.Workplane("XY")
        .box(L + 2 * eps, W + 2 * eps, z_split + eps, centered=(False, False, False))
        .translate((-eps, -eps, -eps))
    )
    top_clip = (
        cq.Workplane("XY")
        .box(L + 2 * eps, W + 2 * eps, (H - z_split) + 2 * eps, centered=(False, False, False))
        .translate((-eps, -eps, z_split - eps))
    )

    bottom = shell.intersect(bottom_clip)
    top = shell.intersect(top_clip)

    # Seal ring extents (around inner opening)
    ix0, iy0 = t, t
    ix1, iy1 = L - t, W - t

    rx0 = ix0 - ring_offset_from_inner
    ry0 = iy0 - ring_offset_from_inner
    rx1 = ix1 + ring_offset_from_inner
    ry1 = iy1 + ring_offset_from_inner

    # --- Top: rib ring, protruding downward from split plane
    rib_outer = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(rx0 - rib_w, ry0 - rib_w, z_split - rib_h))
        .box((rx1 - rx0) + 2 * rib_w, (ry1 - ry0) + 2 * rib_w, rib_h, centered=(False, False, False))
    )
    rib_inner = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(rx0, ry0, z_split - rib_h))
        .box((rx1 - rx0), (ry1 - ry0), rib_h, centered=(False, False, False))
    )
    rib_ring = rib_outer.cut(rib_inner)
    top = top.union(rib_ring)

    # --- Bottom: groove ring, cut downward below split plane
    groove_outer = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(rx0 - groove_w, ry0 - groove_w, z_split - groove_d))
        .box((rx1 - rx0) + 2 * groove_w, (ry1 - ry0) + 2 * groove_w, groove_d, centered=(False, False, False))
    )
    groove_inner = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(rx0, ry0, z_split - groove_d))
        .box((rx1 - rx0), (ry1 - ry0), groove_d, centered=(False, False, False))
    )
    groove_ring = groove_outer.cut(groove_inner)
    bottom = bottom.cut(groove_ring)

    # Seal fillets: try to fillet edges near the split plane.
    # Selector strategy: edges that are mostly in XY (perpendicular to Z) around that area are hard to pick robustly.
    # We approximate by filleting *all* edges created by features may be risky; instead only fillet around Z edges
    # which often exist on the ring walls. This is a compromise vs FreeCAD's bounding-box filter.
    top = _safe_fillet(top, seal_fillet_r, "|Z", "(seal rib walls)")
    bottom = _safe_fillet(bottom, seal_fillet_r, "|Z", "(seal groove walls)")

    # --- Top finger pocket (internal): cut box starting at inner front wall (y=t)
    pocket_z0 = z_split + pocket_from_split
    pocket_z1 = H - pocket_top_margin - pocket_skin
    pocket_h = pocket_z1 - pocket_z0

    px0 = (L - pocket_w) / 2.0
    py0 = t
    pocket_cut = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(px0, py0, pocket_z0))
        .box(pocket_w, pocket_d, pocket_h, centered=(False, False, False))
    )
    top = top.cut(pocket_cut)

    # Finger pocket fillet: best-effort—fillet vertical edges (pocket walls) near that region.
    top = _safe_fillet(top, pocket_fillet_r, "|Z", "(finger pocket vertical edges)")

    # --- Bottom front lip notch: cut from outside front (Y=0) inward by lip_cut_in, but not through cavity.
    lip_z1 = z_split - 1.0
    lip_z0 = max(0.0, lip_z1 - lip_h)

    lx0 = (L - lip_w) / 2.0
    ly0 = -eps
    lip_cut = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(lx0, ly0, lip_z0))
        .box(lip_w, lip_cut_in + eps, (lip_z1 - lip_z0), centered=(False, False, False))
    )
    bottom = bottom.cut(lip_cut)

    bottom = _safe_fillet(bottom, lip_fillet_r, "|Z", "(lip notch vertical edges)")

    # -----------------------------
    # Print placement: both halves open upward
    # - bottom: already open upward (open side at z=z_split)
    # - top: rotate 180 deg about X axis, then lift so Z>=0, then shift to the right
    # -----------------------------
    gap = 20.0

    # top rotate around X axis at origin
    top_solid = top.val()
    top_rot = top_solid.rotate((0, 0, 0), (1, 0, 0), 180)

    # lift so its bounding box minZ is 0
    bb = top_rot.BoundingBox()
    top_lift = -bb.zmin
    top_print = top_rot.translate((0, 0, top_lift))

    # move aside in X
    top_print = top_print.translate((L + gap, 0, 0))

    bottom_print = bottom.val()

    return bottom_print, top_print


if __name__ in ["__main__", "__cqgi__"]:
    bottom_print, top_print = build_storage_box()

    # If running in CQ-editor, show_object is available; otherwise just export STEP for verification.
    try:
        show_object(bottom_print, name="Bottom_Print")
        show_object(top_print, name="Top_Print")
    except NameError:
        # Headless run: export
        cq.exporters.export(bottom_print, "Bottom_Print.step")
        cq.exporters.export(top_print, "Top_Print.step")
        print("[DONE] Exported Bottom_Print.step and Top_Print.step")
