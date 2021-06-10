# Python Module #
import sqlite3
from re import findall
from itertools import combinations

version = "[3.0] 21/06/10"
conn1 = sqlite3.connect('mltdkei_idoldata.sqlite')
cur1 = conn1.cursor()

def version_check():
    return version

def generate_deck(difull, hlall, hlpr, hlfa, hlan, zST, zDM, zDT, zCB, zSL1, zSL2):
    tclist = list()

    def set_leader(inputed_list, mode):
        leaderlist = list()
        for idnumber in inputed_list:
            idnumber = str(idnumber[0])
            idoldata = difull.get(idnumber)
            if not idoldata == None:
                leaderlist.append(idoldata)
        if len(leaderlist) == 0:
            leader = None
        else:
            leaderlist.sort(reverse=True)
            if mode == 0 or (mode == 1 and zST == 4):
                leader = leaderlist[0]
            elif mode == 1 and zST != 4:
                leader = None
                for idoldata in leaderlist:
                    if leader != None: break
                    if idoldata[2] == zST: leader = idoldata
                if leader == None:
                    leader = leaderlist[0]
        return leader

    def set_leader_single(skillid1, skillid2, skillid3, option):
        ll1 = cur1.execute('select idnumber from centerdb where centerid = %s' % skillid1).fetchall()
        l1 = set_leader(ll1, 0)
        ll2 = cur1.execute('select idnumber from centerdb where centerid = %s' % skillid2).fetchall()
        l2 = set_leader(ll2, 0)
        ll3 = cur1.execute('select idnumber from centerdb where centerid = %s' % skillid3).fetchall()
        l3 = set_leader(ll3, 0)
        l = list()
        if zDM == 6 or zDM == 7 or zDM == 8 or zDM == 9:
            if l1 != None: l.append(l1)
            if l2 != None: l.append(l2)
            if l3 != None: l.append(l3)
        else:
            if zST == 4:
                if l2 != None: l.append(l2)
                if l1 != None: l.append(l1)
                if l3 != None: l.append(l3)
            else:
                if l1 != None: l.append(l1)
                if l2 != None: l.append(l2)
                if l3 != None: l.append(l3)
            if len(l) == 0:
                ll4 = cur1.execute(f'''select idnumber from centerdb
                    where {option} != 0 and {option} < 90 order by {option} desc''').fetchall()
                l = [set_leader(ll4, 0)]
            else:
                l = [l[0]]
        return l

    def make_cunit(inputed_data, extract_list, mode):
        clist = list()
        if inputed_data == [None]:
            return clist
        for leader in inputed_data:
            hleader = leader[0:2]
            combilist = list()
            for hidol in extract_list:
                if hidol == hleader: continue
                if not len(combilist) >= zCB:
                    combilist.append(hidol)
            combi = list(combinations(combilist, 4))
            for hunit in combi:
                cunit = tuple([leader]+[difull.get(hunit[i][1]) for i in range(4)])
                if mode == 1:
                    typelist = [int(cunit[i][2]) for i in range(5)]
                    if 1 in typelist and 2 in typelist and 3 in typelist:
                        clist.append(cunit)
                else:
                    clist.append(cunit)
        return clist

    if zSL1 == 0 or (zSL1 == 1 and zSL2 == 0): # Select Leader Idol - Default Auto Mode, Results by zST and zDM
        ll3tvo = cur1.execute('select idnumber from centerdb where centerid = 121').fetchall()
        l3tvo = set_leader(ll3tvo, 1)
        l3tvo = [l3tvo]
        ll3tda = cur1.execute('select idnumber from centerdb where centerid = 124').fetchall()
        l3tda = set_leader(ll3tda, 1)
        l3tda = [l3tda]
        ll3tvi = cur1.execute('select idnumber from centerdb where centerid = 127').fetchall()
        l3tvi = set_leader(ll3tvi, 1)
        l3tvi = [l3tvi]

        lprvo = set_leader_single(231, 222, 213, "prvo")
        lprda = set_leader_single(234, 225, 216, "prda")
        lprvi = set_leader_single(237, 228, 219, "prvi")

        lfavo = set_leader_single(331, 322, 313, "favo")
        lfada = set_leader_single(334, 325, 316, "fada")
        lfavi = set_leader_single(337, 328, 319, "favi")

        lanvo = set_leader_single(431, 422, 413, "anvo")
        landa = set_leader_single(434, 425, 416, "anda")
        lanvi = set_leader_single(437, 428, 419, "anvi")

        # Generate Combi by zCB (by make_cunit) // Select by zST, zDM, zDT

        if zDM == 0 or (zDM == 1 and (zST == 1 or zST == 4)) or zDM == 3 or zDM == 6 or zDM == 9:
            if zDT == 0 or zDT == 1: tclist = tclist + make_cunit(lprvo, hlpr, 0)
            if zDT == 0 or zDT == 2: tclist = tclist + make_cunit(lprda, hlpr, 0)
            if zDT == 0 or zDT == 3: tclist = tclist + make_cunit(lprvi, hlpr, 0)
        if zDM == 0 or (zDM == 1 and (zST == 2 or zST == 4)) or zDM == 4 or zDM == 7 or zDM == 9:
            if zDT == 0 or zDT == 1: tclist = tclist + make_cunit(lfavo, hlfa, 0)
            if zDT == 0 or zDT == 2: tclist = tclist + make_cunit(lfada, hlfa, 0)
            if zDT == 0 or zDT == 3: tclist = tclist + make_cunit(lfavi, hlfa, 0)
        if zDM == 0 or (zDM == 1 and (zST == 3 or zST == 4)) or zDM == 5 or zDM == 8 or zDM == 9:
            if zDT == 0 or zDT == 1: tclist = tclist + make_cunit(lanvo, hlan, 0)
            if zDT == 0 or zDT == 2: tclist = tclist + make_cunit(landa, hlan, 0)
            if zDT == 0 or zDT == 3: tclist = tclist + make_cunit(lanvi, hlan, 0)
        if zDM == 0 or zDM == 2 or zDM == 9:
            if zDT == 0 or zDT == 1: tclist = tclist + make_cunit(l3tvo, hlall, 1)
            if zDT == 0 or zDT == 2: tclist = tclist + make_cunit(l3tda, hlall, 1)
            if zDT == 0 or zDT == 3: tclist = tclist + make_cunit(l3tvi, hlall, 1)

    elif zSL1 == 1 and zSL2 != 0: # Select Leader Idol - Manual Select Mode
        leader = zSL2[0]
        # make_cunit manual mode
        clist, hleader, combilist = list(), leader[0:2], list()
        mode1_temp = cur1.execute('''select idnumber from idoldb natural inner join centerdb
            where centerid = 121 or centerid = 124 or centerid = 127''').fetchall()
        mode1_list = [str(mode1_temp[i][0]) for i in range(0, len(mode1_temp))]
        center = cur1.execute(f'''select center from CenterDB natural inner join CenterStorage
            where idnumber = {leader[1]}''').fetchone()[0]
        if leader[1] in mode1_list:
            extract_list = hlall
            for hidol in extract_list:
                if hidol == hleader: continue
                if not len(combilist) >= zCB: combilist.append(hidol)
            combi = list(combinations(combilist, 4))
            for hunit in combi:
                cunit = tuple([leader]+[difull.get(hunit[i][1]) for i in range(4)])
                typelist = [int(cunit[i][2]) for i in range(5)]
                if 1 in typelist and 2 in typelist and 3 in typelist: clist.append(cunit)
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
                if extract_list == hlall: mode = 1
                else: mode = 0
                for hidol in extract_list:
                    if hidol == hleader: continue
                    if not len(combilist) >= zCB: combilist.append(hidol)
                combi = list(combinations(combilist, 4))
                for hunit in combi:
                    cunit = tuple([leader]+[difull.get(hunit[i][1]) for i in range(4)])
                    if mode == 1:
                        typelist = [int(cunit[i][2]) for i in range(5)]
                        if 1 in typelist and 2 in typelist and 3 in typelist: clist.append(cunit)
                    else: clist.append(cunit)
        tclist = tclist + clist
    return tclist
