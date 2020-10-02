""" PileUpAverage Canvas [HighChart]
"""
from base_generator import BaseGenerator
from omsapi import OMSAPI
from dateutil.parser import parse


class PileUpAverage(BaseGenerator):
    def __init__(self):

        super().__init__()

        self.name = "PileUpAverage"  # without extention
        self.config = {
            "chart": {
                "zoomType": "x",
                "height": 472,
                "width": 696,
                "type": "scatter"
            },
            "credits": {
                "enabled": False
            },
            "title": {
                "text": ""
            },
            "xAxis": {
                "labels": {
                    "format": "{value:%H:%M}"
                },
                "gridLineWidth": 1
            },
            "yAxis": {
                "title": {
                    "text": "Pileup Average"
                }
            },
            "legend": {
                "enabled": "true",
                "verticalAlign": "top"         
            },
            "tooltip": {
                "shared": True,
                "pointFormat": "X: {point.x:%Y-%m-%d %H:%M:%S} <br/> Y: {point.y}"
            },
            "series": []
        }

    def _loadData(self, fill_nr):

        pileup_series = {
            "name": "Pileup average",
            "color": "#4169e1",
            "data": [
            ],
            "marker": {
                "radius": 2
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
        arr_time = []

        for point in fillpoint["data"]:
            point = point["attributes"]
            start_time = point["start_stable_beam"]
            end_time = point["end_stable_beam"]

        query = omsapi.query("diplogger")
        query.attrs(["avg_pile_up", "dip_time"])
        query.paginate(1, 50000)
        query.filter("dip_time", start_time, "GT")
        query.filter("dip_time", end_time, "LT")
        query.filter("source_dir", "dip/CMS/BRIL/Luminosity", "EQ")

        response = query.data()
        points = response.json()

        for point in points["data"]:
            point = point["attributes"]
            unix = parse(point["dip_time"]).timestamp()*1000
            arr_time.append(point["dip_time"])

            pileup_threshold = 110.0

            if point["avg_pile_up"] < pileup_threshold:
                pileup_series["data"].append([unix, point["avg_pile_up"]])

        self.config["xAxis"]["title"] = {
            "text": "{} to {} UTC".format
            (start_time.replace("T", " ").replace("Z", " "),
             end_time.replace("T", " ").replace("Z", " "))
        }

        self.config["series"].append(pileup_series)
        self.config["title"]["text"] = "Fill {} Pileup Average".format(fill_nr)


if __name__ == "__main__":

    chart = PileUpAverage()
    chart._loadData(7125)
    chart.export()
