# -*- coding: utf-8 -*-
seatTypes = {
    'searchInternet': dict(zip([str(i) for i in range(1, 31)], [''] * len(range(1, 31)))),
    'dvd': dict(zip([str(i) for i in range(45, 49)], [''] * len(range(45, 49)))),
    'linguistics': dict(zip([str(i) for i in range(52, 54)], [''] * len(range(52, 54)))),
    'notebook': dict(zip([str(i) for i in range(67, 72)], [''] * len(range(67, 72))))
}

formField = {'seat_id': str(25)}

for t in seatTypes:
    if formField['seat_id'] in seatTypes[t]:
        # seat_today = t + ' ' + str(int(formField['seat_id']) - min(seatTypes[t].keys()))
        print int(formField['seat_id']) - int(min(seatTypes[t].keys()))