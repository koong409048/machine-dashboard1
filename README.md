# Machine Dashboard

Real-time machine monitoring dashboard built with Python + Streamlit.
A first step toward IT/OT integration: connecting PLC data to a web dashboard.

## Features
- Machine status: RUN / STOP / ALARM
- Production counter
- Accumulated downtime
- Availability (%)
- Live production chart (updates every 1 second)

## How to run
pip install streamlit pandas
streamlit run app.py

Then open http://localhost:8501

## Roadmap
- [x] Dashboard with simulated machine data
- [ ] Read live data from PLC (Siemens S7 via Snap7 / OPC UA)
- [ ] Store history in a database (PostgreSQL / InfluxDB)
- [ ] Multi-machine support (Siemens, Mitsubishi, Omron)

## About
Built by a PLC programmer (Siemens, Mitsubishi, Omron) learning IT/OT integration.
