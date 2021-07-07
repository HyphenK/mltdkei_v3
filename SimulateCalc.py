# Python Module #
import sqlite3
from statistics import fmean
from random import random
# mltdkei Module #
from NewProgress import NewProgress
# SimulateCalc for above ver.4.1 21/07/07

def calculator(ntcalc, inputed_ideal, inputed_zTC, songinfo, songinfo_zSN, songinfo_zDI, work_id, IDB_name):
    ideal, howmany, skdict, temp_result, hdict = inputed_ideal, inputed_zTC, dict(), list(), dict()
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
    klist = [0 for i in range(10)]+[1 for i in range(20)]+[1.3 for i in range(20)]+[1.6 for i in range(20)]+[1.8 for i in range(30)]+[2 for i in range(1200)]
    wlist = [1, 2, 1, 1, 1, 1, 1, 2, 10]
    tenplus_list = [str(i[0]) for i in cur1.execute('select idnumber from centerdb where centerid = 122 or centerid = 125 or centerid = 128').fetchall()]

    for noteinfo in songinfo_zDI: # abstime, track, type, bpm, duration, noteid
        if 5 <= noteinfo[2] <= 7:
            hold = round(noteinfo[4]/8/noteinfo[3], 2)
            H = [noteinfo[0]] + [i+1 for i in range(int(noteinfo[0]), int(noteinfo[0]+hold))] + [round(noteinfo[0]+hold, 2)]
            hdict[noteinfo[5]] = H
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
                skinfo = tuple(cur1.execute(f'select * from skilldb where idnumber = {idol[0]}').fetchone())
                skdict[idol[0]] = skinfo
            skinfoL = list(skinfo)
            level = idol[1]
            if skinfoL[2] == 12:
                if level == 12: pass
                elif level == 11: skinfoL[4] = skinfoL[4] - 5
                else: skinfoL[4] = skinfoL[4] - 10 - (10 - level)
            else:
                skinfoL[4] = skinfoL[4] - (10 - level)
            if cunit[0][0] in tenplus_list: skinfoL[4] = skinfoL[4] * 1.1
            if data[2] in tenplus_list: skinfoL[4] = skinfoL[4] * 1.1
            skinfoL = tuple(skinfoL)
            skillset.append(skinfoL)

        runtime, hmcount, ayzlist, bsalist, baselist = songinfo[5], 0, list(), list(), list()
        Av, Lv, N, Nw = data[0], songinfo_zSN[1], songinfo_zSN[2], songinfo_zSN[5]
        Bs = int(Av*(33+Lv)/20)
        s, c = round((0.7*(Bs/Nw)), 2), round((0.3*(Bs/(2*N-66))), 2)

        for noteinfo in songinfo_zDI: # abstime, track, type, bpm, duration, noteid
            baselist.append([int(noteinfo[0]), noteinfo[2], int(noteinfo[5]), s*wlist[noteinfo[2]], c*klist[noteinfo[5]]])

        while 1:
            if hmcount >= howmany: break
            TSlist, svnp, cvnp, spnp, cpnp = list(), [[1, 1] for i in range(runtime)], [[0, 0] for i in range(runtime)], [[0, 0] for i in range(runtime)], [[0, 0] for i in range(runtime)]
            for idol in skillset:
                if idol[1] == 34: continue
                runcount, gaptime, activetime, actpercent, sv, cv = 0, idol[3], idol[5], idol[4]/100, round(1+idol[6]/100, 2), round(idol[7]/100, 2)
                while runcount < runtime and activetime != 0:
                    runcount += gaptime
                    if ideal == True or actpercent >= random():
                        for i in range(runcount, runcount+activetime):
                            try:
                                if idol[1] == 30:
                                    if svnp[i][1] < sv: svnp[i][1] = sv
                                    if cvnp[i][1] < cv: cvnp[i][1] = cv
                                else:
                                    if svnp[i][0] < sv: svnp[i][0] = sv
                                    if cvnp[i][0] < cv: cvnp[i][0] = cv
                            except: break
            for idol in skillset:
                if idol[1] != 34: continue
                runcount, gaptime, activetime, actpercent, sv, cv = 0, idol[3], idol[5], idol[4]/100, round(idol[6]/100, 2), round(idol[7]/100, 2)
                while runcount < runtime and activetime != 0:
                    runcount += gaptime
                    if ideal == True or actpercent >= random():
                        for i in range(runcount, runcount+activetime):
                            try:
                                if svnp[i][0] > svnp[i][1]: spnp[i][0] = sv
                                elif svnp[i][0] < svnp[i][1]: spnp[i][1] = sv
                                if cvnp[i][0] > cvnp[i][1]: cpnp[i][0] = cv
                                elif cvnp[i][0] < cvnp[i][1]: cpnp[i][1] = cv
                            except: break

            for n in baselist:
                Ts = n[3]*(svnp[n[0]][0]+spnp[n[0]][0])*(svnp[n[0]][1]+spnp[n[0]][1]) + n[4]*(1+3*(cvnp[n[0]][0]+cpnp[n[0]][0]))*(1+3*(cvnp[n[0]][1]+cpnp[n[0]][1]))
                if 5 <= n[1] <= 7:
                    for j in range(len(hdict[n[2]])-1):
                        Ts += round(hdict[n[2]][j+1]-hdict[n[2]][j], 2)*2*s*(svnp[int(hdict[n[2]][j])][0]+spnp[int(hdict[n[2]][j])][0])*(svnp[int(hdict[n[2]][j])][1]+spnp[int(hdict[n[2]][j])][1])
                TSlist.append(Ts)

            ayzlist.append(sum(TSlist))
            bsalist.append(sum(TSlist[0:bsa]))
            hmcount += 1
            if ideal == False and hmcount % clmlength == 0:
                clmpbr += 1
                NPG.configmiddle(clmpbr)
        ayzlist.sort(reverse=True)
        bsalist.sort(reverse=True)
        if ideal == True:
            temp_result.append([(int(ayzlist[0]), int(bsalist[0])), datafair])
            if clcount % cllength == 0:
                clpbr += 1
                NPG.configleft(clcount, clpbr)
        else:
            pclist = int(2/1000*howmany), int(2/100*howmany), int(4/100*howmany), int(10/100*howmany), int(20/100*howmany), int(40/100*howmany), int(howmany)
            temp_result.append([[datafair[0]]+[(int(fmean(ayzlist[0:i])), int(fmean(bsalist[0:i]))) for i in pclist]]+[datafair[1]])
            NPG.configleft(clcount, clcount)
            clmpbr = 0
            NPG.configmiddle(clmpbr)
    return temp_result
