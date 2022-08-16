

def change_subject(subject):
    if subject == 'matematyka':
        subject_changed = 'matematyki'
    elif subject == 'angielski':
        subject_changed = 'angielskiego'
    else:
        subject_changed = subject
    return subject_changed

def change_last_letter(name):
    if name[-1] == 'a':
        a = 'a'
    else:
        a = ''
    return a

def change_minute(minute):
    if minute == 0:
        minute == '00'
    else:
        minute = minute
    return minute