from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .models import Car


# ============================================================
# PUBLIC VIEW — visible to all visitors
# ============================================================
def home(request):
    cars = Car.objects.filter(status='available')
    context = {
        'cars'        : cars,
        'total_stock' : Car.objects.filter(status='available').count(),
        'sold_count'  : Car.objects.filter(status='sold').count(),
        'min_price'   : Car.objects.filter(
                            status='available'
                        ).order_by('price').first(),
        'paystack_public_key': os.environ.get('PAYSTACK_PUBLIC_KEY', ''),
    }
    return render(request, 'home/home.html', context)


# ============================================================
# PAYMENT VIEWS
# ============================================================
def payment_success(request):
    return render(request, 'home/payment_result.html', {
        'success': True,
        'car_name': request.GET.get('car', ''),
        'customer_name': request.GET.get('name', ''),
        'amount': 'Deposit Paid',
        'reference': request.GET.get('ref', ''),
    })


def payment_verify(request):
    reference = request.GET.get('reference', '')
    if not reference:
        return render(request, 'home/payment_result.html', {
            'success': False,
            'message': 'No reference provided.'
        })
    try:
        import urllib.request
        secret_key = os.environ.get('PAYSTACK_SECRET_KEY', '')
        req = urllib.request.Request(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers={'Authorization': f'Bearer {secret_key}'}
        )
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())

        if result['data']['status'] == 'success':
            meta = result['data']['metadata']
            return render(request, 'home/payment_result.html', {
                'success': True,
                'car_name': meta.get('car_name', ''),
                'customer_name': meta.get('customer_name', ''),
                'amount': result['data']['amount'] // 100,
                'reference': reference,
            })
        else:
            return render(request, 'home/payment_result.html', {
                'success': False,
                'message': 'Payment was not successful.'
            })
    except Exception as e:
        return render(request, 'home/payment_result.html', {
            'success': False,
            'message': str(e)
        })


# ============================================================
# CRUD API VIEWS — staff only
# ============================================================
@staff_member_required
def api_cars_list(request):
    cars = Car.objects.all().values(
        'id', 'brand', 'model', 'year', 'category', 'fuel',
        'transmission', 'mileage', 'colour', 'price', 'price_note',
        'badge', 'featured', 'status', 'image_url', 'wa_message'
    )
    return JsonResponse({'cars': list(cars)})


@staff_member_required
@require_POST
def api_car_create(request):
    try:
        data = json.loads(request.body)
        car = Car.objects.create(
            brand        = data.get('brand', ''),
            model        = data.get('model', ''),
            year         = int(data.get('year', 2024)),
            category     = data.get('category', 'suv'),
            fuel         = data.get('fuel', 'Petrol'),
            transmission = data.get('transmission', 'Automatic'),
            mileage      = int(data.get('mileage', 0)),
            colour       = data.get('colour', ''),
            price        = int(data.get('price', 0)),
            price_note   = data.get('priceNote', ''),
            badge        = data.get('badge', ''),
            featured     = bool(data.get('featured', False)),
            status       = 'available',
            image_url    = data.get('img', ''),
            wa_message   = data.get('waMsg', ''),
        )
        return JsonResponse({'success': True, 'id': car.id}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@staff_member_required
@require_http_methods(['PUT'])
def api_car_update(request, car_id):
    try:
        car  = get_object_or_404(Car, id=car_id)
        data = json.loads(request.body)
        car.brand        = data.get('brand',        car.brand)
        car.model        = data.get('model',        car.model)
        car.year         = int(data.get('year',     car.year))
        car.category     = data.get('category',     car.category)
        car.fuel         = data.get('fuel',         car.fuel)
        car.transmission = data.get('transmission', car.transmission)
        car.mileage      = int(data.get('mileage',  car.mileage))
        car.colour       = data.get('colour',       car.colour)
        car.price        = int(data.get('price',    car.price))
        car.price_note   = data.get('priceNote',    car.price_note)
        car.badge        = data.get('badge',        car.badge)
        car.featured     = bool(data.get('featured',car.featured))
        car.image_url    = data.get('img',          car.image_url)
        car.wa_message   = data.get('waMsg',        car.wa_message)
        car.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@staff_member_required
@require_http_methods(['DELETE'])
def api_car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    return JsonResponse({'success': True})


@staff_member_required
@require_POST
def api_car_toggle(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.status = 'sold' if car.status == 'available' else 'available'
    car.save()
    return JsonResponse({'success': True, 'status': car.status})