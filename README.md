# Weather_dasboard

## How to set up environment and run dashboard
1. Build docker image

  `docker build -t weather_dashboard .`
  
2. Build docker container

  `docker run -it --name weather_dashboard -v $PWD\:/app -p 8050:8050 weather_dashboard`
  
  3. Run file app.py
  
   `cd dashboard` 
  
   `python3 app.py` 
   
   ## How to set up environment and run scraper file
   1. Create virtual environment
   2. Install library
   
      `pip install -r requirement.txt`
      
   3. Install chrome driver from https://chromedriver.chromium.org/downloads
   4. Run file scrape.py
  
   `python3 scrape.py` 
