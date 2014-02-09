#!/usr/bin/python
from bson import json_util
from datetime import datetime
import json
import time
from pymongo import MongoClient

#~ Mongo Database
client = MongoClient()
db = client.fablab
usagec = db.usage

dateFormat = "%Y-%m-%d %H:%M:%S"


data = '[{"date": "2014-01-31 13:32:12.489309","duration": 45,"logType": "3Dprinter","material quantity": "3.5cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "564.6mm","filament_diameter": "2.8","file": "../../test.gcode","fill_density": "0.1","gcode-generation": "generated by Slic3r 0.9.10b on 2013-10-06 at 18:26:36","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.79mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "Test"},{"date": "2014-01-31 13:34:38.463646","duration": 45,"logType": "3Dprinter","material quantity": "3.5cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "564.6mm","filament_diameter": "2.8","file": "../../test.gcode","fill_density": "0.1","gcode-generation": "generated by Slic3r 0.9.10b on 2013-10-06 at 18:26:36","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.79mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "Test"},{"date": "2014-01-31 13:43:16.782820","duration": 45,"logType": "3Dprinter","material quantity": "3.5cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "564.6mm","filament_diameter": "2.8","file": "../../test.gcode","fill_density": "0.1","gcode-generation": "generated by Slic3r 0.9.10b on 2013-10-06 at 18:26:36","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.79mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "Test"},{"date": "2014-01-31 13:53:25.439951","duration": "0:02:18","logType": "3Dprinter","material quantity": "3.5cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "564.6mm","filament_diameter": "2.8","file": "/home/fabmanager/test.gcode","fill_density": "0.1","gcode-generation": "generated by Slic3r 0.9.10b on 2013-10-06 at 18:26:36","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.79mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-03 11:15:59.426157","duration": "0:54:10","logType": "3Dprinter","material quantity": "14.1cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "2286.5mm","filament_diameter": "2.8","file": "/home/fabmanager/Bureau/BOB/foot_v1.2_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-03 at 10:21:37","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-03 12:35:04.734811","duration": "0:59:42","logType": "3Dprinter","material quantity": "14.1cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "2286.5mm","filament_diameter": "2.8","file": "/home/fabmanager/Bureau/BOB/foot_v1.2_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-03 at 11:35:03","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-03 13:52:34.909195","duration": "0:07:21","logType": "3Dprinter","material quantity": "0.9cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "142.2mm","filament_diameter": "2.8","file": "/media/fabmanager/KINGSTON16GO/En travaux/roue douche/profil-No2b.soften_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-03 at 13:45:02","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-03 14:34:51.513222","duration": "0:22:03","logType": "3Dprinter","material quantity": "3.5cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "564.6mm","filament_diameter": "2.8","file": "/home/fabmanager/Bureau/BOB/Biped_Brackets_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-03 at 14:05:36","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-03 14:58:07.620400","duration": "0:20:26","logType": "3Dprinter","material quantity": "3.5cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "564.6mm","filament_diameter": "2.8","file": "/home/fabmanager/Bureau/BOB/Biped_Brackets_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-03 at 14:05:36","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-03 15:57:58.224377","duration": "0:56:58","logType": "3Dprinter","material quantity": "14.1cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "2284.4mm","filament_diameter": "2.8","file": "/home/fabmanager/Bureau/BOB/foot_v1.2_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-03 at 15:00:18","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-04 11:00:28.213515","duration": "0:52:03","logType": "3Dprinter","material quantity": "12.6cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "2050.9mm","filament_diameter": "2.8","file": "/home/fabmanager/Bureau/BOB/base_v1.2_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-04 at 10:07:31","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-05 11:03:21.671789","duration": "0:55:29","logType": "3Dprinter","material quantity": "14.1cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "2286.5mm","filament_diameter": "2.8","file": "/home/fabmanager/Bureau/BOB/foot_v1.2_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-05 at 10:02:39","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-06 13:41:53.638963","duration": "0:21:49","logType": "3Dprinter","material quantity": "3.0cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "2286.5mm","filament_diameter": "2.8","file": "/home/fabmanager/Bureau/BOB/foot_v1.2_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-05 at 11:07:07","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"},{"date": "2014-02-06 13:41:53.638963","duration": "0:21:49","logType": "3Dprinter","material quantity": "3.0cm3","object": {"bottom_solid_layers": "3","extrusion_multiplier": "1.00","filament used": "485.0mm","filament_diameter": "2.8","file": "/media/fabmanager/F068-969B/Bague Tranzx pleine cm binary_export.gcode","fill_density": "0.5","gcode-generation": "generated by Slic3r 0.9.10b on 2014-02-06 at 13:19:28","infill extrusion width": "0.79mm","infill_speed": "30","layer_height": "0.27","nozzle_diameter": "0.5","perimeter_speed": "25","perimeters": "3","perimeters extrusion width": "0.79mm","solid infill extrusion width": "0.79mm","top infill extrusion width": "0.32mm","top_solid_layers": "3","travel_speed": "150"},"result": "OK","tool": "RepRapOrange"}]'
data = json.loads(data, object_hook=json_util.object_hook)
for usage in data:
    usage['epoch'] = str(time.mktime(time.strptime(usage['date'].split('.')[0], dateFormat))).split('.')[0]+"."+usage['date'].split('.')[1]
    usagec.insert(usage)
