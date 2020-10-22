# web_image_update_checker
This script checks web pages with images for updates by finding a specified image name in the source code of the web page.

For this script to work one needs to provide web page URL and image URL or image name, after doing so script will find this image on the web page and will save the index of this image in the text file, and in the future will check if the same image is still present by the same index on the same page.

Script have a number of available commands that can also be called by typing only the first letter of the command:  
(c)heck  - checks web pages for image changes and allows to open changed pages in web browser  
(u)pdate - updates all or specified by id, changed images in the text file  
(a)dd    - changes existing entry or adds a new entry, type like this:  add page_url image_url  
(d)elete - deletes existing entry, type like this:  delete page_url  
(l)ist   - lists all entries like this:  id page_url image_name image_index  
(e)xit   - stops the program  
(h)elp   - shows all commands  

Requirements:  
python - 3.7.4  
beautifulsoup4 - 4.9.3  
requests - 2.24.0  
