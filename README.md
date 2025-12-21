# Overview (Project in Progress):
**Live Website:** [Website](https://worldcivilliberties.pythonanywhere.com/) <br>
This project is an interactive web platform that visualizes global civil liberties scores and documented cases of digital authoritarianism from 1972 to 2024. <br>
This platform combines relational data modeling, interactive geospacial visualization, and data-driven storytelling to make complex human rights data accessible to a broader audience of educators, researchers, and the general public. 

# Motivation: 
This website aims to raise awareness of civil liberties and digital authoritarianism cases from around the world by connecting long-term civil liberty trends with concrete case-level events. 

# Tech Stack:
**Backend**: Python flask <br>
**Database**: SQL (relational database that links countries, scores, and cases) <br>
**Frontend**: HTML, CSS, JavaScript <br>
**Visualization**: 3D intercative worldmap from: [globe origin](https://www.amcharts.com/demos/rotating-globe/)<br>
**Analytics**: Google Analytics <br>
**Data Analysis (In Progress)**: scikit-learn (K-means)

# Data:
**[Civil Liberty Scores](https://freedomhouse.org/report/freedom-world)**: 1972-2024 (country-year level) <br>
**[Digital Authoritarianism Cases](https://advox.globalvoices.org/special/unfreedom-monitor/)**: event-level descriptions linked to countries <br>
The relational database design joins longitudinal scores with qualitative case data. 

# Features:
1) User can use the interactive 3D world map to explore civil liberties by country. <br>
2) User can explore country-level civil liberty scores and linked case descriptions in year-level. <br>
3) Visualization of civil liberty score trajectories.

# User Engagement:
I utilized Google Analytics to gather insights on the usage of the website and implemented design decisions accordingly. <br>
-The visualization page accounted for 78 engagement events. <br>
-Average session duration: 1:16s <br>

# Project Status:
This project is in progress as I'm implementing K-means clustering to group countries by similarity in civil liberty score trajectories. My goal is to identify regional or temporal patterns of repression beyond individual cases.





