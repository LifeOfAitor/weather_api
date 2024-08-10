from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

filename = "data_small/stations.txt"
stations = pd.read_csv(filename, skiprows=17)
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
def translator(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    # read the data
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    # prepare data to render
    data = reformat(date, station, temperature)
    return render_template("output.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
