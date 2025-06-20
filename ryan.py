import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def style_price(val, min_price, max_price):
    """Style the price column with a gradient from green (cheap) to red (expensive)"""
    if pd.isna(val):
        return ''
    if max_price > min_price:
        ratio = (val - min_price) / (max_price - min_price)
    else:
        ratio = 0
    red = int(255 * ratio)
    green = int(255 * (1 - ratio))
    return f'background-color: rgb({red},{green},100)'

def get_ryanair_airports():
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get("https://www.ryanair.com/api/views/locate/5/airports/en/active", headers=headers)
    if response.status_code == 200:
        airports_data = response.json()
        return {a['code']: f"{a['name']} ({a['code']})" for a in airports_data if a.get('base', False)}
    return {}

def get_ryanair_flights(origin, destination, date):
    url = "https://www.ryanair.com/api/farfnd/3/oneWayFares"
    params = {
        "departureAirportIataCode": origin,
        "arrivalAirportIataCode": destination,
        "outboundDepartureDateFrom": date,
        "outboundDepartureDateTo": date,
        "language": "en",
        "market": "de",
        "currency": "EUR"
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        st.error(f"Error fetching flights: {response.status_code}")
        return pd.DataFrame()

    try:
        data = response.json()
    except Exception:
        st.warning("Invalid JSON in response.")
        return pd.DataFrame()

    if "fares" not in data:
        st.warning("No flight data returned.")
        return pd.DataFrame()

    flights = []
    for fare in data["fares"]:
        outbound = fare.get("outbound")
        if not outbound:
            continue

        try:
            departure_dt = datetime.fromisoformat(outbound["departureDate"].replace("Z", ""))
            arrival_dt = datetime.fromisoformat(outbound["arrivalDate"].replace("Z", ""))
            price = round(outbound["price"]["value"], 2)

            flights.append({
                "Date": departure_dt.strftime("%Y-%m-%d"),
                "Day": departure_dt.strftime("%A"),
                "Departure Time": departure_dt.strftime("%H:%M"),
                "Arrival Time": arrival_dt.strftime("%H:%M"),
                "Price": price
            })
        except (KeyError, ValueError):
            continue

    return pd.DataFrame(flights)

def main():
    st.title("Ryanair Flight Finder")
    airports = get_ryanair_airports()
    if not airports:
        st.error("Failed to load airports.")
        return

    col1, col2 = st.columns(2)
    with col1:
        origin = st.selectbox("Select Origin Airport", options=list(airports.keys()), format_func=lambda x: airports[x])
    with col2:
        destination = st.selectbox("Select Destination Airport", options=list(airports.keys()), format_func=lambda x: airports[x])

    today = datetime.now()
    max_date = today + timedelta(days=180)

    col3, col4 = st.columns(2)
    with col3:
        start_date = st.date_input("Start Date", min_value=today, max_value=max_date, value=today)
    with col4:
        end_date = st.date_input("End Date", min_value=start_date, max_value=max_date, value=start_date + timedelta(days=30))

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    selected_days = st.multiselect("Filter by Day of Week", options=days, default=['Friday'])

    if st.button("Search Flights"):
        st.write("Searching for flights...")
        all_flights = []
        current_date = start_date
        while current_date <= end_date:
            flights = get_ryanair_flights(origin, destination, current_date.strftime("%Y-%m-%d"))
            if not flights.empty:
                all_flights.append(flights)
            current_date += timedelta(days=1)

        if all_flights:
            df = pd.concat(all_flights, ignore_index=True)
            if selected_days:
                df = df[df['Day'].isin(selected_days)]
            df = df.sort_values(['Date', 'Departure Time'])

            min_price = df['Price'].min()
            max_price = df['Price'].max()
            styled_df = df.style.applymap(lambda val: style_price(val, min_price, max_price), subset=['Price'])

            st.dataframe(styled_df)
            st.write(f"Cheapest flight: €{min_price:.2f}")
            st.write(f"Most expensive flight: €{max_price:.2f}")
            st.write(f"Average price: €{df['Price'].mean():.2f}")
        else:
            st.warning("No flights found for the selected criteria.")

if __name__ == "__main__":
    main()
