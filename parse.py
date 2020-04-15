#parse.py
import wget
from pathlib import Path
import urllib


with open("./htmlpdflinks.txt") as f:
    content = f.readlines()

# strip trailig newlines
content = [x.strip() for x in content]

for line in content:
    #parts = line.split(" ", 1) #split on first space
    #parts[0] = filename
    #parts[1] = link
    
    name_from_path = line.split("/")[-1]
    

    my_file = Path(name_from_path)
    if not my_file.is_file():
        # file exists
            
        try:
            
            wget.download("http://www.frankshospitalworkshop.com/equipment/" + line)
        except urllib.error.HTTPError as e:
            print(line + " failed with HTTP error")
            print(e)
    else:
        print(name_from_path + ": file exists")
        
