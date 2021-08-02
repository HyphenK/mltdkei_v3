# Python Module #
import sqlite3
from itertools import combinations
# MakeUnit for above ver.4.19 21/08/02

def generate_deck(difull, hlall, hlpr, hlfa, hlan, zST, zDM, zDT, zCB, zSL1, zSL2, IDB_name):
    tclist = list()
    conn1 = sqlite3.connect(IDB_name)
    cur1 = conn1.cursor()
    slso = [[231, 222, 213, "prvo"], [234, 225, 216, "prda"], [237, 228, 219, "prvi"],
            [331, 322, 313, "favo"], [334, 325, 316, "fada"], [337, 328, 319, "favi"],
            [431, 422, 413, "anvo"], [434, 425, 416, "anvo"], [437, 428, 419, "anvo"]]
    ttonly = [str(i[0]) for i in cur1.execute('select idnumber from centerdb where centerid between 121 and 129')]

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
        if zDM >= 6:
            l = l1 + l2 + l3
        else:
            if zST == 4: l = l2 + l1 + l3
            else: l = l1 + l2 + l3
            if len(l) == 0:
                ll4 = cur1.execute(f'''select idnumber from centerdb natural inner join idoldb_sub
                    where {slso[i][3]} between 1 and 89 order by maxtotal desc''').fetchall()
                l = set_leader(ll4, 0)
            else: l = [l[0]]
        return l
    
    def select_leader_v3t(id1, id2):
        ll1 = cur1.execute(f'select idnumber from centerdb where centerid = {id1}').fetchall()
        l1 = set_leader(ll1, 0) # 105
        ll2 = cur1.execute(f'select idnumber from centerdb where centerid = {id2}').fetchall()
        l2 = set_leader(ll2, 0) # 105 + 10
        if zDM >= 6:
            l = l1 + l2
        else:
            if len(l2) != 0: l = l2
            else: l = l1
        return l

    def make_cunit(inputed_data, extract_list):
        clist = list()
        for leader in inputed_data:
            hleader = leader[0:2]
            combilist = list()
            for hidol in extract_list:
                if hidol == hleader: continue
                if not len(combilist) >= zCB: combilist.append(hidol)
            combi = list(combinations(combilist, 4))
            for hunit in combi:
                cunit = tuple([leader]+[difull.get(hunit[i][1]) for i in range(4)])
                typelist = set([int(cunit[i][2]) for i in range(5)])
                if leader[1] in ttonly and len(typelist) < 3: continue
                clist.append(cunit)
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
            if zDT == 0 or zDT == 1: tclist = tclist + make_cunit(select_leader_v3t(121, 122), hlall)
            if zDT == 0 or zDT == 2: tclist = tclist + make_cunit(select_leader_v3t(124, 125), hlall)
            if zDT == 0 or zDT == 3: tclist = tclist + make_cunit(select_leader_v3t(127, 128), hlall)

    elif zSL1 == 1 and zSL2 != 0:
        # Select Leader Idol - Manual Select Mode
        # make_cunit manual mode
        leader = zSL2[0]
        if leader[1] in ttonly:
            tclist = tclist + make_cunit([leader], hlall)
        else:
            if leader[2] == 1: tclist = tclist + make_cunit([leader], hlpr)
            elif leader[2] == 2: tclist = tclist + make_cunit([leader], hlfa)
            elif leader[2] == 3: tclist = tclist + make_cunit([leader], hlan)
            elif leader[2] == 4:
                if zST == 1: extract_list = [hlpr]
                elif zST == 2: extract_list = [hlfa]
                elif zST == 3: extract_list = [hlan]
                elif zST == 4: extract_list = [hlpr, hlfa, hlan, hlall]
                for i in extract_list:
                    tclist = tclist + make_cunit([leader], i)
    return tclist