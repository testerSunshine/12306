def time_to_minutes(time_str):
    s = time_str.split(":")
    a = int(s[0]) * 60 + int(s[1])
    return a


def minutes_to_time(minutes):
    m = minutes % 60
    if m<10:
        return str(minutes / 60) + ":" + str("0"+str(m))
    else:
        return str(minutes / 60) + ":" + str(m)


