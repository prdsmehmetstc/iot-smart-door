import time

import requests
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from iot_smart_door.models import Cards, Doors, Personnels, Logs


def home(request):
    if request.method == "GET":
        return render(request, "login.html")

    else:
        username = request.POST.get('admin_username', False)
        password = request.POST.get('admin_password', False)

        if username and password:
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': True})
            else:
                return JsonResponse({"status": False, "message": "Kullanıcı adı ve/veya parola hatalı."})
        else:
            return JsonResponse({"status": False, "message": "Kullanıcı adı ve/veya parola hatalı."})


@login_required
def panel_dashboard(request):
    logs = Logs.objects.all()
    print(logs)
    return render(request, 'panel/dashboard.html', {'logs': logs})


@login_required
def panel_doors(request):
    doors = Doors.objects.all()
    return render(request, 'panel/doors.html', {'doors': doors})


@login_required
def panel_cards(request):
    cards = Cards.objects.all()
    return render(request, 'panel/cards.html', {'cards': cards})


@login_required
def panel_personnels(request):
    personnels = Personnels.objects.all()
    return render(request, 'panel/personnels.html', {'personnels': personnels})


def api_get_door(request):
    if request.GET:
        door_id = request.GET.get('door_id', False)
        if door_id:
            door = Doors.objects.get(id=door_id)
            if door:
                res = {'status': True, 'message': door.name}
            else:
                res = {'status': False, 'message': 'Kapı bulunamadı!'}
        else:
            res = {'status': False, 'message': 'Kapı ID Bilgisi Gelmedi.'}
    else:
        res = {'status': False, 'message': 'Post İsteği Gelmedi.'}

    return JsonResponse(res)


def api_add_door(request):
    if request.GET:
        door_name = request.GET.get('door_name', False)
        if door_name:
            door = Doors(name=door_name, is_visible=True)
            door.save()
            if door.id:
                res = {'status': True, 'message': 'Kayıt Başarıyla Tamamlandı.'}
        else:
            res = {'status': False, 'message': 'İşlem Başarısız!'}
    else:
        res = {'status': False, 'message': 'Kapı ID Bilgisi Gelmedi!'}
    return JsonResponse(res)


def api_delete_door(request):
    if request.GET:
        door_id = request.GET.get('door_id', False)
        if door_id:
            door = Doors.objects.get(id=door_id)
            if door.delete():
                res = {'status': True, 'message': 'Kapı başarıyla silindi.'}
            else:
                res = {'status': False, 'message': 'İşlem Başarısız!'}
        else:
            res = {'status': False, 'message': 'Kapı ID Bilgisi Gelmedi.'}
    else:
        res = {'status': False, 'message': 'Post İsteği Gelmedi.'}
    return JsonResponse(res)


def api_update_door(request):
    if request.GET:
        door_id = request.GET.get('door_id', False)
        new_name = request.GET.get('new_name', False)
        if door_id:
            door = Doors.objects.get(id=door_id)
            door.name = new_name
            if door.save():
                res = {'status': True, 'message': 'Kapı ismi başarıyla güncellendi.'}
            else:
                res = {'status': False, 'message': 'Kapı ismi güncellenemedi!'}
        else:
            res = {'status': False, 'message': 'Kapı ID Bilgisi Gelmedi.'}
    else:
        res = {'status': False, 'message': 'Post İsteği Gelmedi.'}

    return JsonResponse(res)


def api_control(request):
    if request.GET:
        izin_verildi = 'Geçiş İzni Verildi.'
        reddedildi = 'Geçiş İzni Reddedildi!'
        tanimsiz_kart = 'Tanımsız kart.'
        tanimsiz_kapi = 'Tanımsız kapı.'
        izinsiz_kapi = 'İzinsiz kapı.'
        yasakli_kapi = 'Yasaklı kapı.'

        door_id = request.GET.get('door_id', False)
        card_identity = request.GET.get('card_identity', False)
        now = time.strftime("%H:%M %Y-%m-%d")

        if door_id and card_identity:

            # KART VAR İSE
            try:
                card = Cards.objects.get(identity=card_identity)
                # KAPI VAR İSE
                try:
                    door = Doors.objects.get(id=door_id)
                    # PERSONEL TANIMLI İSE
                    try:
                        personnel = Personnels.objects.get(id=card.personnel_id)

                        if Cards.objects.filter(identity=card_identity, banned_doors__in=door_id).count() > 0:
                            res = {
                                'status': False,
                                'card_identity': card_identity,
                                'door_name': str(door),
                                'personnel_name': str(personnel),
                                'message': reddedildi,
                                'reason': yasakli_kapi,
                                'sms_status_code': sms_api_result.status_code,
                            }
                            Logs(door=door, card=card, personnel=personnel, status=False, message=reddedildi, reason=yasakli_kapi).save()
                        elif Cards.objects.filter(identity=card_identity, unauthorized_doors__in=door_id).count() > 0:
                            res = {
                                'status': False,
                                'card_identity': card_identity,
                                'door_name': str(door),
                                'personnel_name': str(personnel),
                                'message': reddedildi,
                                'reason': izinsiz_kapi
                            }
                            Logs(door=door, card=card, personnel=personnel, status=False, message=reddedildi, reason=izinsiz_kapi).save()
                        elif Cards.objects.filter(identity=card_identity, authorized_doors__in=door_id).count() > 0:
                            res = {
                                'status': True,
                                'card_identity': card_identity,
                                'door': str(door),
                                'personnel_name': str(personnel),
                                'message': izin_verildi
                            }
                            Logs(door=door, card=card, personnel=personnel, status=True, message=izin_verildi, reason='').save()
                        else:
                            res = {
                                'status': False,
                                'card_identity': card_identity,
                                'door_name': str(door),
                                'personnel_name': str(personnel),
                                'message': reddedildi,
                                'reason': 'Bu karta tanımlı bir kapı yok.'
                            }
                            Logs(door=door, card=card, personnel=personnel, status=False, message=reddedildi, reason='Bu karta tanımlı bir kapı yok.').save()
                    # PERSONEL TANIMLI DEĞİL İSE
                    except:
                        res = {
                            'status': False,
                            'card_identity': card_identity,
                            'door_id': door_id,
                            'door_name': str(door),
                            'message': reddedildi,
                            'reason': 'Bu karta tanımlı bir personel yok.',
                        }
                        Logs(door=door, card=card, status=False, message=reddedildi, reason="Bu karta tanımlı bir personel yok.").save()
                # KAPI TANIMLI DEĞİL İSE
                except:
                    # PERSONEL TANIMLI İSE
                    try:
                        personnel = Personnels.objects.get(id=card.personnel_id)
                        res = {
                            'status': False,
                            'card_identity': card_identity,
                            'door_id': door_id,
                            'door_name': str(door),
                            'personel': str(personnel),
                            'message': reddedildi,
                            'reason': 'Bu karta tanımlı bir kapı yok.',
                        }
                        Logs(door=door, personnel=personnel, card=card, status=False, message=reddedildi, reason="Bu karta tanımlı bir kapı yok.").save()

                    # PERSONEL TANIMLI DEĞİL İSE
                    except:
                        res = {
                            'status': False,
                            'card_identity': card_identity,
                            'door_id': door_id,
                            'door_name': str(door),
                            'message': reddedildi,
                            'reason': 'Bu karta tanımlı bir kapı yok.',
                        }
                        Logs(door=door, card=card, status=False, message=reddedildi, reason="Bu karta tanımlı bir kapı yok.").save()
            # KART VAR DEĞİL İSE
            except:
                # KAPI VAR İSE
                try:
                    door = Doors.objects.get(id=door_id)
                    res = {
                        'status': False,
                        'card_identity': card_identity,
                        'door_id': door_id,
                        'door_name': str(door),
                        'message': reddedildi,
                        'reason': tanimsiz_kart,
                    }
                    Logs(door=door, status=False, message=reddedildi, reason=tanimsiz_kart + " Gelen Kart ID: " + card_identity).save()
                # KAPI VAR DEĞİL İSE
                except:
                    res = {
                        'status': False,
                        'card_identity': card_identity,
                        'door_id': door_id,
                        'door_name': '',
                        'message': reddedildi,
                        'reason': tanimsiz_kart,
                    }
                    Logs(status=False, message=reddedildi, reason=door_id + " ID'li kapı ve " + card_identity + " ID'li kart tanımlı değil.").save()
        else:
            res = {'status': False, 'message': 'İstek içerisinde Kapı ve Kart bilgisi gelmedi.'}
    else:
        res = {'status': False, 'message': 'İstek gelmedi.'}

    return JsonResponse(res)


def cikis(request):
    logout(request)
    return redirect("/")
