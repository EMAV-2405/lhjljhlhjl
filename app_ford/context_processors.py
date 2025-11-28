def carrito_total(request):
    total = 0
    if 'carrito' in request.session:
        for key, value in request.session['carrito'].items():
            total += value['cantidad']
    return {'carrito_total': total}