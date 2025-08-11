import pcbnew
import math


def place_circle(refdes, start_angle, center, radius, component_offset=0, hide_ref=True, lock=False):
    """
    Places components in a circle
    refdes: List of component references
    start_angle: Starting angle
    center: Tuple of (x, y) mils of circle center
    radius: Radius of the circle in mils
    component_offset: Offset in degrees for each component to add to angle
    hide_ref: Hides the reference if true, leaves it be if None
    lock: Locks the footprint if true
    """
    pcb = pcbnew.GetBoard()
    deg_per_idx = 360 / len(refdes)
    grid_origin = pcb.GetDesignSettings().GetGridOrigin()
    for idx, rd in enumerate(refdes):
        part = pcb.FindFootprintByReference(rd)
        angle = (deg_per_idx * idx + start_angle) % 360
        print("{0}: {1}".format(rd, angle))
        xmils = center[0] + math.cos(math.radians(angle)) * radius
        ymils = center[1] + math.sin(math.radians(angle)) * radius
        pos = pcbnew.VECTOR2I(pcbnew.FromMils(xmils), pcbnew.FromMils(ymils))
        part.SetPosition(grid_origin + pos)
        part.SetOrientation(pcbnew.EDA_ANGLE(component_offset - angle))
        # if hide_ref is not None:
        #     part.Reference().SetVisible(not hide_ref)
    print("Placement finished. Press F11 to refresh.")
