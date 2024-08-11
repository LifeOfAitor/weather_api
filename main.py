from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# load only once stations.txt to get info for the table on home.html
filename_home = "data_small/stations.txt"
stations = pd.read_csv(filename_home, skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


def reformat(date, station, temperature):
    return {
        "date": date,
        "station": station,
        "temperature": temperature
    }


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    # read the data
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    # prepare data to render
    data = reformat(date, station, temperature)
    return render_template("output.html", data=data)


@app.route("/api/v1/<station>")
def get_station(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def get_year(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    years = (df[df["    DATE"].str.startswith(str(year))].
             to_dict(orient="records"))
    return years


if __name__ == "__main__":
    app.run(debug=True)
