""" InstLumiRatiosToBran Canvas [HighChart]
"""
from katex2html import katex2html
from base_generator import BaseGenerator
from omsapi import OMSAPI
from datetime import datetime
from katex2html import katex2html
from dateutil.parser import parse
import dateutil.parser


class InstLumiRatiosToBran(BaseGenerator):
    def __init__(self):

        super().__init__()

        self.name = "InstLumiRatiosToBran"  # without extention
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
                "showEmpty": True,
                "labels": {
                    "format": "{value:%H:%M}"
                },
                "gridLineWidth": 1
            },
            "yAxis": {
                "showEmpty": True,
                "title": {
                },
                "gridLineWidth": 1
            },
            "legend": {
                "enabled": True,
                "verticalAlign": "top"
            },
            "tooltip": {
                "shared": True
            },
            "series": []
        }

    def append_series(self, avgs, avgs_bran, series_config):
        """ append series with ratio values by doing division

            Args:
                avgs (array): is being passed from load_data
                and is array where averaged values are

                avgs_bran (array): is being passed from load_data and is
                array where averaged bran values are

                series_config (dict) we pass our config dictionary
        """

        for avg in avgs:

            for avg_bran in avgs_bran:

                if avg[0] == avg_bran[0] and avg[1] != 0 and avg_bran[1] != 0:

                    series_config["data"].append(
                        [avg[0], avg[1] / avg_bran[1]])

    def calculate_averages(self, grouped, arr):
        """ Calculates averages of our grouped arrays (by minute)

            Args:
                grouped (array): is being passed from load_data
                and is array where grouped by minute array values are

                arr (array): is being passed from load_data and is
                array where we gonna bet putting calculated values
        """

        for i in range(len(grouped)):
            arr.append([float(sum(l))/len(l)
                        for l in zip(*grouped[i])])

    def _loadData(self, fill_nr):

        hf_bran = {
            "name": "HF/BRAN",
            "color": "#ff0000",
            "data": [
            ],
            "marker": {
                "radius": 2
            },
            "showInLegend": True
        }

        pltz_bran = {
            "name": "PLTZ/BRAN",
            "color": "#00FF00",
            "data": [
            ],
            "marker": {
                "radius": 2
            },
            "showInLegend": True
        }

        bcmf_bran = {
            "name": "BCMF/BRAN",
            "color": "#4169e1",
            "data": [
            ],
            "marker": {
                "radius": 2
            },
            "showInLegend": True
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
        query.attrs(["hf_inst_lumi", "pltzero_inst_lumi",
                     "bcmf_inst_lumi", "dip_time"])
        query.paginate(1, 9000)
        query.filter("dip_time", start_time, "GT")
        query.filter("dip_time", end_time, "LT")
        query.filter("source_dir", "dip/CMS/BRIL/Luminosity", "EQ")
        response = query.data()
        points = response.json()
        print(len(points["data"]))

        query_brana = omsapi.query("diplogger")
        query_brana.attrs(["mean_luminosity", "dip_time"])
        query_brana.paginate(1, 9000)
        query_brana.filter("dip_time", start_time, "GT")
        query_brana.filter("dip_time", end_time, "LT")
        query_brana.filter(
            "source_dir",
            "dip/acc/LHC/Beam/LuminosityAverage/BRANA.4R5", "EQ")
        response_brana = query_brana.data()
        points_brana = response_brana.json()

        grouped_by_minute_hf = []
        current_hf = []  # for grouping by minutes
        grouped_by_minute_plt = []
        current_plt = []  # for grouping by minutes
        averages_hf = []
        averages_plt = []
        grouped_by_minute_bcmf = []
        current_bcmf = []  # for grouping by minutes
        averages_bcmf = []
        grouped_by_minute_brana = []
        current_brana = []  # for grouping by minutes
        averages_brana = []

        ratio = InstLumiRatiosToBran()

        for point in points["data"]:
            point = point["attributes"]

            time_raw = point["dip_time"]

            time_raw = dateutil.parser.parse(time_raw)

            # without seconds for ratios
            no_seconds = time_raw.strftime("%Y-%m-%dT%H:%MZ")

            millisec = parse(no_seconds).timestamp()*1000

            if current_bcmf:

                if abs(current_bcmf[0][0] - millisec) >= 60000:
                    grouped_by_minute_bcmf.append(current_bcmf)
                    current_bcmf = []

            current_bcmf.append([millisec, point["bcmf_inst_lumi"]])

            if current_plt:

                if abs(current_plt[0][0] - millisec) >= 60000:
                    grouped_by_minute_plt.append(current_plt)
                    current_plt = []

            current_plt.append([millisec, point["pltzero_inst_lumi"]])

            if current_hf:

                if abs(current_hf[0][0] - millisec) >= 60000:
                    grouped_by_minute_hf.append(current_hf)
                    current_hf = []

            current_hf.append([millisec, point["hf_inst_lumi"]])

        if current_bcmf:
            grouped_by_minute_bcmf.append(current_bcmf)

        if current_hf:
            grouped_by_minute_hf.append(current_hf)

        if current_plt:
            grouped_by_minute_plt.append(current_plt)

        for point in points_brana["data"]:
            point = point["attributes"]

            time_raw = point["dip_time"]

            time_raw = dateutil.parser.parse(time_raw)

            # without seconds for ratios
            no_seconds = time_raw.strftime("%Y-%m-%dT%H:%MZ")

            millisec = parse(no_seconds).timestamp()*1000

            if current_brana:

                if abs(current_brana[0][0] - millisec) >= 60000:
                    grouped_by_minute_brana.append(current_brana)
                    current_brana = []

            current_brana.append([millisec, point["mean_luminosity"]])

        if current_brana:
            grouped_by_minute_brana.append(current_brana)

        ratio.calculate_averages(grouped_by_minute_brana, averages_brana)
        ratio.calculate_averages(grouped_by_minute_hf, averages_hf)
        ratio.calculate_averages(grouped_by_minute_plt, averages_plt)
        ratio.calculate_averages(grouped_by_minute_bcmf, averages_bcmf)

        ratio.append_series(averages_plt, averages_brana, pltz_bran)
        ratio.append_series(averages_bcmf, averages_brana, bcmf_bran)
        ratio.append_series(averages_hf, averages_brana, hf_bran)

        self.config["xAxis"]["title"] = {
            "text": "{} to {} UTC".format
            (start_time.replace("T", " ").replace("Z", " "),
             end_time.replace("T", " ").replace("Z", " "))
        }
        self.config["title"]["text"] = "Fill {} Inst lumi ratios to BRAN".format(
            fill_nr)
        self.config["series"].append(hf_bran)
        self.config["series"].append(pltz_bran)
        self.config["series"].append(bcmf_bran)

if __name__ == "__main__":

    chart = InstLumiRatiosToBran()
    chart._loadData(7125)
    chart.export()
