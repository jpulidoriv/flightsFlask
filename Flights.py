import requests
import pandas as pd

origen = input("Origen: ")
destino = input("Destino: ")
fecha_ida = input("Fecha de ida (aaaa-mm-dd): ")
fecha_regreso = input("Fecha de regreso (aaaa-mm-dd): ")

params = {
    "originLocationCode": origen,
    "destinationLocationCode": destino,
    "departureDate": fecha_ida,
    "returnDate": fecha_regreso,
    "adults": 1,
    "max": 7
}


url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
access_token = "************************"

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
                    "Hora Salida": departure.get("at", "N/A").replace('T', ' '),
                    "Llegada": arrival.get("iataCode", "N/A"),
                    "Hora Llegada": arrival.get("at", "N/A").replace('T', ' ')
                })

    if vuelos_data:
        df = pd.DataFrame(vuelos_data)
        df.to_csv("vuelos.csv", index=False)
        print("Datos guardados en 'vuelos.csv'.")
    else:
        print("No se encontraron vuelos.")
else:
    print("Error en la solicitud:", response.status_code, response.text)
