import requests
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
import gspread


sheet = None  


def get_description(url):

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers)
    soup=BeautifulSoup(response.text,'lxml')
    description=soup.find('div',{'id':'marketing-remarks-scroll'}).find('p')
    if description:
      description_text=description.text.replace('Public Remarks: ','')
    else:
        description_text=None
    print(description_text)
    
    return description_text
# find_all('span')

def get_urls():
    global sheet

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('cred/credentials.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key('15vZVl3QDmX0C-bpfr594Q_76rTv2UpXch8fHtDi8iyo')
    worksheet=sheet.worksheet("Input")
    sheet.worksheet("Output").clear()
    # return worksheet.col_values(1)
    return worksheet.col_values(21)



def get_data_from_claude(description):



    return description

def save_data(url,data_from_ai):
    global sheet
    sheet.worksheet("Output").append_row([url,data_from_ai])
    

if __name__ == "__main__":
    urls=get_urls()[1:]
    for url in urls:
        print('start with : '+url)
        description=get_description(url)
        data_from_ai=get_data_from_claude(description)
        save_data(url,data_from_ai)
        