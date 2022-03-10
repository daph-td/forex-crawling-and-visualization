# forex-crawling-and-visualization
A full stack website where users can input their currency pairs of choice, time intervals (eg. starting date, ending date), timeframe (eg. 1 day, 4 hours, 15 minutes, etc.), and a period of moving average to output the visualization of their inputs.

This project collects the forex data in real time and visualize them on web browser based on user input. The crawler was deployed to gcloud to run 24/7 and the data are storing in MongoDB. 

### Features:
- Scrape the currency pair data of your choice in real time 24/7
- Visualize the base data and the moving average based on user input (starting time, ending time, numbers of bins, timeframe, etc.)
- Web browser for user to input from the frontend

### Tech Stack:
- Backend: Python, MongoDB, Google Cloud Server
- Frontend: Dash
- Data crawler: Selenium, BeautifulSoup4
- Data visualization: Pandas, Matplotlib, Plotly

### Screenshot of the program:
![Screenshot](https://github.com/daph-td/forex-crawling-and-visualization/blob/master/data/Screen%20Shot%202022-03-10%20at%208.39.04%20PM.png)

### Demonstration:
https://youtu.be/h5AHvJesB0E
