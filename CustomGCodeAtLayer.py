
from ..Script import Script


class CustomGCodeAtLayer(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Custom GCode At Layer",
            "key": "CustomGCodeAtLayer",
            "metadata": {},
            "version": 2,
            "settings":
            {
                 "z_height":
                {
                    "label": "Z Height in mm",
                    "description": "Z height before which to insert the GCode.  Eg: 1.8",
                    "type": "str",
                    "default_value": ""
                },
                "gcode_to_add":
                {
                    "label": "GCODE to insert.",
                    "description": 'GCODE to add before or after layer change.  Copy and paste a block of lines.  Do not include "\n" newline characters.'
                    "type": "str",
                    "default_value": ""
                }
            }
        }"""

    def execute(self, data):
        i = 0
        # Works without "\n" characters - just copy and paste the lines into the field.
        gcode_to_add = f'{self.getSettingValueByKey("gcode_to_add")}'
        tzh = self.getSettingValueByKey("z_height").strip()
        for layer in data:
            z = layer.split("Z")
            if len(z) < 2:
                break
            z = z[1].split("\n")[0].strip()
            if z == tzh:
                l = layer.split("NONMESH")
                if len(l) < 2:
                    break
                data[i] = l[0] + "NONMESH\n" + gcode_to_add.strip() + l[1]
                break
            i += 1
        return data
