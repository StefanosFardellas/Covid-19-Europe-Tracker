# Covid-19-Europe-Tracker

Hello! This is a repo I created about Covid-19 stats and graphs regarding Europe.

In ***covid_tracker.py*** file I collect all my datas from my 
dataset, which is Wikipedia's page, through **pandas**.
Next, I save my dataframe into datasets/data.csv. 
Then I use **folium** to create three maps and visualise 
the datas using datasets/countries.geo.json file (**cases.html**, **deaths.html** and **recoveries.html**) and 
I save them into maps directory as html files. Lastly, 
I use **selenium** to open the html files through a browser 
and take screenshots of them, which I save into 
static/photos directory. 

In ***app.py*** file I am using **flask** framework to create a simple one-page website where 
I will be able to show the photos from the static directory. 

My dataset I collected from Wikipedia is 
not big enough and I am trying to find more, so I can make more graphs, so the work is not done and I 
will finish the project.
