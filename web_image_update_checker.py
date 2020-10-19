from bs4 import BeautifulSoup
import requests
import os


def create_or_read_file(file_path):
    with open(file_path, 'a'): pass
    with open(file_path, 'r') as f:
        entries = f.readlines()
    return entries


def find_image_name(page_url, image_index):
    page = requests.get(page_url)
    
    if page:
        soup = BeautifulSoup(page.content, 'html.parser')
        image_tags = soup.find_all('img')
        image_index = int(image_index)

        if len(image_tags) > image_index:
            img_tag = image_tags[image_index]
            image_name = img_tag['src'].split('/')[-1]
            return image_name
        else:
            print('The layout of the page', page_url, 'has changed')
            return ''
    
    else:
        print('An error', page.status_code, 'occurred while loading the page', page_url)
        return ''


def find_image_index(page_url, image_name):
    page = requests.get(page_url)
    
    if page:
        soup = BeautifulSoup(page.content, 'html.parser')
        image_tags = soup.find_all('img')

        for i, img_tag in enumerate(image_tags):
            new_image_name = img_tag['src'].split('/')[-1]

            if new_image_name == image_name:
                return i

        print('Image not found on the page', page_url)
        return -1
    
    else:
        print('An error', page.status_code, 'occurred while loading the page', page_url)
        return -1


def find_and_change_entry(searched_page_url, new_entry, entries, file_path, found_message, not_found_message):
    entry_found = False
    
    for i, entry in enumerate(entries):
        page_url = entry.split()[0]

        if page_url == searched_page_url:
            entries[i] = new_entry

            with open(file_path, 'w') as f:
                f.writelines(entries)

            entry_found = True
            print(found_message)
            break

    if not entry_found:
        
        if len(new_entry) > 0:

            with open(file_path, 'a') as f:
                f.writelines(new_entry)

        print(not_found_message)


def main():
    command = input('\nType your command, type "help" for help> ').lower().split(maxsplit=3)
    
    if '__file__' in globals():
        basepath = os.path.dirname(os.path.realpath(__file__))
    else: basepath = os.getcwd()
            
    file_path = os.path.join(basepath, 'web_pages_and_images.txt')
    
    if len(command) == 1 and command[0] in ('check', 'c'):
        entries = create_or_read_file(file_path)
        print('Updated web pages:')
        
        for entry in entries:
            page_url, image_name, image_index = entry.split()
            new_image_name = find_image_name(page_url, image_index)
            
            if new_image_name == '':
                continue
            elif new_image_name != image_name:
                print(page_url)
                
    elif len(command) == 1 and command[0] in ('update', 'u'):
        entries = create_or_read_file(file_path)
        print('Updated entries:')
        
        for i, entry in enumerate(entries):
            page_url, image_name, image_index = entry.split()
            new_image_name = find_image_name(page_url, image_index)
            
            if new_image_name == '':
                continue
            elif new_image_name != image_name:
                entries[i] = '  '.join([page_url, new_image_name, image_index]) + '\n'
                print(entries[i], end='')
                
        with open(file_path, 'w') as f:
            f.writelines(entries)

    elif len(command) == 3 and command[0] in ('add', 'a'):
        _, new_page_url, new_image_url = command
        
        if (new_page_url[:8] == 'https://' or new_page_url[:7] == 'http://') and (new_image_url[:8] == 'https://' or new_image_url[:7] == 'http://'):
            entries = create_or_read_file(file_path)
            new_image_name = new_image_url.split('/')[-1]
            new_image_index = find_image_index(new_page_url, new_image_name)
            
            if new_image_index == -1:
                pass
            else:
                new_entry = '  '.join([new_page_url, new_image_name, str(new_image_index)]) + '\n'
                find_and_change_entry(new_page_url, new_entry, entries, file_path, 'Entry changed', 'Entry added')
        else:
            print('Links must contain "https://" or "http://" part at the beginning')
    
    elif len(command) == 2 and command[0] in ('delete', 'd'):
        _, deleted_page_url = command
        
        if (deleted_page_url[:8] == 'https://' or deleted_page_url[:7] == 'http://'):
            entries = create_or_read_file(file_path)
            find_and_change_entry(deleted_page_url, '', entries, file_path, 'Entry deleted', 'Entry not found')
        else:
            print('Links must contain "https://" or "http://" part at the beginning')
    
    elif len(command) == 1 and command[0] in ('list', 'l'):
        entries = create_or_read_file(file_path)
        print('All entries:')
        
        for entry in entries:
            print(entry, end='')
    
    elif len(command) == 1 and command[0] in ('exit', 'e'):
        print('Program stopped')
        raise SystemExit
    
    elif len(command) == 1 and command[0] in ('help', 'h'):
        print('All commands:',
              '\n(c)heck  - checks web pages for image changes',
              '\n(u)pdate - updates changed images in the text file',
              '\n(a)dd    - changes existing entry or adds a new entry, type like this:  add page_url image_url',
              '\n(d)elete - deletes existing entry, type like this:  delete page_url',
              '\n(l)ist   - lists all entries like this:  page_url image_name image_index',
              '\n(e)xit   - stops the program',
              '\n(h)elp   - shows all commands')
    
    else: print('Wrong syntax')
        
        
if __name__ == '__main__':
    while True:
        main()
