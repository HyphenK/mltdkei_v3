# Pyton Module #
import sqlite3
from re import findall
# mltdkei Module #
from NewProgress import NewProgress
# AppealCalc for above ver.4.13 21/07/19

def appeal_calculator(tclist, temp_splist, zST, difull, zLT, work_id, IDB_name):
    conn1 = sqlite3.connect(IDB_name)
    cur1 = conn1.cursor()
    NPG = NewProgress()
    NPG.workid(1, work_id)
    iclist, cucount, cupbr, cufull = list(), 0, 0, len(tclist)
    culength = len(str(cufull)) - 4
    if culength < 1: culength = 1
    culength = 10 ** culength
    NPG.configmax(cufull, culength)
    cusplit = cufull // culength
    c3tnone = [101, 201, 202, 204, 205, 301, 302, 304, 305, 401, 402, 404, 405]
    cprvo = [111, 207, 208, 209, 211, 212, 213, 221, 222, 231] + c3tnone
    cprda = [111, 207, 208, 209, 214, 215, 216, 224, 225, 234] + c3tnone
    cprvi = [111, 207, 208, 209, 217, 218, 219, 227, 228, 237] + c3tnone
    cfavo = [111, 307, 308, 309, 311, 312, 313, 321, 322, 331] + c3tnone
    cfada = [111, 307, 308, 309, 314, 315, 316, 324, 325, 334] + c3tnone
    cfavi = [111, 307, 308, 309, 317, 318, 319, 327, 328, 337] + c3tnone
    canvo = [111, 407, 408, 409, 411, 412, 413, 421, 422, 431] + c3tnone
    canda = [111, 407, 408, 409, 414, 415, 416, 424, 425, 434] + c3tnone
    canvi = [111, 407, 408, 409, 417, 418, 419, 427, 428, 437] + c3tnone
    c3tvo = [121, 122]
    c3tda = [124, 125]
    c3tvi = [127, 128]
    lcdict, adict, CNFRdict = dict(), dict(), dict()
    alista = ("prvo", "prda", "prvi", "favo", "fada", "favi", "anvo", "anda", "anvi")
    alistb = (0, "prso", "faso", "anso")
    skilldict, gapdict = dict(), dict()
    skill_ext = cur1.execute('select idnumber, skillid, gap from skilldb').fetchall()
    for idnumber, skillid, gap in skill_ext:
        skilldict[str(idnumber)] = skillid
        gapdict[str(idnumber)] = gap
    sc_id, cm_id, db_id, pl_id = [10, 11, 13, 15], [20, 22], [30], [34]
    if 34 in skilldict.values(): meta = 2
    elif 30 in skilldict.values(): meta = 1
    else: meta = 0

    def extract_friend(code1p, code2p, code3):
        nonlocal adict
        code1, code2 = alista[code1p], alistb[code2p]
        codea = str(code1p) + str(code2p)
        if code3 == 1: code3a, code3b = 121, 122
        elif code3 == 2: code3a, code3b = 124, 125
        elif code3 == 3: code3a, code3b = 127, 128
        try:
            idoldata_full = adict[codea]
        except:
            a = cur1.execute(f'''select idnumber, type, vocal, dance, visual, total from centerdb
                natural inner join idoldb natural inner join idoldb_sub
                where {code1} != 0 and centerid != {code3a} and centerid != {code3b}
                order by {code1} + {code2} desc, maxtotal desc''').fetchone()
            total = findall('[0-9]+', a[5])[1]
            idnumber, idoltype, skill = a[0], a[1], 0
            vocal = findall('[0-9]+', a[2])[1]
            dance = findall('[0-9]+', a[3])[1]
            visual = findall('[0-9]+', a[4])[1]
            idoldata_full = total, idnumber, idoltype, skill, vocal, dance, visual
            adict[codea] = idoldata_full
        friend_list.append(idoldata_full)

    def extract_friend_c3t(lcid, cid_list):
        try:
            idoldata_full = adict[str(lcid)]
        except:
            a = cur1.execute(f'''select idnumber, type, vocal, dance, visual, total from centerdb
                natural inner join idoldb natural inner join idoldb_sub
                where centerid in ({cid_list[0]}, {cid_list[1]})
                order by centerid desc, type != {zST}, maxtotal desc''').fetchone()
            total = findall('[0-9]+', a[5])[1]
            idnumber, idoltype, skill = a[0], a[1], 0
            vocal = findall('[0-9]+', a[2])[1]
            dance = findall('[0-9]+', a[3])[1]
            visual = findall('[0-9]+', a[4])[1]
            idoldata_full = total, idnumber, idoltype, skill, vocal, dance, visual
            adict[str(lcid)] = idoldata_full
        friend_list.append(idoldata_full)

    for cunit in tclist:
        cucount = cucount + 1
        # Check Before Calculate
        unitskill = [(skilldict[i[1]], gapdict[i[1]]) for i in cunit]
        unit_c, passed, sc_p, cm_p = [0, 0, 0, 0], False, set(), set()
        for skillid, gap in unitskill:
            if skillid in sc_id:
                unit_c[0] += 1
                sc_p.add(gap)
            elif skillid in cm_id:
                unit_c[1] += 1
                cm_p.add(gap)
            elif skillid in db_id: unit_c[2] += 1
            elif skillid in pl_id: unit_c[3] += 1
        if meta >= 0 and (unit_c == [2, 3, 0, 0] or unit_c == [3, 2, 0, 0]): passed = True
        if meta >= 1 and unit_c == [2, 2, 1, 0]: passed = True
        if meta >= 2 and unit_c == [1, 2, 1, 1]: passed = True
        if len(sc_p) != unit_c[0] or len(cm_p) != unit_c[1]: passed = False
        if passed == False:
            if cucount % cusplit == 0:
                cupbr += 1
                NPG.configleft(cucount, cupbr)
            continue

        # Select Friend
        friend_list = list()
        try:
            lcid = lcdict[cunit[0][1]]
        except:
            lcid = cur1.execute(f'select centerid from centerdb where idnumber = {cunit[0][1]}').fetchone()[0]
            lcdict[cunit[0][1]] = lcid
        if zST == 4:
            if lcid in cprvo: extract_friend(0, 0, 1)
            if lcid in cprda: extract_friend(1, 0, 2)
            if lcid in cprvi: extract_friend(2, 0, 3)
            if lcid in cfavo: extract_friend(3, 0, 1)
            if lcid in cfada: extract_friend(4, 0, 2)
            if lcid in cfavi: extract_friend(5, 0, 3)
            if lcid in canvo: extract_friend(6, 0, 1)
            if lcid in canda: extract_friend(7, 0, 2)
            if lcid in canvi: extract_friend(8, 0, 3)
            if lcid in c3tvo: extract_friend_c3t(lcid, c3tvo)
            if lcid in c3tda: extract_friend_c3t(lcid, c3tda)
            if lcid in c3tvi: extract_friend_c3t(lcid, c3tvi)
        else:
            if lcid in cprvo: extract_friend(0, 1, 1)
            if lcid in cprda: extract_friend(1, 1, 2)
            if lcid in cprvi: extract_friend(2, 1, 3)
            if lcid in cfavo: extract_friend(3, 2, 1)
            if lcid in cfada: extract_friend(4, 2, 2)
            if lcid in cfavi: extract_friend(5, 2, 3)
            if lcid in canvo: extract_friend(6, 3, 1)
            if lcid in canda: extract_friend(7, 3, 2)
            if lcid in canvi: extract_friend(8, 3, 3)
            if lcid in c3tvo: extract_friend_c3t(lcid, c3tvo)
            if lcid in c3tda: extract_friend_c3t(lcid, c3tda)
            if lcid in c3tvi: extract_friend_c3t(lcid, c3tvi)

        # Make Support List
        splist = list()
        spnblist = list()
        for idolbackup in temp_splist:
            if len(splist) == 10: break
            supportable = True
            for idol in cunit:
                if idolbackup[1] == idol[1]:
                    supportable = False
                    break
            if supportable == True:
                splist.append(difull.get(idolbackup[1]))
                spnblist.append(idolbackup[1])
        spnblist = tuple(spnblist)

        for friend in friend_list:
            voB, daB, viB = 0, 0, 0 # vocalbase, dancebase, visualbase
            voS, daS, viS = 0, 0, 0 # vocalsong, dancesong, visualsong
            voC, daC, viC = 0, 0, 0 # vocalcenter, dancecenter, visualcenter
            voF, daF, viF = 0, 0, 0 # vocalfriend, dancefriend, visualfriend
            SPAp, SPsP, SPsO = 0, 0, 0 # specialappeal, specialsupport, specialscore
            vosP, dasP, visP = 0, 0, 0 # vocalsupport, dancesupport, visualsupport
            voSsP, daSsP, viSsP = 0, 0, 0 # vocalsongsupport, dancesongsupport, visualsongsupport
            voL, voR = 0, 0 # vocalleft, vocalright
            daL, daR = 0, 0 # danceleft, danceright
            viL, viR = 0, 0 # visualleft, visualright
            cunitlist = list()

            # MainDeck Base & Song Bonus & Special Bonus
            for idol in cunit:
                cunitlist.append((idol[1], idol[3]))
                vo, da, vi = int(idol[4]), int(idol[5]), int(idol[6])
                voB, daB, viB = voB + vo, daB + da, viB + vi
                if zST == 4 or zST == idol[2] or idol[2] == 4:
                    voS, daS, viS = voS + vo, daS + da, viS + vi
                if zLT == 0: pass
                elif zLT == 1: SPAp = SPAp + vo
                elif zLT == 2: SPAp = SPAp + da
                elif zLT == 3: SPAp = SPAp + vi

            voS, daS, viS, SPAp = int(voS*0.3), int(daS*0.3), int(viS*0.3), int(SPAp*1.2)
            cunitlist = tuple(cunitlist)

            # MainDeck Center Bonus
            try:
                CN = CNFRdict[cunit[0][1]]
            except:
                CN = cur1.execute(f'select * from centerdb where idnumber = {cunit[0][1]}').fetchone()
                CNFRdict[cunit[0][1]] = CN

            if CN[1] in c3tvo: voC += int(voB*1.05)
            elif CN[1] in c3tda: daC += int(daB*1.05)
            elif CN[1] in c3tvi: viC += int(viB*1.05)
            else:
                if CN[2] != 0: voC = voC + int(voB*CN[2]/100)
                elif CN[6] != 0: voC = voC + int(voB*CN[6]/100)
                elif CN[10] != 0: voC = voC + int(voB*CN[10]/100)
                if CN[3] != 0: daC = daC + int(daB*CN[3]/100)
                elif CN[7] != 0: daC = daC + int(daB*CN[7]/100)
                elif CN[11] != 0: daC = daC + int(daB*CN[11]/100)
                if CN[4] != 0: viC = viC + int(viB*CN[4]/100)
                elif CN[8] != 0: viC = viC + int(viB*CN[8]/100)
                elif CN[12] != 0: viC = viC + int(viB*CN[12]/100)
                if zST == 1 and CN[5] != 0:
                    if CN[2] != 0: voC = voC + int(voB*CN[5]/100)
                    if CN[3] != 0: daC = daC + int(daB*CN[5]/100)
                    if CN[4] != 0: viC = viC + int(viB*CN[5]/100)
                if zST == 2 and CN[9] != 0:
                    if CN[6] != 0: voC = voC + int(voB*CN[9]/100)
                    if CN[7] != 0: daC = daC + int(daB*CN[9]/100)
                    if CN[8] != 0: viC = viC + int(viB*CN[9]/100)
                if zST == 3 and CN[13] != 0:
                    if CN[10] != 0: voC = voC + int(voB*CN[13]/100)
                    if CN[11] != 0: daC = daC + int(daB*CN[13]/100)
                    if CN[12] != 0: viC = viC + int(viB*CN[13]/100)

            # MainDeck Friend Bonus
            try:
                FR = CNFRdict[friend[1]]
            except:
                FR = cur1.execute(f'select * from centerdb where idnumber = {friend[1]}').fetchone()
                CNFRdict[friend[1]] = FR

            if FR[1] in c3tvo: voF += int(voB*1.05)
            elif FR[1] in c3tda: daF += int(daB*1.05)
            elif FR[1] in c3tvi: viF += int(viB*1.05)
            else:
                if FR[2] != 0: voF = voF + int(voB*FR[2]/100)
                elif FR[6] != 0: voF = voF + int(voB*FR[6]/100)
                elif FR[10] != 0: voF = voF + int(voB*FR[10]/100)
                if FR[3] != 0: daF = daF + int(daB*FR[3]/100)
                elif FR[7] != 0: daF = daF + int(daB*FR[7]/100)
                elif FR[11] != 0: daF = daF + int(daB*FR[11]/100)
                if FR[4] != 0: viF = viF + int(viB*FR[4]/100)
                elif FR[8] != 0: viF = viF + int(viB*FR[8]/100)
                elif FR[12] != 0: viF = viF + int(viB*FR[12]/100)
                if zST == 1 and FR[5] != 0:
                    if FR[2] != 0: voF = voF + int(voB*FR[5]/100)
                    if FR[3] != 0: daF = daF + int(daB*FR[5]/100)
                    if FR[4] != 0: viF = viF + int(viB*FR[5]/100)
                if zST == 2 and FR[9] != 0:
                    if FR[6] != 0: voF = voF + int(voB*FR[9]/100)
                    if FR[7] != 0: daF = daF + int(daB*FR[9]/100)
                    if FR[8] != 0: viF = viF + int(viB*FR[9]/100)
                if zST == 3 and FR[13] != 0:
                    if FR[10] != 0: voF = voF + int(voB*FR[13]/100)
                    if FR[11] != 0: daF = daF + int(daB*FR[13]/100)
                    if FR[12] != 0: viF = viF + int(viB*FR[13]/100)

            # Friend Base
            vo, da, vi = int(friend[4]), int(friend[5]), int(friend[6])
            voB, daB, viB = voB + vo, daB + da, viB + vi

            # Friend Center Bonus
            if CN[1] in c3tvo: voC += int(vo*1.05)
            elif CN[1] in c3tda: daC += int(da*1.05)
            elif CN[1] in c3tvi: viC += int(vi*1.05)
            else:
                if CN[2] != 0: voC = voC + int(vo*CN[2]/100)
                elif CN[6] != 0: voC = voC + int(vo*CN[6]/100)
                elif CN[10] != 0: voC = voC + int(vo*CN[10]/100)
                if CN[3] != 0: daC = daC + int(da*CN[3]/100)
                elif CN[7] != 0: daC = daC + int(da*CN[7]/100)
                elif CN[11] != 0: daC = daC + int(da*CN[11]/100)
                if CN[4] != 0: viC = viC + int(vi*CN[4]/100)
                elif CN[8] != 0: viC = viC + int(vi*CN[8]/100)
                elif CN[12] != 0: viC = viC + int(vi*CN[12]/100)
                if zST == 1 and CN[5] != 0:
                    if CN[2] != 0: voC = voC + int(vo*CN[5]/100)
                    if CN[3] != 0: daC = daC + int(da*CN[5]/100)
                    if CN[4] != 0: viC = viC + int(vi*CN[5]/100)
                if zST == 2 and CN[9] != 0:
                    if CN[6] != 0: voC = voC + int(vo*CN[9]/100)
                    if CN[7] != 0: daC = daC + int(da*CN[9]/100)
                    if CN[8] != 0: viC = viC + int(vi*CN[9]/100)
                if zST == 3 and CN[13] != 0:
                    if CN[10] != 0: voC = voC + int(vo*CN[13]/100)
                    if CN[11] != 0: daC = daC + int(da*CN[13]/100)
                    if CN[12] != 0: viC = viC + int(vi*CN[13]/100)

            # Friend Friend Bonus
            if FR[1] in c3tvo: voF += int(vo*1.05)
            elif FR[1] in c3tda: daF += int(da*1.05)
            elif FR[1] in c3tvi: viF += int(vi*1.05)
            else:
                if FR[2] != 0: voF = voF + int(vo*FR[2]/100)
                elif FR[6] != 0: voF = voF + int(vo*FR[6]/100)
                elif FR[10] != 0: voF = voF + int(vo*FR[10]/100)
                if FR[3] != 0: daF = daF + int(da*FR[3]/100)
                elif FR[7] != 0: daF = daF + int(da*FR[7]/100)
                elif FR[11] != 0: daF = daF + int(da*FR[11]/100)
                if FR[4] != 0: viF = viF + int(vi*FR[4]/100)
                elif FR[8] != 0: viF = viF + int(vi*FR[8]/100)
                elif FR[12] != 0: viF = viF + int(vi*FR[12]/100)
                if zST == 1 and FR[5] != 0:
                    if FR[2] != 0: voF = voF + int(vo*FR[5]/100)
                    if FR[3] != 0: daF = daF + int(da*FR[5]/100)
                    if FR[4] != 0: viF = viF + int(vi*FR[5]/100)
                if zST == 2 and FR[9] != 0:
                    if FR[6] != 0: voF = voF + int(vo*FR[9]/100)
                    if FR[7] != 0: daF = daF + int(da*FR[9]/100)
                    if FR[8] != 0: viF = viF + int(vi*FR[9]/100)
                if zST == 3 and FR[13] != 0:
                    if FR[10] != 0: voF = voF + int(vo*FR[13]/100)
                    if FR[11] != 0: daF = daF + int(da*FR[13]/100)
                    if FR[12] != 0: viF = viF + int(vi*FR[13]/100)

            # Friend Song Bonus & Special Bonus
            if zST == 4 or zST == friend[2] or friend[2] == 4:
                voS, daS, viS = voS + int(vo*0.3), daS + int(da*0.3), viS + int(vi*0.3)

            # Support Base & Song Bonus & Special Bonus
            for idolsP in splist:
                vo, da, vi = int(idolsP[4]), int(idolsP[5]), int(idolsP[6])
                vosP, dasP, visP = vosP + vo, dasP + da, visP + vi
                if zST == 4 or zST == idolsP[2] or idolsP[2] == 4:
                    voSsP, daSsP, viSsP = voSsP + int(vo*0.3), daSsP + int(da*0.3), viSsP + int(vi*0.3)
                if zLT == 0: pass
                elif zLT == 1: SPsP = SPsP + int(vo*1.2)
                elif zLT == 2: SPsP = SPsP + int(da*1.2)
                elif zLT == 3: SPsP = SPsP + int(vi*1.2)

            voSsP, daSsP, viSsP = int(voSsP/2), int(daSsP/2), int(viSsP/2)
            vosP, dasP, visP, SPsP = int(vosP/2), int(dasP/2), int(visP/2), int(SPsP/2)

            voL, voR = voB+vosP, voS+voSsP+voC+voF
            daL, daR = daB+dasP, daS+daSsP+daC+daF
            viL, viR = viB+visP, viS+viSsP+viC+viF
            SPsO = SPAp+SPsP
            if zLT == 0: pass
            elif zLT == 1: voR = voR + SPsO
            elif zLT == 2: daR = daR + SPsO
            elif zLT == 3: viR = viR + SPsO
            totalAP = voL+voR+daL+daR+viL+viR

            vodata = "".join([str(voL), "(+", str(voR), ")"])
            dadata = "".join([str(daL), "(+", str(daR), ")"])
            vidata = "".join([str(viL), "(+", str(viR), ")"])

            totaldata = totalAP, cunitlist, str(friend[1]), spnblist, vodata, dadata, vidata
            iclist.append(totaldata)

        if cucount % cusplit == 0:
            cupbr += 1
            NPG.configleft(cucount, cupbr)

    NPG.configleft(cucount, cupbr)
    return iclist
