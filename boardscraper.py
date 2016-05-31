import dryscrape, requests, os
from bs4 import BeautifulSoup


searchVar2 = [['seacats', 'rokkenjima', 'umineko', 'erika', 'beatrice', 'battler', 'kinzo', 'ryukishi', 'ryukishi07', 'r07'],['Kancolle', 'Kantai', 'Kantai-Collection']]


print(
'''
What do you want to search for:
\t\t[1]:\t Umineko
\t\t[2]:\t Kancolle
'''
)
choice = input()
if choice == '1':
    searchVar2 = searchVar2[0]
elif choice == '2':
    searchVar2 = searchVar2[1]
else:
    print('Please use 1 or 2')


print('Where do you want to save the images')
folder = input()
os.makedirs(folder, exist_ok=True)    

boardUrl = 'http://boards.4chan.org/jp/catalog'
sess = dryscrape.Session()
sess.set_attribute('auto_load_images', False)
sess.visit(boardUrl)
catalogResponse = sess.body()
soup = BeautifulSoup(catalogResponse, "lxml")
csssearch = soup.select('div a')


if csssearch == []:
    print('Could not find any div "a" elements in the catalog')
else:
    for i in csssearch:
        for threadName in searchVar2:
            hrefstring = str(i.get('href'))
            if threadName.lower() in hrefstring.lower():
                print('Thread found.')
                threadUrl = 'http:' + hrefstring
                sess = dryscrape.Session()
                sess.visit(threadUrl)
                threadResponse = sess.body()
                soup = BeautifulSoup(threadResponse, "lxml")

                #find the image

                threadElem = soup.select('div a')
                if threadElem == []:
                    print('Could not find any div "a" elements in the thread')
                else:
                    for i in threadElem:
                        if i.get('class') == ['fileThumb']:
                            imageUrl = i.get('href')
                            imageUrl = 'http:'+ imageUrl
                            #download the image
                            imageName = os.path.basename(imageUrl)
                            if os.path.exists(folder + '/' + imageName) == True:
                                print(imageName + ' already exists in ' + folder)
                            else:
                                print('Downloading image %s...' % (imageUrl))
                                res = requests.get(imageUrl)
                                res.raise_for_status()
                                imageFile = open(os.path.join(folder, imageName), 'wb')
                                for chunk in res.iter_content(100000):
                                    imageFile.write(chunk)
                                imageFile.close()

print('Done!')
