# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random
import sys
from config import reservation_limit, library_id1, library_password1, library_id1, library_password1
from smtp import email_myself

reload(sys)
sys.setdefaultencoding('utf-8')


# 시간을 form에 포함할 파라미터로 바꿔줌
def time_parser(time):
    if time:
        divide = map(int, time.split(':'))
        minute = divide[0]*60 + divide[1]
        return minute/10 - 35


# 비어있는 좌석 하나를 선택. time은 hour:minute 형태의 string
def form_maker(seatType, time):
    result = {}
    while seatType:
        # 자리 하나를 랜덤으로 선택
        seat_num_today = random.choice(seatType.keys())

        extra_time = map(time_parser, seatType.pop(seat_num_today))

        # 3시간 예약이 가능한가?
        for i in range(0, reservation_limit):
            if time_parser(time) + i not in extra_time:
                seat_num_today = False
                break

        if seat_num_today:
            result['seat_id'] = seat_num_today
            result['Hsvar'] = time_parser(time)
            result['Hevar'] = result['Hsvar'] + reservation_limit - 1
            result['StimeVar'] = time.replace(':', "")
            result['EtimeVar'] = '00'
            result['Userid'] = library_id1
            result['Userpw'] = library_password1
            result['bars'] = '1700'
            break

    return result


def main(name, time):
    # 좌석 초기화
    seatTypes = {
        'searchInternet': dict(zip([str(i) for i in range(1, 31)], [''] * len(range(1, 31)))),
        'dvd': dict(zip([str(i) for i in range(45, 49)], [''] * len(range(45, 49)))),
        'linguistics': dict(zip([str(i) for i in range(52, 54)], [''] * len(range(52, 54)))),
        'notebook': dict(zip([str(i) for i in range(67, 72)], [''] * len(range(67, 72))))
    }

    # 빈 좌석을 알아내기위한 url, 팝업에서 여기로 iframe이 걸려있음.
    page = lambda seatId: requests.get('http://210.104.8.144:8800/Libmate3_web_hj/Vorvertrag_Position.php?id=' + str(seatId) + '&t=1&s=1')

    for seatType in seatTypes:
        for seatNum in seatTypes[seatType]:
            remain = []
            soup = BeautifulSoup(page(seatNum).content, "html.parser")

            # 빈좌석이라면 bar_green.gif 임. img 태그 객체를 return
            mySoup = soup.find_all("img", {"src": './images/range/bar_green.gif'})
            for imgObj in mySoup:
                try:
                    remain.append(imgObj['alt'])
                except:
                    print 'occur parsing error where handling for ' + imgObj['alt']

            currentType = seatTypes[seatType]
            currentType[seatNum] = remain

    formField = form_maker(seatTypes[name], time)

    if formField:
        # 자리 이름
        seat_today = int(formField['seat_id'])

        if 1 <= seat_today <= 30:
            seat_today = '인터넷검색 ' + str(seat_today)
        elif 45 <= seat_today <= 49:
            seat_today = 'DVD ' + str(seat_today - 44)
        elif 52 <= seat_today <= 54:
            seat_today = '어학 ' + str(seat_today - 51)
        elif 67 <= seat_today <= 72:
            seat_today = '노트북 ' + str(seat_today - 66)
        else:
            seat_today = 'No seat'

        response = requests.post("http://210.104.8.144:8800/Libmate3_web_hj/Vorvertrag_Sql.php", data=formField)
        email_myself(response.text + '\n\n' + seat_today)
    else:
        email_myself('예약실패, 빈 좌석이 없습니다.')
    return

if __name__ == "__main__":
    main('searchInternet', '18:30')

# form field#
#
# 1~30 : 인터넷 검색, 45~48 : DVD, 52~53 : 어학, 67~71 : 노트북
# seat_id:1
#
# 9:00 => 19 ~ 21:50 => 96, 최대 예약시간은 3시간 이므로  Hevar - Hsvar < 18
# Hsvar:81  시작
# Hevar:82  끝
#
# 시작시간, EtimeVar은 무조건 00으로 주는듯
# StimeVar:1920
# EtimeVar:00
#
# 뭔지 모르겠으나 안줘도 되는듯
# bars:1700
# dayAct:
#
# 아이디, 패스워드
# Userid:
# Userpw:

# http://210.104.8.144:8800/Libmate3_web_hj/Vorvertrag_Sql.php 예약요청 보내는 URL



