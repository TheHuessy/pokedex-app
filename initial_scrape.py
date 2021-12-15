import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_egg_moves(tables):
    headers = [header.text for header in [tables[25].find_all("th") for x in range(1,len(tables[25].find_all("tr"))) if tables[25].find_all("tr")[x].find_all("th")][0]]
    headers[-1] = 'Desc.'

    egg_mv_rows = [tables[25].find_all("tr")[x].find_all("td") for x in range(1,len(tables[25].find_all("tr"))) if tables[25].find_all("tr")[x].find_all("td")]

    out_rows = []

    for idx, val in enumerate(egg_mv_rows):
        ## Every other row is the description of the attack (all odd indexes)
        if idx % 2 == 0:
            vals = [x.text for x in val]

            ## have to sort of go back and grab other values that are nested
            img_vals = [x.find_all("img") for x in val if x.find_all("img")]
            atk_type = img_vals[0][0].attrs['src'].split("/")[-1].split(".")[0]
            atk_cat = img_vals[1][0].attrs['src'].split("/")[-1].split(".")[0]
            
            vals[0] = vals[0].replace("SWSH Only", "").replace("BDSP Only", "") #Should really add another field for 'game exclusive move' or something and put BDSP/SWSH/etc. in as value for later db building
            vals[1] = atk_type
            vals[2] = atk_cat
            vals[-1] = [x.text for x in egg_mv_rows[idx+1]][0]

            out_rows += [vals]
    out_df = pd.DataFrame(out_rows, columns=headers)

    return(out_df)


def get_level_up_attacks(tables):
    atk_tbl_header_row = [tables[20].find_all("tr")[x].find_all("th") for x in range(1,len(tables[20].find_all("tr"))) if tables[20].find_all("tr")[x].find_all("th")][0]
    headers = [x.text for x in atk_tbl_header_row]
    headers += ['Desc.']

    atk_tbl_rows = [tables[20].find_all("tr")[x].find_all("td") for x in range(1,len(tables[20].find_all("tr"))) if tables[20].find_all("tr")[x].find_all("td")]

    out_rows = []

    for idx, val in enumerate(atk_tbl_rows):
        ## Every other row is the description of the attack (all odd indexes)
        if idx % 2 == 0:
            vals = [x.text for x in val]
            vals += [x.text for x in atk_tbl_rows[idx+1]]

            out_rows += [vals]
    out_df = pd.DataFrame(out_rows, columns=headers)

    return(out_df)





base_url = "https://serebii.net/pokedex-swsh/bulbasaur/"

req = requests.get(base_url)

page_html = req.text

soup = BeautifulSoup(page_html, "html.parser")

tables = soup.find_all("table")

## DF of all attacks learned 
    #get_level_up_attacks(tables)
## DF of all egg moves
    #print(get_egg_moves(tables))
