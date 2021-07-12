# Python Module #
import sqlite3
from itertools import combinations
# MakeUnit for above ver.4.11 21/07/12

def generate_deck(difull, hlall, hlpr, hlfa, hlan, zST, zDM, zDT, zCB, zSL1, zSL2, IDB_name, beta_enable):
    tclist = list()
    conn1 = sqlite3.connect(IDB_name)
    cur1 = conn1.cursor()
    slso = [[231, 222, 213, "prvo"], [234, 225, 216, "prda"], [237, 228, 219, "prvi"],
            [331, 322, 313, "favo"], [334, 325, 316, "fada"], [337, 328, 319, "favi"],
            [431, 422, 413, "anvo"], [434, 425, 416, "anvo"], [437, 428, 419, "anvo"]]
    ttonly = [str(i[0]) for i in cur1.execute('select idnumber from centerdb where centerid between 121 and 129')]
    pronly = [str(i[0]) for i in cur1.execute('select idnumber from centerdb where centerid between 221 and 229')]
    faonly = [str(i[0]) for i in cur1.execute('select idnumber from centerdb where centerid between 321 and 329')]
    anonly = [str(i[0]) for i in cur1.execute('select idnumber from centerdb where centerid between 421 and 429')]
    skilldict = dict()
    skill_ext = cur1.execute('select idnumber, skillid from skilldb').fetchall()
    for idnumber, skillid in skill_ext:
        skilldict[str(idnumber)] = skillid

    def set_leader(inputed_list, mode):
        leaderlist, leader = list(), list()
        for idnumber in inputed_list:
            try: leaderlist.append(difull[str(idnumber[0])])
            except: continue
        if len(leaderlist) != 0:
            leaderlist.sort(reverse=True)
            if mode == 0 or (mode == 1 and zST == 4):
                leader.append(leaderlist[0])
            elif mode == 1 and zST != 4:
                for idoldata in leaderlist:
                    if len(leader) != 0: break
                    if idoldata[2] == zST: leader.append(idoldata)
                if len(leader) == 0:
                    leader.append(leaderlist[0])
        return leader

    def select_leader(i):
        ll1 = cur1.execute(f'select idnumber from centerdb where centerid = {slso[i][0]}').fetchall()
        l1 = set_leader(ll1, 0) # 90 + 15
        ll2 = cur1.execute(f'select idnumber from centerdb where centerid = {slso[i][1]}').fetchall()
        l2 = set_leader(ll2, 0) # 95
        ll3 = cur1.execute(f'select idnumber from centerdb where centerid = {slso[i][2]}').fetchall()
        l3 = set_leader(ll3, 0) # 90
        if zDM == 6 or zDM == 7 or zDM == 8 or zDM == 9:
            l = l1 + l2 + l3
        else:
            if zST == 4: l = l2 + l1 + l3
            else: l = l1 + l2 + l3
            if len(l) == 0:
                ll4 = cur1.execute(f'''select idnumber from centerdb
                    where {slso[i][3]} != 0 and {slso[i][3]} < 90 order by {slso[i][3]} desc''').fetchall()
                l = set_leader(ll4, 0)
            else:
                l = [l[0]]
        return l

    def make_cunit(inputed_data, extract_list):
        clist = list()
        if beta_enable == 0:
            for leader in inputed_data:
                hleader = leader[0:2]
                combilist = list()
                for hidol in extract_list:
                    if hidol == hleader: continue
                    if not len(combilist) >= zCB: combilist.append(hidol)
                combi = list(combinations(combilist, 4))
                for hunit in combi:
                    cunit = tuple([leader]+[difull.get(hunit[i][1]) for i in range(4)])
                    if leader[1] in ttonly:
                        typelist = [int(cunit[i][2]) for i in range(5)]
                        if 1 in typelist and 2 in typelist and 3 in typelist: clist.append(cunit)
                    elif leader[1] in pronly:
                        typelist = [int(cunit[i][2]) for i in range(5)]
                        if 2 not in typelist and 3 not in typelist: clist.append(cunit)
                    elif leader[1] in faonly:
                        typelist = [int(cunit[i][2]) for i in range(5)]
                        if 1 not in typelist and 3 not in typelist: clist.append(cunit)
                    elif leader[1] in anonly:
                        typelist = [int(cunit[i][2]) for i in range(5)]
                        if 1 not in typelist and 2 not in typelist: clist.append(cunit)
                    else: clist.append(cunit)
        elif beta_enable == 1:
            sc_id, cm_id, db_id, pl_id = [10, 11, 13, 15], [20, 22], [30], [34]
            if 34 in skilldict.values(): meta = 2
            elif 30 in skilldict.values(): meta = 1
            else: meta = 0
            for leader in inputed_data:
                hleader = leader[0:2]
                combilist = list()
                for hidol in extract_list:
                    if hidol == hleader: continue
                    if not len(combilist) >= zCB: combilist.append(hidol)
                combi = list(combinations(combilist, 4))
                for hunit in combi:
                    cunit = tuple([leader]+[difull.get(hunit[i][1]) for i in range(4)])
                    unitskill = [skilldict[i[1]] for i in cunit]
                    sc_c, cm_c, db_c, pl_c, passed = 0, 0, 0, 0, False
                    for skillid in unitskill:
                        if skillid in sc_id: sc_c += 1
                        elif skillid in cm_id: cm_c += 1
                        elif skillid in db_id: db_c += 1
                        elif skillid in pl_id: pl_c += 1
                    if meta >= 0:
                        if (sc_c == 2 and cm_c == 3) or (sc_c == 3 and cm_c == 2): passed = True
                    if meta >= 1:
                        if sc_c == 2 and cm_c == 2 and db_c == 1: passed = True
                    if meta >= 2:
                        if sc_c == 1 and cm_c == 2 and db_c == 1 and pl_c == 1: passed = True
                    if passed == True: pass
                    else: continue
                    if leader[1] in ttonly:
                        typelist = [int(cunit[i][2]) for i in range(5)]
                        if 1 in typelist and 2 in typelist and 3 in typelist: clist.append(cunit)
                    elif leader[1] in pronly:
                        typelist = [int(cunit[i][2]) for i in range(5)]
                        if 2 not in typelist and 3 not in typelist: clist.append(cunit)
                    elif leader[1] in faonly:
                        typelist = [int(cunit[i][2]) for i in range(5)]
                        if 1 not in typelist and 3 not in typelist: clist.append(cunit)
                    elif leader[1] in anonly:
                        typelist = [int(cunit[i][2]) for i in range(5)]
                        if 1 not in typelist and 2 not in typelist: clist.append(cunit)
                    else: clist.append(cunit)
        return clist

    if zSL1 == 0 or (zSL1 == 1 and zSL2 == 0):
        # Select Leader Idol - Default Auto Mode, Results by zST, zDM
        # Generate Combi by zCB (by make_cunit) // Select by zST, zDM, zDT
        if zDM == 0 or (zDM == 1 and (zST == 1 or zST == 4)) or zDM == 3 or zDM == 6 or zDM == 9:
            if zDT == 0 or zDT == 1: tclist = tclist + make_cunit(select_leader(0), hlpr)
            if zDT == 0 or zDT == 2: tclist = tclist + make_cunit(select_leader(1), hlpr)
            if zDT == 0 or zDT == 3: tclist = tclist + make_cunit(select_leader(2), hlpr)
        if zDM == 0 or (zDM == 1 and (zST == 2 or zST == 4)) or zDM == 4 or zDM == 7 or zDM == 9:
            if zDT == 0 or zDT == 1: tclist = tclist + make_cunit(select_leader(3), hlfa)
            if zDT == 0 or zDT == 2: tclist = tclist + make_cunit(select_leader(4), hlfa)
            if zDT == 0 or zDT == 3: tclist = tclist + make_cunit(select_leader(5), hlfa)
        if zDM == 0 or (zDM == 1 and (zST == 3 or zST == 4)) or zDM == 5 or zDM == 8 or zDM == 9:
            if zDT == 0 or zDT == 1: tclist = tclist + make_cunit(select_leader(6), hlan)
            if zDT == 0 or zDT == 2: tclist = tclist + make_cunit(select_leader(7), hlan)
            if zDT == 0 or zDT == 3: tclist = tclist + make_cunit(select_leader(8), hlan)
        if zDM == 0 or zDM == 2 or zDM == 9:
            ll3tvo = cur1.execute('select idnumber from centerdb where centerid between 121 and 123').fetchall()
            ll3tda = cur1.execute('select idnumber from centerdb where centerid between 124 and 126').fetchall()
            ll3tvi = cur1.execute('select idnumber from centerdb where centerid between 127 and 129').fetchall()
            if zDT == 0 or zDT == 1: tclist = tclist + make_cunit(set_leader(ll3tvo, 1), hlall)
            if zDT == 0 or zDT == 2: tclist = tclist + make_cunit(set_leader(ll3tda, 1), hlall)
            if zDT == 0 or zDT == 3: tclist = tclist + make_cunit(set_leader(ll3tvi, 1), hlall)

    elif zSL1 == 1 and zSL2 != 0:
        # Select Leader Idol - Manual Select Mode
        # make_cunit manual mode
        leader = zSL2[0]
        if leader[1] in ttonly:
            tclist = tclist + make_cunit([leader], hlall)
        else:
            extract_list4 = list()
            if leader[2] == 1: extract_list4.append(hlpr)
            elif leader[2] == 2: extract_list4.append(hlfa)
            elif leader[2] == 3: extract_list4.append(hlan)
            if zST == 1 and hlpr not in extract_list4: extract_list4.append(hlpr)
            elif zST == 2 and hlfa not in extract_list4: extract_list4.append(hlfa)
            elif zST == 3 and hlan not in extract_list4: extract_list4.append(hlan)
            if leader[2] == 4 and zST == 4: extract_list4 = [hlpr, hlfa, hlan, hlall]
            for extract_list in extract_list4:
                tclist = tclist + make_cunit([leader], extract_list)
    return tclist