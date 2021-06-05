# Python Module #
import sqlite3
from numpy import zeros, array, where
from random import randrange
# mltdkei Module #
from NewProgress import NewProgress

version = "[3.0] 21/06/05"

def version_check():
    return version

def calculator(ntcalc, inputed_ideal, inputed_zTC, songinfo, songinfo_zSN, songinfo_zDI, work_id):
    klist = [0 for i in range(1, 11)]+[1 for i in range(11, 31)]+[1.3 for i in range(31, 51)]+[1.6 for i in range(51, 71)]+[1.8 for i in range(71, 101)]+[2 for i in range(101, 1201)]
    wlist = [1, 2, 1, 1, 1, 1, 1, 2, 10]
    ideal, howmany, skdict, temp_result = inputed_ideal, inputed_zTC, dict(), list()
    clcount, clpbr, clmpbr, clfull = 0, 0, 0, len(ntcalc)
    conn1 = sqlite3.connect('mltdkei_idoldata.sqlite')
    cur1 = conn1.cursor()
    NPG = NewProgress()
    if ideal == True:
        NPG.workid(2, work_id)
        cllength = clfull // 100
        NPG.configmax(clfull, 100)
    else:
        NPG.workid(3, work_id)
        clmlength = howmany // 100
        NPG.configmax(clfull, clfull)

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
            skinfo = tuple(skinfo)
            skillset.append(skinfo)

        runtime, hmcount, ayzlist, bsalist = songinfo[5], 0, list(), list()
        Av, Lv, N, Nw = data[0], songinfo_zSN[1], songinfo_zSN[2], songinfo_zSN[5]
        Bs, fullnp = int(Av*(33+Lv)/20), zeros((runtime, 5))
        s, c = round((0.7*(Bs/Nw)), 2), round((0.3*(Bs/(2*N-66))), 2)

        while 1:
            if hmcount >= howmany: break
            effectnp, number, sklist = fullnp, 0, list()
            while number < 5:
                runcount, gaptime, activetime, actpercent = 0, skillset[number][3], skillset[number][5], skillset[number][4]
                tempnp = zeros((runtime))
                while runcount < runtime and activetime != 0:
                    runcount = runcount + gaptime
                    if ideal == False:
                        if actpercent >= randrange(1, 101):
                            try: tempnp[runcount:runcount+activetime] = 1
                            except: tempnp[runcount:] = 1
                    else:
                        try: tempnp[runcount:runcount+activetime] = 1
                        except: tempnp[runcount:] = 1
                effectnp[0:runtime, number] = tempnp
                number = number + 1
            for extract in effectnp:
                X1, Y1, X2, Y2, skillexc = 0, 0, 0, 0, where(extract == 1)[0]
                if len(skillexc) > 0:
                    for slot in skillexc:
                        X0, Y0 = skillset[slot][6:8]
                        if skillset[slot][1] == 30:
                            if X2 < X0: X2 = X0
                            if Y2 < Y0: Y2 = Y0
                        else:
                            if X1 < X0: X1 = X0
                            if Y1 < Y0: Y1 = Y0
                sklist.append([X1/100, Y1/100, X2/100, Y2/100])

            TotalScore, NC = 0, 0
            for noteinfo in songinfo_zDI:
                w, a, NC, abstime = wlist[noteinfo[2]], 1, NC + 1, int(noteinfo[0])
                nsk, score, combo = sklist[abstime], s*w*a, c*klist[NC]
                Ts = score + combo + score*nsk[0] + combo*3*nsk[1] + score*nsk[2] + combo*nsk[3]
                if 5 <= noteinfo[2] <= 7:
                    nsk2, hold = sklist[abstime], noteinfo[4]/8/noteinfo[3]*2*s
                    Ts = Ts + hold + hold*nsk2[0] + hold*nsk2[2]
                TotalScore = round(TotalScore + Ts, 2)
                if noteinfo[2] == 8: bsalist.append(int(TotalScore))

            ayzlist.append(int(TotalScore))
            hmcount = hmcount + 1
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
