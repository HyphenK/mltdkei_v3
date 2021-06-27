# Python Module #
import sqlite3
from urllib.request import urlopen
from re import findall
from bs4 import BeautifulSoup
from time import sleep

version = "[3.1] 21/06/29"
conn1 = sqlite3.connect('mltdkei_idoldata_kr.sqlite')
cur1 = conn1.cursor()
conn2 = sqlite3.connect('mltdkei_songdata_kr.sqlite')
cur2 = conn2.cursor()
matsuri_url = "https://mltd.matsurihi.me/ko/cards/"
matsuri_storage = "https://storage.matsurihi.me/mltd_ko/icon_l/"
github_url = "https://raw.githubusercontent.com/HyphenK/mltdkei_v3/main_kr/"
namedict = dict()

def version_check():
    return version

def update_centerstorage():
    web_centerid_list = list()
    centerid_page = github_url + "centerinfo"
    centerid_page_data = urlopen(centerid_page).read().decode('utf-8').split('\n')
    for line in centerid_page_data:
        if len(line) == 0: continue
        web_centerid_list.append(line)
    web_centerid_count = int(len(web_centerid_list))

    try: centerid_count = int(cur1.execute('select count(centerid) from CenterStorage').fetchone()[0])
    except: centerid_count = 0

    if centerid_count == web_centerid_count:
        return False
    else:
        cur1.executescript('''
        drop table if exists CenterStorage;
        create table if not exists CenterStorage (centerid integer, center text);
        ''')
        for line in web_centerid_list:
            line = line.split('	')
            cur1.execute(f'insert into CenterStorage (centerid, center) values {line[0], line[1]}')
        conn1.commit()
        return True

def update_typestorage():
    web_idolinfo_list = list()
    idolinfo_page = github_url + "idolinfo"
    idolinfo_page_data = urlopen(idolinfo_page).read().decode('utf-8').split("\n")
    for line in idolinfo_page_data:
        if len(line) == 0: continue
        web_idolinfo_list.append(line)
    web_idolinfo_count = int(len(web_idolinfo_list))

    try: idolinfo_count = int(cur1.execute('select count(name) from TypeStorage').fetchone()[0])
    except: idolinfo_count = 0

    if idolinfo_count == web_idolinfo_count:
        return False
    else:
        cur1.executescript('''
        drop table if exists TypeStorage;
        create table if not exists TypeStorage (name text, type integer);
        ''')
        for line in idolinfo_page_data:
            line = line.split(',')
            name = line[0]
            if name == '': break
            type = line[1]
            cur1.execute(f'insert into TypeStorage (name, type) values {name, type}')
        conn1.commit()
        return True

def load_idolinfo(i):
    webdata = urlopen(matsuri_url+str(i))
    soup1 = BeautifulSoup(webdata, 'html.parser')
    name = soup1.find("h1").get_text()
    data = soup1.find_all("div", class_="col")
    k, r_raw = 0, []
    while 1:
        k = k - 1
        card = data[k].find_all("div", class_="col-12")
        if len(card) != 0: break
    for j in card:
        r_raw.append(j.get_text())
    rare = r_raw[0].split(' ')[-1]
    maxrank = r_raw[2].split(' ')[-1]
    vocal = ' '.join(r_raw[4].split(' ')[1:])
    dance = ' '.join(r_raw[5].split(' ')[1:])
    visual = ' '.join(r_raw[6].split(' ')[1:])
    total = ' '.join(r_raw[7].split(' ')[2:])
    center = ' '.join(r_raw[9].split(' ')[4:])
    if rare == "N+":
        skill = "스킬 없음"
        maxlevel = 0
        percent = 0
    else:
        skill = ' '.join(r_raw[12].split(' ')[3:])
        maxlevel = r_raw[11].split(' ')[-1]
        percent = findall('[0-9]+', skill)[1]
    if int(maxrank) == 5 and int(maxlevel) != 12:
        maxlevel = '12'
        percent = str(int(percent)+10)
    photocode = str(soup1.find('div', class_="card-img-b")).split('/')[5][0:10] + "_1.png"
    r = [rare, maxrank, vocal, dance, visual, total, center, skill, maxlevel, percent, photocode]
    global namedict
    namedict[int(i)] = name
    return name, r

def update_idoldata(cls_name):
    main_page_data = urlopen(matsuri_url).read().decode('utf-8')
    extract_end = findall("""<a class="card-select" href="/ko/cards/([0-9]+?)">""", main_page_data)
    extract_end.sort(reverse=True)
    extract_end = int(extract_end[0]) + 1

    try:
        extract_start = int(cur1.execute('select idnumber from IdolDB order by idnumber asc').fetchall()[-4][0]) + 1
        db_exist = True
    except:
        extract_start = 1
        db_exist = False

    try:
        infofile = open('mltdkei_info_kr.txt', 'r', encoding='utf-8')
        infodata = infofile.read().split('\n')[:-1]
        infofile.close()
        txt_last = int(infodata[-1].split(',')[0]) + 1
    except:
        infodata = []
        txt_last = 1

    # print(extract_start, extract_end, txt_last)

    if db_exist == True and txt_last == extract_end and extract_start == extract_end:
        cls_name.config_info("Checking Main DB and mltdkei_info_kr.txt Updates... No Updates Found.")
        return

    if db_exist == False:
        cur1.executescript('''
        drop table if exists IdolDB;
        create table if not exists IdolDB (
            idnumber integer unique, rare text, type integer,
            name text unique, maxrank integer, vocal text,
            dance text, visual text, total text);
        drop table if exists SkillDB;
        create table if not exists SkillDB (
            idnumber integer unique, skillid integer, maxlevel integer,
            gap integer, percent integer, actime integer, scboost integer,
            cmboost integer, lfplus integer, lfminus integer);
        drop table if exists CenterDB;
        create table if not exists CenterDB (
            idnumber integer unique, centerid integer,
            prvo integer, prda integer, prvi integer, prso integer,
            favo integer, fada integer, favi integer, faso integer,
            anvo integer, anda integer, anvi integer, anso integer);
        drop table if exists PhotoCodeDB;
        create table if not exists PhotoCodeDB (
            idnumber integer unique, photocode text unique);
        ''')
        ssr_list = list()

    elif db_exist == True:
        cls_name.config_info("Checking Main DB and mltdkei_info.txt Updates... Refreshing old data...")
        ssr_list = list()
        ssrlisttem = cur1.execute('''select idnumber, name from IdolDB where rare = "SSR+"''').fetchall()
        if cur1.execute('select maxlevel from SkillDB where idnumber = 103').fetchone()[0] == 12:
            try: already_updated = cur1.execute('select idnumber from IdolDB where maxrank = 5').fetchall()[-4]
            except: pass
        for fair in ssrlisttem:
            if "BRAND NEW PERFORMANCE" in fair[1]: continue
            elif "UNI-ONAIR" in fair[1]: continue
            elif "CHALLENGE FOR GLOW-RY DAYS" in fair[1]: continue
            elif fair[0] > 9000: continue
            ssr_list.append(int(fair[0]))
        if len(ssr_list) != 0:
            try: ssr_list = ssr_list[ssr_list.index(already_updated)+1:]
            except: pass
        updateq_count, updateg_count = 0, 0
        for idnumber in ssr_list:
            if updateq_count == 5: break
            # rare, maxrank, vocal, dance, visual, total, center, skill, maxlevel, percent, photocode
            name, r = load_idolinfo(idnumber)
            maxlevel = r[8]
            old_maxlevel = str(cur1.execute(f'select maxlevel from SkillDB where idnumber={idnumber}').fetchone()[0])
            if maxlevel == old_maxlevel:
                updateq_count += 1
                sleep(0.5)
                continue
            else:
                updateg_count += 1
                vocal, dance, visual, total = r[2:6]
                maxrank, percent = r[1], r[9]
                cur1.execute(f'''update IdolDB set maxrank={maxrank}, vocal='{vocal}', dance='{dance}',
                    visual='{visual}', total='{total}' where idnumber={idnumber}''')
                cur1.execute(f'update SkillDB set maxlevel={maxlevel}, percent={percent} where idnumber={idnumber}')
                sleep(0.5)
        cls_name.config_info(f"Checking Main DB and mltdkei_info.txt Updates... {updateg_count} data affected.")

    sleep(1)
    webcount = 0
    cls_name.config_info("Retrieving New Data from Web...")
    if extract_start <= txt_last:
        idgroup = [i for i in range(extract_start, extract_end)]
        cls_name.config_pbr(webcount, extract_end-extract_start, extract_end-extract_start)
    else:
        idgroup = [i for i in range(txt_last, extract_end)]
        cls_name.config_pbr(webcount, extract_end-txt_last, extract_end-txt_last)
    if db_exist == False:
        idgroup = [9001, 9002, 9003] + idgroup
        cls_name.config_pbr(webcount, extract_end-txt_last+3, extract_end-txt_last+3)
    cls_name.add_info2()
    typefair = cur1.execute('select * from TypeStorage').fetchall()

    for idnumber in idgroup:
        webcount += 1
        if idnumber == 1064 or idnumber == 1065:
            cls_name.update_pbr(webcount, webcount)
            continue
        # rare, maxrank, vocal, dance, visual, total, center, skill, maxlevel, percent, photocode
        name, r = load_idolinfo(idnumber)
        rare = r[0]
        type = 0
        for idname, idtype in typefair:
            if idname in name:
                type = idtype
                break
        maxrank, vocal, dance, visual, total = r[1:6]
        center, skill, maxlevel, percent_fromr, photocode = r[6:11]

        cls_name.update_pbr(webcount, webcount)
        cls_name.config_info2(name)

        centerid = cur1.execute('''select centerid from CenterStorage where center = "%s"''' % center).fetchone()[0]
        prvo, prda, prvi, prso = 0, 0, 0, 0
        favo, fada, favi, faso = 0, 0, 0, 0
        anvo, anda, anvi, anso = 0, 0, 0, 0
        number = findall('[0-9]+', center)
        if "보컬" in center:
            if "세 타입" in center:
                prvo, favo, anvo = number[0], number[0], number[0]
            elif "Princess" in center:
                prvo = number[0]
                try: prso = number[1]
                except: pass
            elif "Fairy" in center:
                favo = number[0]
                try: faso = number[1]
                except: pass
            elif "Angel" in center:
                anvo = number[0]
                try: anso = number[1]
                except: pass
        elif "댄스" in center:
            if "세 타입" in center:
                prda, fada, anda = number[0], number[0], number[0]
            elif "Princess" in center:
                prda = number[0]
                try: prso = number[1]
                except: pass
            elif "Fairy" in center:
                fada = number[0]
                try: faso = number[1]
                except: pass
            elif "Angel" in center:
                anda = number[0]
                try: anso = number[1]
                except: pass
        elif "비주얼" in center:
            if "세 타입" in center:
                prvi, favi, anvi = number[0], number[0], number[0]
            elif "Princess" in center:
                prvi = number[0]
                try: prso = number[1]
                except: pass
            elif "Fairy" in center:
                favi = number[0]
                try: faso = number[1]
                except: pass
            elif "Angel" in center:
                anvi = number[0]
                try: anso = number[1]
                except: pass
        elif "모든 어필" in center:
            if "모든 타입" in center:
                prvo, favo, anvo = number[0], number[0], number[0]
                prda, fada, anda = number[0], number[0], number[0]
                prvi, favi, anvi = number[0], number[0], number[0]
            elif "Princess" in center:
                prvo, prda, prvi = number[0], number[0], number[0]
            elif "Fairy" in center:
                favo, fada, favi = number[0], number[0], number[0]
            elif "Angel" in center:
                anvo, anda, anvi = number[0], number[0], number[0]

        skillid, gap, percent, actime = 0, 0, 0, 0
        scboost, cmboost, lfplus, lfminus = 0, 0, 0, 0
        nolist = findall('[0-9]+', skill)
        if skill == "스킬 없음":
            pass
        elif "Perfect로 판정" in skill:
            if "Fast" in skill and "Slow" in skill: skillid = 3
            elif "Good" in skill: skillid = 2
            elif "Great" in skill: skillid = 1
            gap, percent, actime = nolist[0:3]
        elif "감소하지 않음" in skill:
            skillid = 5
            gap, percent, actime = nolist[0:3]
        elif "콤보 유지" in skill:
            skillid = 7
            gap, percent, actime = nolist[0:3]
        elif "스코어" in skill:
            if "消費し" in skill:
                if "Great" in skill: skillid = 13
                else: skillid = 12
                gap, percent, lfminus, actime, scboost = nolist[0:5]
            elif "회복" in skill:
                if "Great" in skill: skillid = 15
                else: skillid = 14
                gap, percent, actime, scboost, lfplus = nolist[0:5]
            elif "콤보 보너스" in skill:
                if "Great" in skill: skillid = 31
                else: skillid = 30
                gap, percent, actime, scboost, cmboost = nolist[0:5]
            else:
                if "Great" in skill: skillid = 11
                else: skillid = 10
                gap, percent, actime, scboost = nolist[0:4]
        elif "콤보 보너스" in skill:
            if "消費し" in skill:
                if "Great" in skill: skillid = 23
                else: skillid = 22
                gap, percent, lfminus, actime, cmboost = nolist[0:5]
            elif "회복" in skill:
                if "Great" in skill: skillid = 25
                else: skillid = 24
                gap, percent, actime, cmboost, lfplus = nolist[0:5]
            else:
                if "Great" in skill: skillid = 21
                else: skillid = 20
                gap, percent, actime, cmboost = nolist[0:4]
        elif "회복" in skill:
            skillid = 6
            gap, percent, actime, lfplus = nolist[0:4]

        percent = percent_fromr

        cur1.executescript(f'''insert or ignore into PhotoCodeDB (idnumber, photocode) values {idnumber, photocode};
            insert or ignore into CenterDB (idnumber, centerid, prvo, prda, prvi, prso, favo, fada, favi, faso, anvo, anda, anvi, anso)
            values {idnumber, centerid, prvo, prda, prvi, prso, favo, fada, favi, faso, anvo, anda, anvi, anso};
            insert or ignore into IdolDB (idnumber, rare, type, name, maxrank, vocal, dance, visual, total)
            values {idnumber, rare, type, name, maxrank, vocal, dance, visual, total};
            insert or ignore into SkillDB (idnumber, skillid, maxlevel, gap, percent, actime, scboost, cmboost, lfplus, lfminus)
            values {idnumber, skillid, maxlevel, gap, percent, actime, scboost, cmboost, lfplus, lfminus};''')
        # IDNumber,Rare,Name,Have,Rank,SkillLevel
        conn1.commit()
        sleep(0.5)
    ilist = cur1.execute('select idnumber, rare from IdolDB').fetchall()
    global namedict
    for i in ilist:
        if len(i) == 0 or int(i[0]) < txt_last: continue
        try: infodata.append(f'{i[0]},{i[1]},{namedict[int(i[0])]},0,0,1')
        except: continue
    infodata.append('')
    infofile = open('mltdkei_info_kr.txt', 'w', encoding='utf-8')
    infofile.write('\n'.join(infodata))
    infofile.close()
    cls_name.config_info("Main DB and mltdkei_info_kr.txt Update Completed.")
