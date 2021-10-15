# Python Module #
import sqlite3
from random import random
# mltdkei Module #
from NewProgress import NewProgress
# SimulateCalc for above ver.4.22 21/10/07

def quantiles(data, split):
    l = len(data)
    c = int(l/split)
    r, rn, rs = [], [], []
    for i in range(l):
        rn.append(data[i])
        if i % c == c - 1:
            r.append(rn)
            rn = []
    # 0.1, 0.5, 1, 2, 5, 10, 20, 50
    ex = [0, 1], [4, 5], [9, 10], [19, 20], [49, 50], [99, 100], [199, 200], [499, 500]
    for i1, i2 in ex:
        p = (r[i1][-1]+r[i2][0])//2
        rs.append(p)
    return rs

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
            TSlist, stnp, ctnp, snp, cnp = [], [], [], [[0, 0, 0, 0] for i in range(runtime)], [[0, 0, 0, 0] for i in range(runtime)]
            for idol in skillset:
                if idol[1] == 34: continue
                runcount, gaptime, activetime, actpercent, sv, cv = 0, idol[3], idol[5], idol[4]/100, round(idol[6]/100, 2), round(idol[7]/100, 2)
                while runcount < runtime and activetime != 0:
                    runcount += gaptime
                    if ideal == True or actpercent >= random():
                        for i in range(runcount, runcount+activetime):
                            try:
                                if idol[1] == 30:
                                    if snp[i][1] < sv: snp[i][1] = sv
                                    if cnp[i][1] < cv: cnp[i][1] = cv
                                else:
                                    if snp[i][0] < sv: snp[i][0] = sv
                                    if cnp[i][0] < cv: cnp[i][0] = cv
                            except: break
            for idol in skillset:
                if idol[1] != 34: continue
                runcount, gaptime, activetime, actpercent, sv, cv = 0, idol[3], idol[5], idol[4]/100, round(idol[6]/100, 2), round(idol[7]/100, 2)
                while runcount < runtime and activetime != 0:
                    runcount += gaptime
                    if ideal == True or actpercent >= random():
                        for i in range(runcount, runcount+activetime):
                            try:
                                if snp[i][0] != 0 and snp[i][2] < sv: snp[i][2] = sv
                                if snp[i][1] != 0 and snp[i][3] < sv: snp[i][3] = sv
                                if cnp[i][0] != 0 and cnp[i][2] < cv: cnp[i][2] = cv
                                if cnp[i][1] != 0 and cnp[i][3] < cv: cnp[i][3] = cv
                            except: break

            for i in range(len(snp)):
                stnp.append(1+sum(snp[i]))
                ctnp.append(1+3*sum(cnp[i]))

            for n in baselist:
                Ts = n[3]*stnp[n[0]] + n[4]*ctnp[n[0]]
                if 5 <= n[1] <= 7:
                    for j in range(len(hdict[n[2]])-1):
                        Ts += round(hdict[n[2]][j+1]-hdict[n[2]][j], 2)*2*s*stnp[int(hdict[n[2]][j])]
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
            if cllength != 0:
                if clcount % cllength == 0:
                    clpbr += 1
                    NPG.configleft(clcount, clpbr)
        else:
            qtlist_a = quantiles(ayzlist, 1000)
            qtlist_b = quantiles(bsalist, 1000)
            qt_ex = [(int(qtlist_a[i]), int(qtlist_b[i])) for i in range(8)]
            qt_ex = [(int(ayzlist[0]), int(bsalist[0]))] + qt_ex
            temp_result.append([[datafair[0]]+qt_ex]+[datafair[1]])
            NPG.configleft(clcount, clcount)
            clmpbr = 0
            NPG.configmiddle(clmpbr)
    NPG.closewindow()
    return temp_result
