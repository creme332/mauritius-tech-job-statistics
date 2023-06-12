# myjobviz  

![Build status of workflow](https://github.com/creme332/mauritius-tech-job-statistics/actions/workflows/scrape.yml/badge.svg) ![job-count-1](https://img.shields.io/badge/Total%20jobs%20scraped-2496-orange) ![Badge for test workflow](https://github.com/creme332/mauritius-tech-job-statistics/actions/workflows/test.yml/badge.svg)

Visualize the latest job trends in the IT job market in Mauritius. 

![GIF of visualised data](archive/website-v2.gif)

[▶ Live preview](myjobviz.web.app)

# How it works
1. A selenium web scraper fetches new jobs from myjob.mu on a daily basis.
2. Scraped data is processed and saved to Firestore database.
3. `myjobviz` website fetches processed data from Firestore and creates charts.
# Usage

View instructions on how to setup the project locally [here](docs/setup.md).

# Disclaimer

Please be aware that while efforts have been made to ensure accurate representation and meaningful interpretations, there is a possibility of misinterpretations or errors in the analysis. The conclusions drawn from the data should be approached with caution.

# To-do 
* [ ] Add a workflow to backup database (and maybe release a public version).
* [ ] Add more tests using test sample data.
* [ ] Add workflow to check for duplicates.
* [ ] Frontend
  + [ ] Add a choropleth map
  + [ ] Add [offline support](https://firebase.google.com/docs/firestore/manage-data/enable-offline#web-modular-api)
* [ ] Use typescript on frontend
* [ ] Generate charts on backend
# Acknowledgements

Project was inspired by the [Stack Overflow Developer survey](https://insights.stackoverflow.com/survey).
