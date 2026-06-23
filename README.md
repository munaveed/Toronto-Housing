# Toronto RentSafe Data Pipeline & Dashboard 🚀

## Overview
This project is an end-to-end Data Engineering and Analytics pipeline. It extracts live building safety evaluation data from the Toronto municipal Open Data API, processes it using Python, loads it into a local SQL Server database, and visualizes the results in an interactive Power BI dashboard.

## Tech Stack
* **Python:** API extraction, data cleaning (Pandas)
* **SQL Server:** Relational database storage
* **Power BI:** Interactive geospatial visualization and reporting

## Features
* Automated data extraction from the City of Toronto API.
* "Wall of Shame" bar chart highlighting the lowest-scoring buildings.
* Interactive Azure Map visualizing property safety scores across Toronto neighborhoods using custom red-to-green gradients.
* Data linked interactively—clicking a building in the charts isolates its location on the map.

