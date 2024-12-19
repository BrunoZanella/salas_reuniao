from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date, time
from .models import Sala
from reservas.models import Reserva
from django.contrib import messages
from django.http import JsonResponse

def home(request):
    salas = Sala.objects.all()
    agora = datetime.now()
    data_atual = agora.date()
    hora_atual = agora.time()
    
    for sala in salas:
        sala.esta_ocupada = sala.esta_ocupada(data_atual, hora_atual, hora_atual)

    return render(request, 'home.html', {'salas': salas})

def atualizar_status_salas(request):
    agora = datetime.now()
    data_atual = agora.date()
    hora_atual = agora.time()

    # Obtém todas as salas
    salas = Sala.objects.all()
    salas_data = []

    for sala in salas:
        # Acesse os valores diretamente, chamando o método 'esta_ocupada' corretamente
        salas_data.append({
            'id': sala.id,
            'nome': sala.nome,
            'capacidade': sala.capacidade,
            'esta_ocupada': sala.esta_ocupada(data_atual, hora_atual, hora_atual),  # Chame o método aqui
        })

    return JsonResponse({'salas': salas_data})

#@login_required
def calendario_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    data_param = request.GET.get('data')
    
    if data_param:
        hoje = datetime.strptime(data_param, '%Y-%m-%d').date()
    else:
        hoje = datetime.now().date()
    
    hora_atual = datetime.now().time()
    dias_semana = []
    horarios = []
    
    # Encontra a segunda-feira da semana atual
    while hoje.weekday() != 0:
        hoje -= timedelta(days=1)
    
    # Gera os dias da semana (segunda a sexta)
    for i in range(5):
        dias_semana.append(hoje + timedelta(days=i))
    
    # Gera os horários (7:00 às 18:00)
    hora_atual_dt = time(7, 0)  # Usando time() em vez de datetime.strptime
    hora_fim_dt = time(18, 0)
    
    while hora_atual_dt <= hora_fim_dt:
        horarios.append(hora_atual_dt)
        # Avança 30 minutos
        dt = datetime.combine(date.today(), hora_atual_dt) + timedelta(minutes=30)
        hora_atual_dt = dt.time()
    
    # Busca todas as reservas da semana
    reservas = Reserva.objects.filter(
        sala=sala,
        data__range=[dias_semana[0], dias_semana[-1]]
    ).select_related('usuario')

    # Construindo o dicionário de reservas
    reservas_dict = {}
    for dia in dias_semana:
        reservas_dict[dia] = {}
        dia_reservas = reservas.filter(data=dia)
        for reserva in dia_reservas:
            hora_atual = reserva.hora_inicio
            while hora_atual < reserva.hora_fim:
                reservas_dict[dia][hora_atual] = {
                    'usuario': reserva.usuario if reserva.usuario else None,
                    'nome_nao_registrado': reserva.nome_nao_registrado,
                    'empresa_nao_registrado': reserva.empresa_nao_registrado,
                }
                dt = datetime.combine(date.today(), hora_atual) + timedelta(minutes=30)
                hora_atual = dt.time()
    
    # Obtém a sala anterior e próxima
    salas = list(Sala.objects.order_by('id'))
    sala_idx = salas.index(sala)
    sala_anterior = salas[sala_idx - 1] if sala_idx > 0 else None
    sala_proxima = salas[sala_idx + 1] if sala_idx < len(salas) - 1 else None
    
    context = {
        'sala': sala,
        'sala_anterior': sala_anterior,
        'sala_proxima': sala_proxima,
        'dias_semana': dias_semana,
        'horarios': horarios,
        'hora_atual': hora_atual,
        'reservas': reservas_dict,
        'data_atual': hoje.strftime('%Y-%m-%d'),
    }
    return render(request, 'calendario.html', context)