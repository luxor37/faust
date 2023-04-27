from bs4 import BeautifulSoup
from variables import URL_LISTE_PROGRAMME, URL_DETAIL_COUR, PROGRAMMES, CSV_FILE_NAME, cookies, headers
import requests, csv, time, re

def get_program_content(session, code):
    print("Downloading programme" + code)

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
    resp = requests.post(URL_LISTE_PROGRAMME, data=post_items,
                         cookies=cookies, headers=headers, stream=True)
    return resp.content.decode('latin-1').encode('utf-8')


def get_cour_content(session, sigle):
    print("Downloading cours" + sigle)
    post_items = {
        'pn_trim_num': session,
        'pc_niveau': 'D',
        'pc_format': 'HTML_AVEC_CART_HEADER_BACK_BUTTON_APPEND_COMPRIME',
        'pc_sigle': sigle,
        'pc_code_prog': '',
    }
    resp = requests.post(URL_DETAIL_COUR, data=post_items,
                         cookies=cookies, headers=headers, stream=True)
    return resp.content.decode('latin-1').encode('utf-8')


def get_classes_from_html(session, polite=True):
    tous_les_cours = []
    for i, prog in enumerate(PROGRAMMES):
        if i >= 10:
            break

        if polite:
            time.sleep(0.5)

        programme_content = get_program_content(session, prog)

        soup = BeautifulSoup(programme_content, 'html.parser')
        all_cours = soup.find_all('a')
        
        for j, cours in enumerate(all_cours):
            # cours are like: <a onclick="det_horaire2('SOM4500' , 'pc_niveau=D&amp;pn_trim_num=20191&amp;pc_format...
            if j != 0:
                a = re.split(' ', cours.string)
                tous_les_cours.append(a[0])
    
    return sorted(set(tous_les_cours))


def get_classes(session, polite=True, refresh=False):
    sigles = get_classes_from_html(session)
    classes = []

    for i, sigle in enumerate(sigles):
        if i >= 10:
            break

        if polite:
            time.sleep(0.5)
        cour_content = get_cour_content(session, sigle)
        soup = BeautifulSoup(cour_content, 'html.parser')
        titre = soup.find_all('h2')[0].text.split(' ', 2)[2]
        bloc_groupe = soup.find_all('table')
        # pour chaque groupe y'a une table
        # avec les heures du cours, qui ont probablement
        # plusieurs lignes
        for tr_groupe in bloc_groupe:
            infos = tr_groupe.find_all('td')
            groupe = re.split(' |\n ', infos[0].text)

            tr_blocs = tr_groupe.find_all('tr')
            prof = ""
            presentiel = ""
            note = ""
            dates = ""
            tmp_groups = []
            last_group = ""
            for j, tr_bloc in enumerate(tr_blocs):
                if j == 0:  # headers row
                    continue

                if len(tr_bloc.find_all('td')) == 6:
                    group_info = get_group_info(tr_bloc, last_group)
                    last_group = group_info['groupe']
                    tmp_groups.append(group_info)
                else:
                    if "Enseignants" in tr_bloc.text or "Enseignant" in tr_bloc.text:
                        prof = tr_bloc.text.split(':')[1]
                    elif "Mode d'enseignement en ligne" in tr_bloc.text:
                        presentiel = tr_bloc.text.split(':')[1]
                    elif "Remarque" in tr_bloc.text:
                        note += " " + tr_bloc.text.split(':')[1]
                    elif "Periode" in tr_bloc.text:
                        dates = tr_bloc.text.split(':')[1]
                    else:
                        note += " " + tr_bloc.text

            for group in tmp_groups:
                group['groupe'] = groupe[0]
                group['prof'] = prof
                group['presentiel'] = presentiel
                group['note'] = note
                group['dates'] = dates
                group['titre'] = titre
                group['sigle'] = sigle
                classes.append(group)

    return classes


def save_as_csv(classes):
    header = [
        'Groupe', 'Jour', 'Debut', 'Fin', 'Salle', 'Prof', 'Type', 'Presentiel', 'Dates', 'Sigle', 'Titre', 'Note']
    fieldnames = [
        'groupe', 'jour', 'debut', 'fin', 'salle', 'prof', 'type', 'presentiel', 'dates', 'sigle', 'titre', 'note']

    with open('liste-cours.csv', 'w', encoding='UTF-8') as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(classes)
    print("Le fichier CSV a ete ecrit: " + 'liste-cours.csv')


def get_group_info(tr_bloc, last_group=""):
    tds = tr_bloc.find_all('td')

    # Sometime there's multiple class for the same group, but the group number isn't repeated, it's empty instead
    if tds[0].text.strip():
        groupe = tds[0].text.strip()[0]
    else:
        groupe = last_group
    return {
        'groupe': groupe,
        'jour': tds[1].text.strip(),
        'debut': tds[2].text,
        'fin': tds[3].text,
        'salle': tds[4].text.strip(),
        'type': tds[5].text,
    }


def get_schedule(session, polite=True, refresh=False):
    classes = get_classes(session, polite, refresh)
    save_as_csv(classes)
