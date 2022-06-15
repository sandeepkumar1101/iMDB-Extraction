import secrets
from imdb import IMDb
from bs4 import BeautifulSoup
import requests
import os 
import sys   
import csv
from googlesearch import search
import urllib




# getting path 
path = os.getcwd()
expath = path+'\movie_info.csv'
expath = expath.split("\\")
doc = '//'
expath = doc.join(expath)
# end of getting path


# create an instance of the IMDb class
ia = IMDb()

# for searching a movie 
to_search = sys.argv[1:]

to_search = ' '.join(map(str, to_search))



movies = ia.search_movie(to_search)

# print(movies[0].movieID)
# print(movies[0]['cover url'])
# rating = movies[0].rating
movieid = movies[0].movieID
movie = ia.get_movie(movieid)
# infosets key willgive you alll the info about the movie 


# print(movie.infoset2keys)

title = movie.get('title')
#trailer link from google
query = title+' trailer'
for result in search(query, stop=10):
    trailer = result
    trailer = trailer.replace('watch?v=','embed/')
    break
# trailer = 'https://www.youtube.com/watch?v=x7Krla_UxRg'
# req format = https://www.youtube.com/embed/x7Krla_UxRg
# trailer find end

genre = str(movie.get('genres'))
genre = genre.replace("'", "''")

try:
   runtime = (movie.get('runtime'))[0]
except TypeError:
  runtime='50'
  
year = movie.get('year')
plot = str(movie.get('plot outline'))
plot = plot.replace("'", "''")
rating = movie.get('rating')

url = ia.get_imdbURL(movies[0])




source = requests.get(url).text


soup = BeautifulSoup(source, 'lxml')

image = soup.find('img', class_='ipc-image')
# images = image.split(' ')
images = image['srcset']
images = images.split(' ')
image = []
image.append(images[0])
image.append(images[2])
image.append(images[4])
images = str(image)
images = images.replace("'", "''")
kind = movie['kind']
if(kind=='tv series'):
 ia.update(movie,'episodes')
 totalSeason = len(movie['episodes'])


with open(expath, 'w' , encoding='utf-8') as f:
  if(kind=='tv series'):
    fieldnames = ['movieid','title','kind','season','year','genre','plot','runtime','rating','url','image','trailer']
    write = csv.writer(f)
    write.writerow(fieldnames)
    row = [movieid,title,kind,totalSeason,year,genre,plot,runtime,rating,url,images,trailer]
    write.writerow(row)  

  else:
    fieldnames = ['movieid','title','kind','year','genre','plot','runtime','rating','url','image','trailer']
    write = csv.writer(f)
    write.writerow(fieldnames)
    row = [movieid,title,kind,year,genre,plot,runtime,rating,url,images,trailer]
    write.writerow(row)  

