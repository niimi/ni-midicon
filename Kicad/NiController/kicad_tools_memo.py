import kicad_tools
import importlib
importlib.reload(kicad_tools)
ledList = kicad_tools.find_modules("D\d+")
kicad_tools.place_circle(ledList, 0, (0, 0), 300)
kicad_tools.place_circle(ledList, 0, (0, 0), 500)


dNameList = [f"D{i}" for i in range(1, 17)]
dList = kicad_tools.find_modules_strings(dNameList)


cNameList = [f"C{i}" for i in range(301, 317)]
cList = kicad_tools.find_modules_strings(cNameList)
kicad_tools.place_circle(cList, 90, (0, 0), 250, 180)


kicad_tools.find_modules_strings(dNameList)
dList = kicad_tools.find_modules_strings(dNameList)
kicad_tools.place_circle(dList, 90, (0, 0), 400, 180)


cNameList = [f"C{i}" for i in range(1401, 1417)]
cList = kicad_tools.find_modules_strings(cNameList)
kicad_tools.place_circle(cList, 90, (-37.5, -12.5), 7, 180, mils=False)

dNameList = [
    [f"D{group:02d}{i:02d}" for i in range(1, 17)]
    for group in range(14, 22)
]

dList = [kicad_tools.find_modules_strings(ref_list) for ref_list in dNameList]
