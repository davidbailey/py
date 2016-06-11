import re

title_pattern = '" PRIVATE="0" TAGS="">(.*)</A>'
link_pattern = '<DT><A HREF="(.*)" ADD_DATE.*'
date_pattern = 'ADD_DATE="(.*)" PRIVATE="0"'

with open('Desktop/delicious.html') as f:
  for line in f:
    title = re.search(title_pattern,line).group(1)
    link = re.search(link_pattern,line).group(1)
    date = re.search(date_pattern,line).group(1)
    print("\"" + title + "\",\"" + link + "\"," + date)
