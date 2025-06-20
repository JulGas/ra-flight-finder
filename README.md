# Ryanair Flight Finder ✈️

A lightweight Streamlit app to search Ryanair one-way flights between base airports and visualise prices with intuitive colour highlights.

## Overview

This tool is ideal for **flexible travellers** who want to discover the cheapest days to fly between two Ryanair hubs.  
It scans flights over a chosen date range and highlights price trends in a simple table.

## Features

- Search between all **Ryanair base airports**
- Define **start/end date** and filter by **days of the week**
- Flights displayed in a table:
  - **Green** = cheapest
  - **Red** = most expensive
- Summary statistics: min, max, and average price

## Disclaimer

- Prices come directly from Ryanair’s **public API**
- All prices are displayed in **Euro (EUR)**
- Data is **not guaranteed to be complete or accurate** — Ryanair may change availability or prices at any time
- This tool is provided as-is, without any guarantees regarding:
  - Price accuracy or availability
  - Completeness or correctness of data
  - Stability of Ryanair's API

I do not guarantee correctness, and I take no responsibility for errors, missing data, or booking decisions made using this tool.

## Installation & Usage

Run the app in one line:

```bash
pip install -r https://raw.githubusercontent.com/JulGas/ryanair-flight-finder/main/requirements.txt && streamlit run https://raw.githubusercontent.com/JulGas/ryanair-flight-finder/main/ryan.py
