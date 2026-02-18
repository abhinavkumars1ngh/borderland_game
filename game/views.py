from django.shortcuts import render, redirect
from .models import Round, Entry
from django.db.models import Avg


PLAYER_CODES = {
    "AP1": "Alice",
    "AP2": "Bob",
    "AP3": "Charlie",
    "AP4": "Dave",
    "AP5": "Eve",
}

HOST_CODE = "HOST999"


def login_view(request):
    if request.method == "POST":
        code = request.POST["code"].upper()

        if code == HOST_CODE:
            return redirect("/host/")

        if code in PLAYER_CODES:
            name = PLAYER_CODES[code]
            return redirect(f"/play/?name={name}")

        return render(request, "game/login.html",
                      {"error": "Invalid code"})

    return render(request, "game/login.html")

def get_current_round():
    r = Round.objects.last()
    if not r:
        r = Round.objects.create()
    return r


def player_view(request):
    name = request.GET.get("name", "Player")
    r = get_current_round()

    entry = Entry.objects.filter(round=r, name=name).first()

    return render(request, "game/player.html", {
        "name": name,
        "loser": r.loser,
        "entry": entry
    })


def submit_number(request):
    name = request.POST.get("name", "Player")

    if request.method == "POST":
        num = int(request.POST["number"])
        r = get_current_round()

        Entry.objects.update_or_create(
            name=name,
            round=r,
            defaults={"number": num}
        )

        entries = Entry.objects.filter(round=r)
        avg = entries.aggregate(Avg('number'))['number__avg']

        r.average = avg or 0
        r.save()

    return redirect("/play/?name=" + name)


def host_view(request):
    r = get_current_round()
    entries = Entry.objects.filter(round=r)

    data = []
    for e in entries:
        diff = abs(e.number - r.average)
        data.append((e.name, e.number, diff))

    return render(request, "game/host.html", {
        "entries": data,
        "average": r.average
    })


def choose_loser(request):
    name = request.POST["loser"]
    r = get_current_round()
    r.loser = name
    r.save()
    return redirect("/host/")


def reset_round(request):
    Round.objects.create()
    return redirect("/host/")

def result_view(request):
    name = request.GET.get("name")
    r = get_current_round()

    return render(request, "game/result.html", {
        "name": name,
        "loser": r.loser,
        "average": r.average
    })