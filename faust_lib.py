from bs4 import BeautifulSoup
import requests
import csv
import time
import os
import re  # regex

# la liste des programmes (ajoutez nouveaux programmes dans bonne section)
PROGRAMMES_SCI_HUM = ['7756', '7758', '7640', '7796', '7733', '7647', '20173', '20183', '6961', '6161', '8917', '4975', '6389', '4524', '4014', '4033', '4402', '4347', '4116', '4026', '4350', '4047', '4269', '6155', '6850', '6013', '6432', '6510', '6047', '8866', '8855', '8853', '8384', '0931', '0791', '0173', '0745', '3268', '3269', '1653', '2254', '1963', '1964', '3542', '6155', '3431',
                      'F009', '3117', '3118', '1548', '1549', '1616', '2218', '1828', '1829', 'F012', '1846', '1847', '3003', '2112', '1944', '1995', '3246', '0251', '0933', '9112', '6998', '0547', 'F003', 'F017', 'F016', 'F015', 'F019', 'F010', 'F013', 'F007', '1730', '3448', '3662', '3433', '1958', '3091', '3191', '3291', '1550', '2350', '3127', '3678', '1595', '3486', '1506', '6514', 'F002', '6998']
PROGRAMMES_SPDR = ['4205', '7641', '8308', '3033', '1617', '1618', '1627', '1661', '1573', '0790', '4590',
                   '1556', '0783', '4181', '7060', '6660', '2350', '7760', '3555', '1691', '1997', '1998', '1996', '6120', '8912']
PROGRAMMES_ARTS = ['3031', '7601', '7603', '6507', '7605', '4087', '7324', '7325', '3574', '1893', '4717', '4289', '6511', '6512', '1801', '1802', '3566', '3997', '7322', '1604', '1704', '7779', '3273', '1901', '1902', '1903',
                   '1904', '3761', '6862', '8557', '3436', '3750', '2250', '6003', '8547', '7240', '7250', '4564', '6564', '8564', '3163', '3796', '3420', '4675', '3122', '7099', '7602', '6377', '7099', '7602', '6377', '3011', '4327', '3078', '3010']
PROGRAMMES_EDUC = ['1757', '1755', '7548', '7549', '6348', '0640', '3556', '3123', '0756', '1871', '1872', '1873', '1874', '1771', '1772', '1773', '1774', '3666', '4634', '4615', '1703', '0703', '9163', '7593', '6694', '0192', '1711', '1712', '1713', '1714', '1551', '1552',
                   '1553', '1554', '1555', '7176', '4851', '7177', '4857', '7088', '7489', '7414', '7415', '7951', '7652', '7954', '7653', '7657', '4550', '0630', '3264', '9518', '3170', '4031', '9584', '1891', '0680', '9211', '0813', '0814', '0896', '8097', '2350', '7690', '1596', '4046', '9211']
PROGRAMMES_COM = ['6525', '4165', '0124', 'F006', '4729', '0922', 'F004', '6007', '4098', '4214', '6960', '3479', '3279', '3179', '1879', '1779', '1679', '1979', '1634', '6503', '6504', '6505', '7433', '6637', '6638', '6639', '7434', '7234', '0479',
                  '6529', '0595', 'F022', '0513', '4672', '7641', '4727', '4655', '0758', '0823', 'F005', '4569', '9024', 'F025', '4153', '0754', 'F018', '4720', '0816', 'F020', '0873', 'F021', '9253', 'F024', '4621', '6021', '6022', '0389', '3011', '4650', '0485', '2350']
PROGRAMMES_SCIENCES = ['6542', '6543', '3056', '3814', '3440', '3805', '6713', '6532', '6533', '3411', '3554', '7363', '7359', '6002', '4780', '3005', '4626', '4201', '1564', '1622', '1822', '0822', '7442', '6920', '4024', '1517', '3281', '2282', '2283', '2284', '3121', '2222', '3560', '0433', '4702', '7316', '7416', '7616', '7616', '1919', '7328', '7326', '0804',
                       '1851', '6486', '3783', '3785', '1984', '1912', '1989', '1985', '1913', '1990', '3673', '8543', '7421', '7721', '1845', '4179', '4888', '4049', '2350', '3117', '3118', '3217', '1799', '1789', '4526', '1812', '4139', '1852', '1853', '3583', '3405', '1805', '3141', '7442', '6920', '7459', '2005', '6506', '6487', '0434', '3159', '0793', '0794', '6526', '0432']
PROGRAMMES_ESG = ['7669', '6559', '7111', '6560', '7112', '6561', '7113', '6562', '7320', '6563', '6538', '6539', '7668', '6558', '4122', '3451', '4480', '1892', '1970', '1972', '1971', '4423', '4723', '0799', '4518', '4517', '4627', '3026', '3027', '1628', '3203', '3111', '1940', '1835', '3045', '0635', '4092', '6571', '6572', '6573', '6574', '6575', '4614', '3424', '3524', '3747', '0770', '1918', '9118', '6990', '8856', '3855', '3854', '3895', '1896', '1739', '0739', '4607', '3842', '3580', '1894', '1895', '3139', '3195', '0785', '3186', '3183', '3185', '0623', '4525', '7002',
                  '7420', '4209', '0803', '4734', '0535', '7307', '8411', '7317', '8421', '7410', '8412', '7588', '7423', '7589', '6655', '6656', '6653', '6654', '6536', '6537', '6535', '4035', '4956', '7215', '7278', '4555', '1919', '3280', '9030', '4206', '1840', '0796', '8859', '4548', '4751', '4731', '1735', '0871', '0485', '2350', '7330', '4738', '1528', '1761', '1762', '1763', '1764', '1765', '1766', '1767', '1768', '1769', '2381', '1931', '1932', '1933', '1934', '1935', '1936', '1947', '1948', '1949', '1981', '4668', '1575', '1758', '1759', '0924', '8013', '8014', '8017', '8018', '8858']
PROGRAMMES = PROGRAMMES_SPDR + PROGRAMMES_SCI_HUM + PROGRAMMES_ARTS + \
    PROGRAMMES_EDUC + PROGRAMMES_COM + PROGRAMMES_ESG + PROGRAMMES_SCIENCES
TEMP_FILE_PREFIX = '/tmp/bs-cours-'
CSV_FILE_NAME = 'liste-cours.csv'

URL_LISTE_PROGRAMME = 'https://www-s.websysinfo.uqam.ca/regis/reg_horaire_pkg.liste_cours_horaire_html2'

# this is a POST, however it passes args as GETs as well might as well mimick
# the behaviour all the way
URL_DETAIL_COUR = 'https://www-s.websysinfo.uqam.ca/regis/reg_horaire_pkg.liste_cours_horaire2'

# if polite we delay requests not to alarm sysadmins
POLITE = 1

# ark, oui, ca prends toute ces crisses d'affaires là
# pour que le serveur réponde... y se protège surment
# du monde qui font des scripts comme ca qui font 10k
# requêtes, mais tabarnac, y'ont juste à nous donner
# les estis de listes de cours si y veulent pas qu'on
# aille les chercher nous même
cookies = {
    '_shib_uqamidp': '1',
    '.SAVCMSredirecturl': (
        "http://www.international.uqam.ca/WebResource.axd?d=JDLEMbQIwWjwmORkh2H2CtU0nf8NkTR89j"
        "l9Fu5UWSGgMfhoGOYijMWIE8lrT6FR6wxX_o7PBI9YGTpsloEdzbM51Ra_GeEey232ZI1EWDiPw6dGrnswO-I"
        "Qd6_ii1Ef_x8a6cqIF6cbfzY_pOS8_PX8ouLdfZYrLEmPO18AO4U-zOtI0&t=635288525880000000"
    ),
    'cycle1': 'Non',  # sti de beaux booleans ca, bravo UQAM
    'cycle23': 'Non',
    '_ga': 'GA1.2.775433387.1505390484',
    '__utma': '100371649.775433387.1505390484.1507203776.1508178842.9',
    'typeEtudiant': 'indefini',
}
headers = {
    'Referer': 'https://etudier.uqam.ca/horaire_cours/recherche.php',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
}


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


def get_classes(session, refresh=False):
    toute_les_cours = []
    for i, prog in enumerate(PROGRAMMES):
        print(i)
        if i >= 10:
            break
        filename = TEMP_FILE_PREFIX + prog
        # if the file is not already there
        if refresh or not os.path.isfile(filename):
            if POLITE:
                time.sleep(0.5)
            programme_content = get_program_content(session, prog)

            with open(filename, 'wb') as fd:
                fd.write(programme_content)

        with open(filename) as fd:
            soup = BeautifulSoup(fd.read(), 'html.parser')
            all_cours = soup.find_all('a')
            for j, cours in enumerate(all_cours):
                # cours are like: <a onclick="det_horaire2('SOM4500' , 'pc_niveau=D&amp;pn_trim_num=20191&amp;pc_format...
                if j != 0:
                    a = re.split(' ', cours.string)
                    toute_les_cours.append(a[0])

    sigles = sorted(set(toute_les_cours))
    classes = []

    for i, sigle in enumerate(sigles):
        if i >= 10:
            break
        filename = TEMP_FILE_PREFIX + 'cour-' + sigle
        if refresh or not os.path.isfile(filename):
            if POLITE:
                time.sleep(0.5)
            cour_content = get_cour_content(session, sigle)
            with open(filename, 'wb') as fd:
                fd.write(cour_content)

        with open(filename) as fd:
            soup = BeautifulSoup(fd, 'html.parser')
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


def save_as_csv(classes, filename):
    header = [
        'Groupe', 'Jour', 'Debut', 'Fin', 'Salle', 'Prof', 'Type', 'Presentiel', 'Dates', 'Sigle', 'Titre', 'Note']
    fieldnames = [
        'groupe', 'jour', 'debut', 'fin', 'salle', 'prof', 'type', 'presentiel', 'dates', 'sigle', 'titre', 'note']

    with open(filename, 'w', encoding='UTF-8') as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(classes)
    print("Le fichier CSV a ete ecrit: " + filename)


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


def get_schedule(session, output=CSV_FILE_NAME, refresh=False):
    classes = get_classes(session, refresh)
    save_as_csv(classes, output)
