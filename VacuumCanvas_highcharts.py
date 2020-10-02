""" Vacum Canvas [HighChart]
"""
from base_generator import BaseGenerator
from omsapi import OMSAPI
from dateutil.parser import parse
from katex2html import katex2html


class Vacum(BaseGenerator):
    def __init__(self):

        super().__init__()

        self.name = "Vacum"  # without extention
        self.config = {
            "chart": {
                "zoomType": "x",
                "height": 472,
                "width": 696,
                "type": "line"
            },
            "credits": {
                "enabled": False
            },
            "title": {
                "text": ""
            },
            "xAxis": {
                "type": "datetime",
                "labels": {
                    "format": "{value:%H:%M}"
                },
                "gridLineWidth": 1
            },
            "yAxis": {
                "type": "logarithmic",
                "title": {
                    "useHTML": True,
                    "text": "Preasure [Torr]"
                }
            },
            "legend": {
                "enabled": "true",
                "verticalAlign": "top",
            },
            "tooltip": {
                "shared": True,
                "xDateFormat": "%Y-%m-%d %H:%M:%S"
            },
            "series": []
        }

    def _loadData(self, fill_nr):

        vgi_183_1r5 = {
            "name": "VGI_183_1R5",
            "color": "#9bccb4",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgi_183_1l5 = {
            "name": "VGI_183_1L5",
            "color": "#876656",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgi_220_1r5 = {
            "name": "VGI_220_1R5",
            "color": "#dbd79d",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgi_220_1l5 = {
            "name": "VGI_220_1L5",
            "color": "#ce5e60",
            "data": [
            ],
            "marker": {
                "radius": 1 
            },
            "showInLegend": "true"
        }

        vgpb_7_4l5 = {
            "name": "VGPB_7_4L5",
            "color": "#000000",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgpb_7_4r5 = {
            "name": "VGPB_7_4R5",
            "color": "#ff0000",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgpb_147_1r5 = {
            "name": "VGPB_147_1R5",
            "color": "#00ff00",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgpb_147_1l5 = {
            "name": "VGPB_147_1L5",
            "color": "#2f2fff",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgpb_148_1r5 = {
            "name": "VGPB_148_1R5",
            "color": "#ffff5f",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgpb_148_1l5 = {
            "name": "VGPB_148_1L5",
            "color": "#ff00ff",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgpb_183_1r5 = {
            "name": "VGPB_183_1R5",
            "color": "#00ffff",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgpb_183_1l5 = {
            "name": "VGPB_183_1L5",
            "color": "#59d354",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgpb_220_1r5 = {
            "name": "VGPB_220_1R5",
            "color": "#635eda",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        vgpb_220_1l5 = {
            "name": "VGPB_220_1L5",
            "color": "#c0b6ac",
            "data": [
            ],
            "marker": {
                "radius": 1
            },
            "showInLegend": "true"
        }

        start_time = ""
        end_time = ""
        omsapi = OMSAPI()
        omsapi.auth_cert()

        get_time_range = omsapi.query("fills")
        get_time_range.attrs(["start_stable_beam", "end_stable_beam"])
        get_time_range.filter("fill_number", fill_nr, "EQ")
        data = get_time_range.data()
        fillpoint = data.json()

        for point in fillpoint["data"]:
            point = point["attributes"]
            start_time = point["start_stable_beam"]
            end_time = point["end_stable_beam"]

        query = omsapi.query("diplogger")
        query.attrs(
            [
                "first_dip_time",
                "vgi_183_1r5", "vgi_183_1l5",
                "vgi_220_1r5", "vgi_220_1l5",
                "vgpb_7_4l5", "vgpb_7_4r5",
                "vgpb_147_1r5", "vgpb_147_1l5",
                "vgpb_148_1r5", "vgpb_148_1l5",
                "vgpb_183_1r5", "vgpb_183_1l5",
                "vgpb_220_1r5", "vgpb_220_1l5"
            ])
        query.paginate(1, 100000)
        query.filter("dip_time", start_time, "GT")
        query.filter("dip_time", end_time, "LT")
        query.custom("group[count]", 1000)
        query.filter("source_dir", "dip/CMS/BRIL/VacSummary", "EQ")
        query.sort("dip_time", True)
        response = query.data()
        points = response.json()

        for point in points["data"]:
            point = point["attributes"]
            unix = parse(point["first_dip_time"]).timestamp()*1000

            vgi_183_1r5["data"].append([unix, point["vgi_183_1r5"]])
            vgi_183_1l5["data"].append([unix, point["vgi_183_1l5"]])
            vgi_220_1r5["data"].append([unix, point["vgi_220_1r5"]])
            vgi_220_1l5["data"].append([unix, point["vgi_220_1l5"]])
            vgpb_7_4l5["data"].append([unix, point["vgpb_7_4l5"]])
            vgpb_7_4r5["data"].append([unix, point["vgpb_7_4r5"]])
            vgpb_147_1r5["data"].append([unix, point["vgpb_147_1r5"]])
            vgpb_147_1l5["data"].append([unix, point["vgpb_147_1l5"]])
            vgpb_148_1r5["data"].append([unix, point["vgpb_148_1r5"]])
            vgpb_148_1l5["data"].append([unix, point["vgpb_148_1l5"]])
            vgpb_220_1r5["data"].append([unix, point["vgpb_220_1r5"]])
            vgpb_220_1l5["data"].append([unix, point["vgpb_220_1l5"]])
            vgpb_183_1r5["data"].append([unix, point["vgpb_183_1r5"]])
            vgpb_183_1l5["data"].append([unix, point["vgpb_183_1l5"]])

        self.config["xAxis"]["title"] = {
            "text": "{} to {} UTC".format
            (start_time.replace("T", " ").replace("Z", " "),
             end_time.replace("T", " ").replace("Z", " "))
        }

        self.config["series"].append(vgi_183_1r5)
        self.config["series"].append(vgi_183_1l5)
        self.config["series"].append(vgi_220_1r5)
        self.config["series"].append(vgi_220_1l5)
        self.config["series"].append(vgpb_7_4l5)
        self.config["series"].append(vgpb_7_4r5)
        self.config["series"].append(vgpb_147_1r5)
        self.config["series"].append(vgpb_147_1l5)
        self.config["series"].append(vgpb_148_1r5)
        self.config["series"].append(vgpb_148_1l5)
        self.config["series"].append(vgpb_220_1r5)
        self.config["series"].append(vgpb_220_1l5)
        self.config["series"].append(vgpb_183_1r5)
        self.config["series"].append(vgpb_183_1l5)
        self.config["title"]["text"] = "Fill {} Vacuum pressure All".format(
            fill_nr)


if __name__ == "__main__":

    chart = Vacum()
    chart._loadData(7109)
    chart.export()
