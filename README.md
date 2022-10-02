# Weather_dasboard
 
 ## How to set up environment and run scraper file
 1. Create virtual environment
 2. Install library

    `pip install -r requirement.txt`

 3. Install chrome driver from https://chromedriver.chromium.org/downloads
 4. Edit month and day in main function 
 6. Run file scrape.py

 `python3 scrape.py` 

## How to run dashboard and set up environment for development
1. `git clone https://github.com/KanokpatS/Weather_dasboard.git`
2. `git checkout -b {your branch}`
3. Build docker image

  `docker build -t weather_dashboard .`
  
4. Build docker container

  `docker run -it --name weather_dashboard -v $PWD\:/app -p 8050:8050 weather_dashboard`
  
5. Run file app.py
  
   `cd dashboard` 
  
   `python3 app.py`
   
## How to deploy dashboard
1. Add below ommand in Dockerfile
    `ADD . /app/

    ENTRYPOINT [ "python3" ]
    CMD ["dashboard/app.py"]`
    ![image](https://user-images.githubusercontent.com/67723788/193453157-e5438dda-1f34-478a-bd1f-b186fe6705b8.png)

2. Build docker image

  `docker build -t weather_dashboard .`
  
3. Test docker container

  `docker run -it --name weather_dashboard -p 8050:8050 weather_dashboard`
  
4. Login dokerhub
  `docker login`

5. Tag and push docker image into dokcerhub
  `docker tag weather_dashboard {docker username}/weather_dashboard:{version}`

  `docker push {docker username}/weather_dashboard:{version}`
  
6. 
