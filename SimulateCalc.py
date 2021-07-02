# Python Module #
import sqlite3
from random import randrange
# mltdkei Module #
from NewProgress import NewProgress
# SimulateCalc for ver.3.95 21/07/02

def calculator(ntcalc, inputed_ideal, inputed_zTC, songinfo, songinfo_zSN, songinfo_zDI, work_id, IDB_name):
    ideal, howmany, skdict, temp_result, hold_dict = inputed_ideal, inputed_zTC, dict(), list(), dict()
    clcount, clpbr, clmpbr, clfull = 0, 0, 0, len(ntcalc)
    NPG = NewProgress()
    if ideal == True:
        NPG.workid(2, work_id)
        cllength = clfull // 100
        NPG.configmax(clfull, 100)
    else:
        NPG.workid(3, work_id)
        clmlength = howmany // 100
        NPG.configmax(clfull, clfull)

    conn1 = sqlite3.connect(IDB_name)
    cur1 = conn1.cursor()
    klist = [0 for i in range(1, 11)]+[1 for i in range(11, 31)]+[1.3 for i in range(31, 51)]+[1.6 for i in range(51, 71)]+[1.8 for i in range(71, 101)]+[2 for i in range(101, 1201)]
    wlist = [1, 2, 1, 1, 1, 1, 1, 2, 10]
    tenplus_list = [i[0] for i in cur1.execute('select idnumber from centerdb where centerid = 122 or centerid = 125 or centerid = 128').fetchall()]

    for noteinfo in songinfo_zDI:
        if 5 <= noteinfo[2] <= 7:
            hold = round(noteinfo[4]/8/noteinfo[3], 2)
            H = [noteinfo[0]] + [i+1 for i in range(int(noteinfo[0]), int(noteinfo[0]+hold))] + [round(noteinfo[0]+hold, 2)]
            hold_dict[noteinfo[5]] = H
        if noteinfo[2] == 8: bsa = int(noteinfo[5])

    for datafair in ntcalc:
        clcount += 1
        if ideal == True:
            data = datafair
        else:
            data = datafair[1]
        skillset, cunit = list(), data[1]
        for idol in cunit:
            try:
                skinfo = skdict[idol[0]]
            except:
                skinfo = list(cur1.execute(f'select * from skilldb where idnumber = {idol[0]}').fetchone())
                skdict[idol[0]] = skinfo
            level = idol[1]
            if skinfo[2] == 12:
                if level == 12: pass
                elif level == 11: skinfo[4] = skinfo[4] - 5
                else: skinfo[4] = skinfo[4] - 10 - (10 - level)
            else:
                skinfo[4] = skinfo[4] - (10 - level)
            if cunit[0][0] in tenplus_list: skinfo[4] += 10
            if cunit[2] in tenplus_list: skinfo[4] += 10
            skinfo = tuple(skinfo)
            skillset.append(skinfo)

        runtime, hmcount, ayzlist, bsalist = songinfo[5], 0, list(), list()
        Av, Lv, N, Nw = data[0], songinfo_zSN[1], songinfo_zSN[2], songinfo_zSN[5]
        Bs = int(Av*(33+Lv)/20)
        s, c = round((0.7*(Bs/Nw)), 2), round((0.3*(Bs/(2*N-66))), 2)

        while 1:
            if hmcount >= howmany: break
            effectnp, TSlist = [[0, 0, 0, 0] for i in range(runtime)], list()
            for idol in skillset:
                runcount, gaptime, activetime, actpercent, sv, cv = 0, idol[3], idol[5], idol[4], round(idol[6]/100, 2), round(idol[7]/100, 2)
                while runcount < runtime and activetime != 0:
                    runcount += gaptime
                    if ideal == True or actpercent >= randrange(1, 101):
                        for i in range(runcount, runcount+activetime):
                            try:
                                if idol[1] == 30:
                                    if effectnp[i][2] < sv: effectnp[i][2] = sv
                                    if effectnp[i][3] < cv: effectnp[i][3] = cv
                                else:
                                    if effectnp[i][0] < sv: effectnp[i][0] = sv
                                    if effectnp[i][1] < cv: effectnp[i][1] = cv
                            except: break

            for noteinfo in songinfo_zDI:
                Ts = s*wlist[noteinfo[2]]*(1+effectnp[int(noteinfo[0])][0]+effectnp[int(noteinfo[0])][2]) + c*klist[int(noteinfo[5])]*(1+3*effectnp[int(noteinfo[0])][1]+effectnp[int(noteinfo[0])][3])
                if 5 <= noteinfo[2] <= 7:
                    for j in range(len(hold_dict[noteinfo[5]])-1):
                        Ts += round(hold_dict[noteinfo[5]][j+1]-hold_dict[noteinfo[5]][j], 2)*2*s*(1+effectnp[int(hold_dict[noteinfo[5]][j])][0]+effectnp[int(hold_dict[noteinfo[5]][j])][2])
                TSlist.append(Ts)

            ayzlist.append(int(sum(TSlist)))
            bsalist.append(int(sum(TSlist[0:bsa])))
            hmcount += 1
            if ideal == False and hmcount % clmlength == 0:
                clmpbr += 1
                NPG.configmiddle(clmpbr)
        ayzlist.sort(reverse=True)
        bsalist.sort(reverse=True)
        if ideal == True:
            temp_result.append([(ayzlist[0], bsalist[0]), datafair])
            if clcount % cllength == 0:
                clpbr += 1
                NPG.configleft(clcount, clpbr)
        else:
            pclist = int(1/1000*howmany), int(1/100*howmany), int(2/100*howmany), int(5/100*howmany), int(10/100*howmany), int(20/100*howmany), int(50/100*howmany)
            temp_result.append([[datafair[0]]+[(ayzlist[i], bsalist[i]) for i in pclist]]+[datafair[1]])
            NPG.configleft(clcount, clcount)
            clmpbr = 0
            NPG.configmiddle(clmpbr)
    return temp_result
