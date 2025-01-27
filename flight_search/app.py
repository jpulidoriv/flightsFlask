from flask import Flask, render_template, request, url_for
import requests
import pandas as pd

app = Flask(__name__, template_folder='templates')

@app.route("/", methods=["GET", "POST"])
def search_flights():
    if request.method == "POST":
        origen = request.form.get('origen')
        destino = request.form.get('destino')
        fecha_ida = request.form.get('fecha_ida')
        fecha_regreso = request.form.get('fecha_regreso')

        if not (origen and destino and fecha_ida and fecha_regreso):
            return render_template('base.html', error='All fields are required')

        params = {
            "originLocationCode": origen,
            "destinationLocationCode": destino,
            "departureDate": fecha_ida,
            "returnDate": fecha_regreso,
            "adults": 1,
            "max": 7,
            "currencyCode": "MXN"
        }

        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        access_token = "WResVnKLy3J1sA9G2k3du0HH2knm"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            resultados = response.json().get("data", [])
            vuelos_data = []

            for vuelo in resultados:
                price = vuelo.get("price", {}).get("total", "N/A")
                currency = vuelo.get("price", {}).get("currency", "N/A")

                for itinerary in vuelo.get("itineraries", []):
                    for segment in itinerary.get("segments", []):
                        departure = segment.get("departure", {})
                        arrival = segment.get("arrival", {})
                        carrier_code = segment.get("carrierCode", "N/A")
                        duration = segment.get("duration", "N/A")

                        vuelos_data.append({
                            "Aerolínea": carrier_code,
                            "Precio": f"{price} {currency}",
                            "Duración": duration,
                            "Salida": departure.get("iataCode", "N/A"),
                            "HoraSalida": departure.get("at", "N/A").replace('T', ' '),
                            "Llegada": arrival.get("iataCode", "N/A"),
                            "HoraLlegada": arrival.get("at", "N/A").replace('T', ' ')
                        })

            if vuelos_data:
                df = pd.DataFrame(vuelos_data)
                df.to_csv("vuelos.csv", index=False)
                return render_template('base.html', vuelos=vuelos_data)

        else:
            return render_template('base.html', error=response.text)

    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)
