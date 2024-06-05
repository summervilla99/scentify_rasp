from django.shortcuts import render
from django.http import JsonResponse
import RPi.GPIO as GPIO
import time
import threading

# GPIO set
RELAY_PIN_1 = 17
RELAY_PIN_2 = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RELAY_PIN_2, GPIO.OUT, initial=GPIO.LOW)

def app(request):
    if request.method == "POST":
        pin = request.POST.get('pin')
        if pin:
            pin = int(pin)
            if pin in [RELAY_PIN_1, RELAY_PIN_2]:
                current_state = GPIO.input(pin)
                new_state = GPIO.HIGH if current_state == GPIO.LOW else GPIO.LOW
                GPIO.output(pin, new_state)
                return JsonResponse({'status': 'success', 'pin': pin, 'humidifier_state': new_state})
            else:
                return JsonResponse({'status': 'failure', 'message': 'Invalid pin'}, status=400)
        else:
            return JsonResponse({'status': 'failure', 'message': 'No pin provided'}, status=400)
    return JsonResponse({'status': 'failure'}, status=400)

def index(request):
    state_1 = GPIO.input(RELAY_PIN_1)
    state_2 = GPIO.input(RELAY_PIN_2)
    context = {
        'state_1': state_1,
        'state_2': state_2,
        'RELAY_PIN_1': RELAY_PIN_1,
        'RELAY_PIN_2': RELAY_PIN_2,
    }
    return render(request, 'control/index.html', context)

def timer(request):
    if request.method == "POST":
        pin = request.POST.get('pin')
        duration = request.POST.get('duration')
        if pin and duration:
            pin = int(pin)
            duration = int(duration)
            if pin in [RELAY_PIN_1, RELAY_PIN_2]:
                GPIO.output(pin, GPIO.HIGH)
                threading.Timer(duration, lambda: GPIO.output(pin, GPIO.LOW)).start()
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failure', 'message': 'Invalid pin'}, status=400)
        else:
            return JsonResponse({'status': 'failure', 'message': 'No pin or duration provided'}, status=400)
    return JsonResponse({'status': 'failure'}, status=400)
