from bs4 import BeautifulSoup
from variables import URL_LISTE_PROGRAMME, URL_DETAIL_COUR, PROGRAMMES, cookies, headers
import requests, csv, time, re

def get_program_content(session, code, i):
    print("Downloading programme " + code + " " + str(i) + "/" + str(len(PROGRAMMES)))

    post_items = {
        'pn_trim_num': session,
        'pc_type_offre': 'P',
        'pc_code_prog': code,
        'pc_titre': '',
        'pc_groupe': '',
        'pc_dept': '',
        'pa_no_jour': '',
        'pa_no_creneau': '',
        'pa_campus': '',
        'pa_cycle': '',
        'pa_type_ens': '',
        'pa_type_horaire': '',
        'pa_type_cours': '',
        'pc_min_place': '',
        'pn_max_cours': 500,
        'pc_format': 'HTML_AVEC_CART_HEADER_BACK_BUTTON',
    }
    
    resp = requests.post(URL_LISTE_PROGRAMME, data=post_items, cookies=cookies, headers=headers, stream=True)
    return resp.content.decode('latin-1').encode('utf-8')


def get_cours_content(session, sigle, i, total):
    print("Downloading cours " + sigle + " " + str(i) + "/" + str(total))
    
    post_items = {
        'pn_trim_num': session,
        'pc_niveau': 'D',
        'pc_format': 'HTML_AVEC_CART_HEADER_BACK_BUTTON_APPEND_COMPRIME',
        'pc_sigle': sigle,
        'pc_code_prog': '',
    }
    
    resp = requests.post(URL_DETAIL_COUR, data=post_items, cookies=cookies, headers=headers, stream=True)
    return resp.content.decode('latin-1').encode('utf-8')


def get_classes_from_html(session, polite, programme):
    tous_les_cours = []
    programmes = PROGRAMMES
    if programme != "":
        programmes = [programme]
    for i, prog in enumerate(programmes):
        # TEST
        # if i >= 1:
        #     break

        if polite:
            time.sleep(0.5)

        soup = BeautifulSoup(get_program_content(session, prog, i+1), 'html.parser')
        all_cours = soup.find_all('a')
        
        for j, cours in enumerate(all_cours):
            if j != 0:
                # cours =  <a onclick="det_horaire2('SOM4500' , 'pc_niveau=D&amp;pn_trim_num=20191&amp;pc_format...
                a = re.split(' ', cours.string)
                tous_les_cours.append(a[0])
    
    return sorted(set(tous_les_cours))


def get_classes(session, polite, programme):
    sigles = get_classes_from_html(session, polite, programme)
    classes = []

    for i, sigle in enumerate(sigles):
        # TEST
        # if i >= 1:
        #     break

        if polite:
            time.sleep(0.5)

        page_du_cours = BeautifulSoup(get_cours_content(session, sigle, i+1, len(sigles)), 'html.parser')
        
        titre = page_du_cours.find('h2').text.split(' ', 2)[2]
        rows = page_du_cours.find_all('tr')

        prof = ""
        presentiel = ""
        note = ""
        dates = ""
        groupes_info_incomplet = []
        last_group_num = ""
        for j, row in enumerate(rows):
            if j == 0:  # headers row
                continue

            columns = row.find_all('td')
            if len(columns) == 6:
                groupe_info = get_group_info(columns, last_group_num)
                last_group_num = groupe_info['groupe']
                groupes_info_incomplet.append(groupe_info)
            else:
                if "Enseignants" in row.text or "Enseignant" in row.text:
                    prof = row.text.split(':')[1]
                elif "Mode d'enseignement en ligne" in row.text:
                    presentiel = row.text.split(':')[1]
                elif "Remarque" in row.text:
                    note += " " + row.text.split(':')[1]
                elif "Periode" in row.text:
                    dates = row.text.split(':')[1]
                # else:
                    # note += " " + row.text

        for groupe in groupes_info_incomplet:
            groupe['prof'] = prof
            groupe['presentiel'] = presentiel
            groupe['note'] = note
            groupe['dates'] = dates
            groupe['titre'] = titre
            groupe['sigle'] = sigle
            classes.append(groupe)

    return classes


def save_as_csv(classes):
    fieldnames = ['groupe', 'jour', 'debut', 'fin', 'salle', 'prof', 'type', 'presentiel', 'dates', 'sigle', 'titre', 'note']
    with open('liste-cours.csv', 'w', encoding='UTF-8') as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(classes)
    print("Le fichier CSV a ete ecrit: " + '"./liste-cours.csv"')


def get_group_info(columns, last_group=""):
    # Sometime there's multiple class for the same group, but the group number isn't repeated, it's empty instead
    if columns[0].text.strip():
        groupe = columns[0].text.strip()
    else:
        groupe = last_group
    return {
        'groupe': groupe,
        'jour': columns[1].text.strip(),
        'debut': columns[2].text,
        'fin': columns[3].text,
        'salle': columns[4].text.strip(),
        'type': columns[5].text,
    }


def get_schedule(session, polite=False, programme="7416"):
    classes = get_classes(session, polite, programme)
    save_as_csv(classes)
