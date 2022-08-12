from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
days = ["Poniedziałek","Wtorek","Środa","Czwartek","Piątek","Sobota","Niedziela"]
months = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień", ]

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def remove_repetitions(working_months):
    seen = set()
    new_working_months = []
    for d in working_months:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_working_months.append(d)
    return new_working_months

def make_scope(start , end):
    scope = []
    scope.append(start)
    counter = start
    while counter != end:
        scope.append(counter + 1)
        counter += 1
    return scope

def format_date(data):
    data = data['date']
    week_day = days[data.weekday()]
    day = str(data)[8:10]
    month = str(data)[5:7]
    month = months[int(month)-1]
    return week_day+', '+day+' '+month

def format_hour(data):
    data = data['date']
    hour = str(data)[11:13]+':00'
    return hour

def format_data(data):
    new_data = []

    for item in data:
        row = {"day": format_date(item), "hour": format_hour(item)}
        new_data.append(row)

    return new_data

def smap(f):
    return f()