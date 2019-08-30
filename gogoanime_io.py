import requests,time,os,math
from tqdm import tqdm
from IPython.display import Image, display  
from bs4 import BeautifulSoup
print("\033[J")

def newanime(url="https://www9.gogoanime.io/new-season.html"):
    link=[i.find("a").get("href") for i in BeautifulSoup(requests.get(url).text,features="lxml").select('ul.pagination-list > li')]
    new_release=[i.get("title") for i in link for i in BeautifulSoup(requests.get(url+i).text,features="lxml").select('div.last_episodes > ul > li > p > a')]
    printdata(new_release,"New Release")   
def search():
    print("Search For Anime ____")
    word=input("Enter Anime to Search :  ")
    if len(word) <=2:
        raise Exception("Word Entered lenght should be greater then 2")
    soup=BeautifulSoup(requests.get("https://www9.gogoanime.io//search.html?keyword="+word).text,features="lxml")
    search_result=[i.get("title") for i in soup.select('div.last_episodes > ul > li > p > a')]
    if (len(search_result)==0):
        raise Exception("No Result found // Try differnt keywords for better result")
    else:
        printdata(search_result,"Search Result",False)
    search_list=input("Enter Name Anime / Number to Get info :  ").lower().strip()
    search_found=[]
    if search_list.isdigit():
        if int(search_list)==0:
            raise Exception("0 is not an option")
        href=soup.select('div.last_episodes > ul > li > p > a')[int(search_list)-1].get("href") 
        search_url="https://www9.gogoanime.io"+href
        return search_url
    else:
        search_found=[i for i in search_result if search_list in i.lower()  ]
    if len(search_found)==0:
        raise Exception("Something went wrong //Try again")
    if len(search_found)==1:
        search_url="https://www9.gogoanime.io"+soup.select('div.last_episodes > ul > li > p > a')[0].get("href")
        return search_url
    else:
        printdata(search_found, "Be Specfic from",delete=False)
        Number=int(input("Enter Number :  "))-1
        if Number.isalpha():
            raise Exception("Enter integer value")
        if len(search_found)<Number+1 or Number+1 < 1 :
            raise Exception("Out of range Number entered")
        search_url="https://www9.gogoanime.io"+soup.select('div.last_episodes > ul > li > p > a')[search_result.index(search_found[Number])].get("href")
        if len(search_url)==0 :
            raise Exception("Wrong Keyword entered")
        return search_url

def details(url):
    soup=BeautifulSoup(requests.get(url).text,features="lxml")
    img=soup.select('div.anime_info_body_bg > img')[0].get('src')
    img_data = requests.get(img).content
    with open(url.split("/")[-1]+'.jpg', 'wb') as handler:
        handler.write(img_data)
    display(Image(filename=url.split("/")[-1]+'.jpg'))
    os.remove(url.split("/")[-1]+'.jpg')
    title=soup.select('div.anime_info_body_bg > h1')[0].string
    print(f"Anime Name : {title}")
    plot=soup.select('div.anime_info_body_bg > p')[2].getText()
    print(plot)
    Genre=soup.select('div.anime_info_body_bg > p')[3].getText()
    print(" ".join(Genre.split("\n")))
    T_download=int(soup.select('ul#episode_page > li > a')[0].get("ep_end"))
    print(f"Total Episode : {T_download}")
    download_link=["https://www9.gogoanime.io/"+url.split("/")[-1]+"-episode-"+str(i+1) for i in range(T_download) ]
    return download_link
def episode(tup):
    print(f"link:  {tup}")
def downloading(url,name):
    print("//  Downloading starting")
    soup=BeautifulSoup(requests.get(url).text,features="lxml")
    link=soup.select("span.btndownload")[0].parent.get('href')
    soup=BeautifulSoup(requests.get(link).text,features="lxml")
    link=soup.select("div.dowload")[0].find('a').get("href")
    r = requests.get(link, stream=True)
    total_size = int(r.headers.get('content-length', 0)); 
    block_size = 1024
    wrote = 0 
    with open(name+'.mp4', 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")  
    print("//  Downloading Ended")   
def printdata(data, phrase,delete=True):
     no=1
     print(f"{phrase} ___")
     for i in data:
         print(f"    {no}.  {i}")
         time.sleep(.2)
         no=no+1
         if no%10==0 and delete==True:
             input("// Press Any Key _____ ")
             print("\033[J")
             print(f"{phrase} ___")
def ongoing(url="https://www9.gogoanime.io/anime-list.html"):
    soup=BeautifulSoup(requests.get(url).text,features="lxml")
    list_search= [ i.get("href")  for i in soup.select('div.list_search > ul > li > a ')][1:]
    words=list("0ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    letter="/anime-list-"+input("Enter Starting Char Anime of ongoing series : ").upper() 
    if len(letter)!=13:
        raise Exception(" // letter lenght should be one _____")
    if letter.split("-")[-1] not in words:
        raise Exception(" // Invalid Char Entered PS:Try Again _____")
    index=int("".join(map(str,[list_search.index(i) for i in list_search if letter==i])))
    listname("https://www9.gogoanime.io/"+list_search[index],letter.split("-")[-1])
def listname(url,l):
    soup=BeautifulSoup(requests.get(url).text,features="lxml")
    name= [ i.string for i in soup.select('div.anime_list_body > ul > li > a ')]
    printdata(name,l+" Letter ongoing Series",False)
def main():
    print("Welcome to https://www9.gogoanime.io")   
    print("GoGoAnime.io is the best site where you can watch online anime for free as it is a free site")
    print("Access https://www9.gogoanime.io with help of python and webscrapping".title())
    Options=["Newly Released Anime","Anime's Picture, Title, synopsis, episode list","Episode's urls","List of ongoing series","Find anime by keyword"]
    printdata(Options,"Choose option from following list : ",False )
    try:
        Option=input("Enter Option : ")
        if Option.isdigit():
            if int(Option) <=5 and int(Option) >=1: 
                if int(Option)==1:
                    newanime()
                if int(Option)==2:
                    details(search())
                if int(Option)==3:
                    tup=details(search())
                    epi=int(input("Enter Episode Number: "))
                    if epi<1 or epi >len(tup):
                        raise Exception("Enter Correct Episode Number")                
                    episode(tup[epi-1])
                    ch=input("Want to download [Yes:No]:  ").lower()
                    if ch=="" or ch==None:
                        raise Exception("No input provided")
                    if ch=="Yes" or ch=="y":
                        downloading(tup[epi-1],tup[epi-1].split("/")[-1])
                if int(Option)==4:
                    ongoing()
                if int(Option)==5:
                    search()
            else:
                raise Exception("Out of range")
        else:
            raise Exception("Enter integer value")
    except Exception as h:
        print("Error: // "+str(h).title())   
    try:
        ch=input("Want to Run Program again? [Yes:No]:  ").lower()
        if ch=="" or ch==None:
            raise Exception("No input provided")
        if ch=="Yes" or ch=="y":
            main()
        else:
            print("Have a nice day :-)")
    except Exception as h:
        print("Error: // "+str(h).title())  
if __name__=="__main__":
    main()
