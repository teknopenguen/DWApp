from bs4 import BeautifulSoup
from requests import get


class DWParser:

    def __init__(self, link):
        self.link = link
        self.content = self.get_html_content()
        self.soup = BeautifulSoup(self.content, "html.parser")
        self.distrolist = self.get_distro_list()

    def get_html_content(self, link=''):
            
        link = self.link if link == '' else link
        r = get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                                             '(KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'})
        content = r.text
        return content

    def get_distro_list(self, content='', soup=''):

        content = self.content if content == '' else content
        soup = self.soup if soup == '' else BeautifulSoup(content, "html.parser")
        select_menu_content = soup.find('select')
        select_menu_list = select_menu_content.find_all('option')

        def create_generator():
            for i in select_menu_list:
                if i.get('value') != '':
                    inner_data = {'link': i.get('value'), 'name': i.text}
                    yield inner_data

        return create_generator()

    def create_last_news_data_list(self, content='', soup=''):

        tags = ['NewsHeadline', 'NewsLogo', 'NewsText', 'NewsDate']
        content = self.content if content == '' else content
        soup = self.soup if soup == '' else BeautifulSoup(content, "html.parser")
        items = soup.find_all('td', attrs={'class': 'News1'})

        def create_generator():
            for i in items[1:]:
                inner_data = {}
                for j in tags:
                    if j == 'NewsLogo':
                        inner_data[j] =  self.link + i.parent.find(attrs={'class': j}).img.get('src')
                        inner_data['Link'] = i.parent.find(attrs={'class': j}).a.get('href')
                    else:
                        inner_data[j] = i.parent.find(attrs={'class': j}).text

                yield inner_data

        return create_generator()

    def create_popularity_data_list(self, content='', soup=''):

        tags = ['phr1', 'phr2', 'phr3', 'img']
        content = self.content if content == '' else content
        soup = self.soup if soup == '' else BeautifulSoup(content, "html.parser")
        items_soup = soup.find('table', attrs={'class': 'News', 'style': 'direction: ltr'})
        items = items_soup.find_all('tr')[3:]

        def create_generator():
            for i in items:
                inner_data = {}
                for j in tags:
                    if j == 'img':
                        inner_data[j] = self.link + i.find('img').get('src')
                    elif j == 'phr2':
                        inner_data[j] = i.find(attrs={'class': j}).text
                        inner_data[j+'link'] = i.find('a').get('href').split('?')[0]
                    else:
                        inner_data[j] = i.find(attrs={'class': j}).text
                yield inner_data
        return create_generator()
    
    def create_distro_page_data_list(self, distro):

        if 'weekly.php' not in distro:
            link = 'https://www.distrowatch.com/table.php?distribution=' + distro
            content = self.get_html_content(link)
            soup = BeautifulSoup(content, "html.parser")
            innerContent = soup.find('td',attrs={'class':'TablesTitle'})
            img = innerContent.find_all('img')
            img_gen = (self.link + i.get('src') for i in img)

            def create_generator():

                distro_info = innerContent.find('li')
                for i in distro_info.find_all('b'):
                    label = i.text
                    for j in i.find_next_siblings():
                        if label == 'Based on:' and j.text.strip() == '':
                            label += ' Independent'
                            yield label
                        if j.name == 'a' or j.name == 'font':
                            label += ' ' + j.text
                            yield label

            return img_gen, create_generator()
        else:
            return []

if __name__ == '__main__':

    dwparser = DWParser('https://www.distrowatch.com/')
    data = dwparser.create_distro_page_data_list('mint')
    print(list(data[1]))