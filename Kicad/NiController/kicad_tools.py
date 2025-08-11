import pcbnew
import re
import math

def __extractRefNumber(module):
    matchResult = re.findall('\d+', module.GetReference())
    return int(matchResult[0])

#正規表現にマッチしたMODULEをリストにして返す
#sort=Trueにするとリファレンスの番号順にソートする
def find_modules(pattern, sort=False):
    re_pattern = re.compile(pattern)
    moduleList = []
    for module in pcbnew.GetBoard().GetFootprints():
        if re_pattern.match( module.GetReference() ):
            moduleList.append(module)
    if sort:
        moduleList = sorted(moduleList, key=__extractRefNumber)

    return moduleList

#文字列のリストを渡すと、文字列と一致したリファレンスをもつMODULEのリストを返す
def find_modules_strings(refList):
    moduleList = []
    for ref in refList:
        found = pcbnew.GetBoard().FindFootprintByReference(ref)
        if found:
            moduleList.append(found)

    return moduleList


def place_circle(modules, start_angle, center, radius, component_offset=0, hide_ref=True, lock=False, mils=True):
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
    deg_per_idx = 360 / len(modules)
    grid_origin = pcb.GetDesignSettings().GetGridOrigin()
    print(grid_origin)
    for idx, part in enumerate(modules):
        angle = (deg_per_idx * idx + start_angle) % 360
        # print("{0}: {1}".format(part.GetName(), angle))
        xmils = center[0] + math.cos(math.radians(angle)) * radius
        ymils = center[1] + math.sin(math.radians(angle)) * radius
        pos = pcbnew.VECTOR2I()
        if mils:
            pos = pcbnew.VECTOR2I(pcbnew.FromMils(xmils), pcbnew.FromMils(ymils))
        else:
            pos = pcbnew.VECTOR2I(pcbnew.FromMM(xmils), pcbnew.FromMM(ymils))
        part.SetPosition(grid_origin + pos)
        part.SetOrientation(pcbnew.EDA_ANGLE(component_offset - angle))
        if hide_ref is not None:
            part.Reference().SetVisible(not hide_ref)
    print("Placement finished. Press F11 to refresh.")

def place_all(d_radius, c_radius):
    d_name_list = [
        [f"D{group:02d}{i:02d}" for i in range(1, 17)]
        for group in range(14, 22)
    ]
    d_list = [find_modules_strings(ref_list) for ref_list in d_name_list]
    for id, d_inner_list in enumerate(d_list):
        center = [id % 4 * 25 - 37.5, math.floor(id / 4) * 25 - 12.5]
        place_circle(d_inner_list, 90, center, d_radius, 180, mils = False)
    c_name_list = [
        [f"C{group:02d}{i:02d}" for i in range(1, 17)]
        for group in range(14, 22)
    ]
    c_list = [find_modules_strings(ref_list) for ref_list in c_name_list]
    for id, c_inner_list in enumerate(c_list):
        center = [id % 4 * 25 - 37.5, math.floor(id / 4) * 25 - 12.5]
        place_circle(c_inner_list, 90, center, c_radius, 180, mils = False) 

# import kicad_tools
# import importlib
# importlib.reload(kicad_tools)
# ledList = kicad_tools.find_modules(“D\d+”)
# kicad_tools.place_circle(ledList, 0, (0, 0), 300)
# kicad_tools.place_circle(ledList, 0, (0, 0), 500)