import datetime
import cnlunar
import re
import json

# 通过日期，得到今日节气，下一个节气
def getSolarTerm(year, month, day):
    a = cnlunar.Lunar(datetime.datetime(year, month, day))
    return a.todaySolarTerms, a.nextSolarTerm

# 根据数字年月日得到干支年
def getYear8Char(year, month, day):
    a = cnlunar.Lunar(datetime.datetime(year, month, day))
    return a.year8Char

# 根据数字年月日得到年月日干支
def get8Char(year, month, day):
    a = cnlunar.Lunar(datetime.datetime(year, month, day))
    return a.year8Char, a.month8Char, a.day8Char

# 根据数字年月日得到农历年月日
def getLunarCn(year, month, day):
    a = cnlunar.Lunar(datetime.datetime(year, month, day))
    return a.lunarYearCn, a.lunarMonthCn, a.lunarDayCn

# 平气运
pingqi8yearlist = ["己未", "己丑", "乙酉", "乙卯", "丁亥", "丁巳", "癸巳", "癸亥", "辛丑", "辛未", "癸卯", "癸酉", "丁卯"]

# 从数字1-6，变成文字初之气、二之气、三之气、四之气、五之气、终之气
def switch_qi(value):
    switcher = {
        1: "初之气",
        2: "二之气",
        3: "三之气",
        4: "四之气",
        5: "五之气",
        6: "终之气",
    }

    return switcher.get(value, 'wrong in qi value')

# 灾宫依据：乙年：灾七宫；丁年：灾三宫；己年：灾五宫；辛年：灾一宫；癸年：灾九宫
def switch_zaigong(value):
    switcher = {
        "乙": "灾七宫",
        "丁": "灾三宫",
        "己": "灾五宫",
        "辛": "灾一宫",
        "癸": "灾九宫",
    }
    return switcher.get(value, '')
# 根据当天节气名字，来区分状态
def switch_today_jieqi(value):
    switcher = {
        "春分": 2,
        "小满": 3,
        "大暑": 4,
        "秋分": 5,
        "小雪": 6,
        "大寒": 1,
    }
    return switcher.get(value, "wrong in today jieqi")

# 年份变化都是以春节为标识，进入下一年
def switch_case(value):
    switcher = {
        # 节气分阶段
        # 根据下一个节气名字，将当前状态分6类
        # 大寒-春分1   立春 雨水 惊蛰 春分
        "立春": 1, 
        "雨水": 1,
        "惊蛰": 1,
        "春分": 1,
        # 春分-小满2   清明 谷雨 立夏 小满
        "清明": 2,
        "谷雨": 2,
        "立夏": 2,
        "小满": 2,
        # 小满-大暑3  芒种 夏至 小暑 大暑
        "芒种": 3,
        "夏至": 3,
        "小暑": 3,
        "大暑": 3,
        # 大暑-秋分4  立秋 处暑 白露 秋分
        "立秋": 4,
        "处暑": 4,
        "白露": 4,
        "秋分": 4,
        # 秋分-小雪5  寒露 霜降 立冬 小雪
        "寒露": 5,
        "霜降": 5,
        "立冬": 5,
        "小雪": 5,
        # 小雪-大寒6  大雪 冬至 小寒  大寒
        "大雪": 6,
        "冬至": 6,
        "小寒": 6,
        "大寒": 6,
        # 大运
        "甲": "太阴湿土（126）^",
        "乙": "阳明燥金（28）˅",
        "丙": "太阳寒水（39）^",
        "丁": "厥阴风木（410）˅",
        "戊": "火运^",
        "己": "太阴湿土（126）˅",
        "庚": "阳明燥金（28）^",
        "辛": "太阳寒水（39）˅",
        "壬": "厥阴风木（410）^",
        "癸": "火运˅",
        # 平运
        "己未": "太阴湿土（126）-",
        "己丑": "太阴湿土（126）-",
        "乙酉": "阳明燥金（28）-",
        "乙卯": "阳明燥金（28）-",
        "丁亥": "厥阴风木（410）-",
        "丁巳": "厥阴风木（410）-",
        "丁卯": "厥阴风木（410）-",
        "癸巳": "火运-",
        "癸亥": "火运-",
        "癸卯": "火运-",
        "癸酉": "火运-",
        "辛丑": "太阳寒水（39）-",
        "辛未": "太阳寒水（39）-",       
        # 司天
        "子": "少阴君火（115）",
        "午": "少阴君火（115）",
        "丑": "太阴湿土（126）",
        "未": "太阴湿土（126）",
        "寅": "少阳相火（17）",
        "申": "少阳相火（17）",
        "卯": "阳明燥金（28）",
        "酉": "阳明燥金（28）",
        "辰": "太阳寒水（39）",
        "戌": "太阳寒水（39）",
        "巳": "厥阴风木（410）",
        "亥": "厥阴风木（410）",
        # 主气
        1: "厥阴风木（410）",
        2: "少阴君火（115）",
        3: "少阳相火（17）",
        4: "太阴湿土（126）",
        5: "阳明燥金（28）",
        6: "太阳寒水（39）",
    }

    return switcher.get(value, 'wrong value')

# 从年干支得到天干
def getTianGan(year8char):
    return year8char[0]

# 从年干支得到地支
def getDiZhi(year8char):
    return year8char[1]

# 从年干支通过匹配得到司天
def getSiTian(year8char):
    dizhi = getDiZhi(year8char)
    return switch_case(dizhi)

# 从当前或者下一个节气得到当前的阶段
def getPhaseStatus(todaysolarterm, nextsolarterm):
    if (todaysolarterm == '无'):
        return switch_case(nextsolarterm)
    else:
        return switch_case(todaysolarterm)

# 客气
def getKeQi(sitian, phasestatus):
    keqiset = ["厥阴风木（410）", "少阴君火（115）", "太阴湿土（126）", "少阳相火（17）", "阳明燥金（28）", "太阳寒水（39）"]
    keqidictset = {}
    num = 0
    length = len(keqiset)
    i = 0
    while True:
        if (i == length):
            i = 0
            continue
        # 找到客气3号位，就开始继续往后补起，4,5,6，逢6之后就从1开始计数
        if num == 7:
            num = 1
        # 客气的3号位置就是司天
        if (sitian == keqiset[i]):
            num = 3
            keqidictset[num] = sitian
        # 继续补内容
        if (len(keqidictset) > 0):
            keqidictset[num] = keqiset[i]
        num = num + 1
        if (len(keqidictset) == 6):
            keqi = keqidictset[phasestatus]
            return keqi
        i = i + 1


# 主气
# 直接根据节气阶段得到
def getZhuQi(phasestatus):
    return switch_case(phasestatus)

# 灾宫，从年干支得到
def getZaiGong(year8char):
    tiangan = getTianGan(year8char)
    return switch_zaigong(tiangan)

# 大运
def getDaYun(year8char):
    if year8char in pingqi8yearlist:
        return switch_case(year8char)

    tiangan = getTianGan(year8char)
    return switch_case(tiangan)

# 在泉
def getZaiQuan(year8char):
    sitian = getSiTian(year8char)
    zaiquan = getKeQi(sitian, 6) # 客气顺序的第6个阶段就是在泉
    return zaiquan


# 司天，客气，主气，在泉
def getAll(year8char, phasestatus):
    sitian = getSiTian(year8char)
    keqi = getKeQi(sitian, phasestatus)
    zhuqi = getZhuQi(phasestatus)
    zaiquan = getZaiQuan(year8char)

    return sitian, keqi, zhuqi, zaiquan

# 司天，客气，主气
def getThree(year8char, phasestatus):
    sitian = getSiTian(year8char)
    keqi = getKeQi(sitian, phasestatus)
    zhuqi = getZhuQi(phasestatus)
    
    return sitian, keqi, zhuqi

def getParticularSolarTerm(year, month, day, solarterm):
    a = cnlunar.Lunar(datetime.datetime(year, month, day))
    solartermsdic = a.thisYearSolarTermsDic

    return solartermsdic[solarterm]

def dateDistance(newdate, olddate):
    x = datetime.date(newdate[0], newdate[1], newdate[2])
    y = datetime.date(olddate[0], olddate[1], olddate[2])

    return abs((x - y).days)

def getWuYunLiuQi(datetime):
    dictdata = [{
                "gongli": "1994-11-10", 
                "nongli": "一九九四十月大初八", 
                "ganzhi": "甲戌 乙亥 庚子", 
                "zaigong": "灾三宫",
                "qi_shunxu": "初之气",
                "jieqi": "小雪", 
                "sitian": "太阳寒水（39）", 
                "keqi": "少阴君火（115）", 
                "dayun": "太阴湿土（126）^", 
                "zhuqi": "阳明燥金（28）", 
                "zaiquan": "太阴湿土（126）", 
                'dong': '',
                'nan': '',
                'zhong': '',
                'xi': '',
                'bei': ''
                }]
    # year = 2056
    # month = 1
    # day = 7
    # # year = 1979
    # # month = 1
    # # day = 30
    # # year = 1994
    # # month = 11
    # # day = 10
    # 转换'1997-1-20'变成数字年月日
    # datetime = '1997-1-20'
    result = re.split('-', datetime)
    year = int(result[0])
    month = int(result[1])
    day = int(result[2])
    print("公历:", datetime)
    dictdata[0]['gongli'] = datetime
    # return "公历:", year, month, day
    olddate = (year, month, day)
    # 打印农历时间
    lunaryear, lunarmonth, lunarday = getLunarCn(year, month, day)
    print("农历:", lunaryear + lunarmonth + lunarday)
    dictdata[0]['nongli'] = lunaryear + lunarmonth + lunarday

    year8char, month8char, day8char = get8Char(year, month, day)
    print("年月日干支:", year8char + " " + month8char + " " + day8char)
    dictdata[0]['ganzhi'] = year8char + " " + month8char + " " + day8char
    # 通过日期，得到今日节气，下一个节气
    todaysolarterm, nextsolarterm = getSolarTerm(year, month, day)
    print("下一个节气:", nextsolarterm)
    dictdata[0]['jieqi'] = nextsolarterm
    # 求阶段（今日节气，下一个节气）
    phasestatus = getPhaseStatus(todaysolarterm, nextsolarterm)

    # 从数字1-6，变成文字初之气、二之气、三之气、四之气、五之气、终之气
    qi_shunxu = switch_qi(phasestatus)
    print("几之气:", qi_shunxu)
    dictdata[0]['qi_shunxu'] = qi_shunxu

    # 从年干支得到灾宫
    zaigong = getZaiGong(year8char)
    print("灾宫:", zaigong)
    dictdata[0]['zaigong'] = zaigong

    ### 先考虑司天、客气、主气、在泉的结果
    ## 春节在大寒后，还有可能春节在立春后，过了春节就进入下一年干支了，总之春节肯定在大寒后
    # 大寒附近要特殊处理
    # 下一个节气是大寒，就要看本年是太过还是不及或平气，如果是不及，则就进入下一年计算；如果是太过，就按照当年计算；如果是平气，则按照当年计算
    if (nextsolarterm == "大寒"):

    ## 以当年的大寒为分界线，太过之年是从当年的大寒13天前开始，不及之年是从当年的大寒13天之后开始，平气之年是从大寒开始
    ## 先看当年6月6日，是什么样的年，如果是太过，就从上一年的大寒开始算
    ### 这个时候的年干支只能用上一年的，因为如果是按照year, 6, 6，就是等于求下一年的年干支了，所以为了求当年的年干支，就是需要将年份减1

    #   年干支 = 当年年份-1年，6月6日的年干支
        year8char = getYear8Char(year - 1, 6, 6)
    #   求司天、客气、主气、在泉（年干支，阶段）
        sitian, keqi, zhuqi, zaiquan = getAll(year8char, phasestatus)

    ## 春节在大寒后，还有可能春节在立春后，过了春节就进入下一年干支了，总之春节肯定在大寒后
    # 立春前也要特殊考虑，立春肯定在大寒后
    elif (nextsolarterm == "立春"):
    #   年干支 = 当年年份年，6月6日的年干支，不做任何操作，反而是下一年的干支
        year8char = getYear8Char(year, 6, 6)
    #   求司天、客气、主气（年干支，阶段）
        sitian, keqi, zhuqi = getThree(year8char, phasestatus)
    ### 在泉和大运需要特殊处理，不行简单使用当年的年干支
    #   年干支 = 当年年份-1年，6月6日的年干支，减1反而是今年的干支
        year8char = getYear8Char(year - 1, 6, 6)
    #   求在泉（年干支）
        zaiquan = getZaiQuan(year8char)

    else:
    #   年干支 = 当年年份的年干支
        # year8char = getYear8Char(year, 6, 6)
    #   求司天、客气、主气、在泉（年干支，阶段）
        sitian, keqi, zhuqi, zaiquan = getAll(year8char, phasestatus)

    ### 单独处理年运问题
    ## 以当年的大寒为分界线，太过之年是从当年的大寒13天前开始，不及之年是从当年的大寒13天之后开始，平气之年是从大寒开始
    ## 先看当年6月6日，是什么样的年，如果是太过，就从上一年的大寒开始算
    ### 这个时候的年干支只能用上一年的，因为如果是按照year, 6, 6，就是等于求下一年的年干支了，所以为了求当年的年干支，就是需要将年份减1
    ## 这两个日期肯定是新一年的1月附近
    if (nextsolarterm == "大寒"):
        #   年干支 = 当年年份年，6月6日的年干支，下一年干支
        year8char = getYear8Char(year, 6, 6)
        #   求大运（年干支）
        dayun = getDaYun(year8char)
        ## 如果是不及，那就看是不是大寒前13天内，如果是，就是进入下一年的大运
        #   计算距离大寒的天数（因为大寒日期是年初，所以必须用不减1的year来求大寒的具体时间）
        date = getParticularSolarTerm(year, 6, 6, "大寒") # 大寒的日期
        yeartuple = (year,)
        
        newdate = yeartuple + date # 大寒的年月日
        #   计算差的天数
        gapdays = dateDistance(newdate, olddate)
        #   太过，大寒前13天，用下一年的大运
        if re.search("^", dayun):
            if gapdays <= 13:
                pass
        else:
            ## 如果否，就是进入当年的大运
            year8char = getYear8Char(year, 6, 6)
            dayun = getDaYun(year8char)
 

    ## 春节在大寒后，还有可能春节在立春后，过了春节就进入下一年干支了，总之春节肯定在大寒后
    # 立春前也要特殊考虑，立春肯定在大寒后
    elif (nextsolarterm == "立春"):
        #   年干支 = 当年年份年，6月6日的年干支，是下一年的干支
        year8char = getYear8Char(year, 6, 6)
        #   求大运（年干支）
        dayun = getDaYun(year8char)
        ## 如果是过，那就看是不是大寒后13天内，如果是按照当年求，否则按照下一年求
        #   计算距离大寒的天数（因为大寒日期是年初，所以必须用不减1的year来求大寒的具体时间）
        date = getParticularSolarTerm(year, 6, 6, "大寒") # 大寒的日期
        yeartuple = (year,)
        
        newdate = yeartuple + date # 大寒的年月日
    #   计算差的天数
        gapdays = dateDistance(newdate, olddate)

        #   如果大运为不及&距离大寒后在13天内，那就不用变，否则就用新的年份 
        if re.search("˅", dayun):
            if gapdays <= 13:
                year8char = getYear8Char(year - 1, 6, 6)
                dayun = getDaYun(year8char)        

    else:
        #   年干支 = 当年年份年，6月6日的年干支，是本年的干支
        # year8char = getYear8Char(year, 6, 6)
        dayun = getDaYun(year8char)   
    

    #   输出结果
    print("司天:", sitian)
    dictdata[0]['sitian'] = sitian
    print("客气:", keqi)
    dictdata[0]['keqi'] = keqi
    print("大运:", dayun)
    dictdata[0]['dayun'] = dayun
    print("主气:", zhuqi)
    dictdata[0]['zhuqi'] = zhuqi
    print("在泉:", zaiquan)
    dictdata[0]['zaiquan'] = zaiquan

    # 统计上图效果
    # 木，东：1，火，南：1，土，中：1， 金，西：1， 水，北：1
    # 输出：东1，南1，中1，西1，北1，便于直接替换图片名称
    # 构造一个list装结果
    list = [sitian, keqi, dayun,zhuqi, zaiquan]
    dongnum = 0
    huonum = 0
    tunum = 0
    jinnum = 0
    shuinum = 0
    for item in list:
        for c in item:
            if re.search("木", c):
                dongnum = dongnum + 1
            elif re.search("火", c):
                huonum = huonum + 1
            elif re.search("土", c):
                tunum = tunum + 1
            elif re.search("金", c):
                jinnum = jinnum + 1
            elif re.search("水", c):
                shuinum = shuinum + 1
    print("东%d" % dongnum) 
    dictdata[0]['dong'] = 'dong' + str(dongnum)
    print("南%d" % huonum)
    dictdata[0]['nan'] = 'nan' + str(huonum)
    print("中%d" % tunum)
    dictdata[0]['zhong'] = 'zhong' + str(tunum)
    print("西%d" % jinnum)
    dictdata[0]['xi'] = 'xi' + str(jinnum)
    print("北%d" % shuinum)
    dictdata[0]['bei'] = 'bei' + str(shuinum)

    print(dictdata)
    return json.dumps(dictdata, ensure_ascii=False)
