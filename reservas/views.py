from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta, time
from .models import Reserva, ConfiguracaoSistema
from salas.models import Sala
from django.db import models
from zoneinfo import ZoneInfo
from django.utils.timezone import make_aware
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

# Configura o timezone de São Paulo
SAO_PAULO_TZ = ZoneInfo("America/Sao_Paulo")

# Helper para converter uma data e hora em timezone-aware
def to_sao_paulo_tz(data, hora):
    """Combina uma data e hora e retorna como um objeto timezone-aware em São Paulo"""
    naive_datetime = datetime.combine(data, hora)
    return make_aware(naive_datetime, timezone=SAO_PAULO_TZ)

# @login_required
def verificar_disponibilidade(request, sala_id, data, hora_inicio):
    sala = get_object_or_404(Sala, id=sala_id)
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()
    hora_fim_obj = (datetime.combine(data_obj, hora_inicio_obj) + timedelta(minutes=30)).time()

    if sala.esta_ocupada(data_obj, hora_inicio_obj, hora_fim_obj):
        salas_sugeridas = Sala.objects.filter(
            capacidade=sala.capacidade
        ).exclude(
            id=sala.id
        ).exclude(
            reserva__data=data_obj,
            reserva__hora_fim__gt=hora_inicio_obj,
            reserva__hora_inicio__lt=hora_fim_obj
        )[:3]

        sugestoes = [{
            'id': s.id,
            'nome': s.nome,
            'capacidade': s.capacidade
        } for s in salas_sugeridas]

        return JsonResponse({
            'disponivel': False,
            'sugestoes': sugestoes,
            'data': data,
            'hora_inicio': hora_inicio
        })

    return JsonResponse({
        'disponivel': True,
        'data': data,
        'hora_inicio': hora_inicio
    })


def arredondar_horario(hora):
    """Arredonda o horário para o próximo intervalo de 30 minutos"""
    minutos = hora.minute
    if minutos <= 30:
        return hora.replace(minute=30)
    return (hora + timedelta(hours=1)).replace(minute=0)

# @login_required
'''
def criar_reserva(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)

    if request.method == 'POST':
        data = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')

        # Ajusta o horário atual caso selecionado
        if hora_inicio == 'now':
            agora = make_aware(datetime.now(), timezone=SAO_PAULO_TZ)
            hora_inicio = arredondar_horario(agora.time())
            data = agora.date()
        else:
            data_obj = datetime.strptime(data, '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
            data = to_sao_paulo_tz(data_obj, hora_inicio).date()

        # Ajusta o horário de fim, se fornecido
        if hora_fim:
            hora_fim = datetime.strptime(hora_fim, '%H:%M').time()
        else:
            hora_fim = (to_sao_paulo_tz(data, hora_inicio) + timedelta(minutes=30)).time()

        # Verifica disponibilidade no intervalo solicitado
        if not sala.esta_ocupada(data, hora_inicio, hora_fim):
            reserva = Reserva(
                sala=sala,
                data=data,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim
            )
            if request.user.is_authenticated:
                reserva.usuario = request.user
            else:
                reserva.nome_nao_registrado = request.POST.get('nome_usuario')
                reserva.empresa_nao_registrado = request.POST.get('empresa')

            reserva.save()
            messages.success(request, 'Reserva criada com sucesso!')
        else:
            messages.error(request, 'Este horário já está reservado.')

        return redirect('calendario_sala', sala_id=sala_id)
'''


def criar_reserva(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    config = ConfiguracaoSistema.objects.first()
#    limite = config.limite_reservas_por_usuario if config else 5
    limite = config.limite_reservas_por_usuario if config and config.limite_reservas_por_usuario else None

    if request.method == 'POST':

        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            messages.error(request, "Você precisa estar autenticado para criar reservas.")
            return redirect('login')

        # usuario = request.user
        
        usuario = request.user if request.user.is_authenticated else None

        # Para usuários autenticados, verifica o número de reservas no mês atual
        # if usuario:
        #     inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        #     fim_mes = (inicio_mes + relativedelta(months=1, days=-1))  # Último dia do mês

        #     reservas_ativas_no_mes = Reserva.objects.filter(
        #         usuario=usuario,
        #         data__gte=inicio_mes,
        #         data__lte=fim_mes
        #     ).count()

        #     if reservas_ativas_no_mes >= limite:
        #         messages.error(request, f"Você atingiu o limite de {limite} reservas para este mês.")
        #         return redirect('minhas_reservas')

        # Para usuários autenticados, verifica o número de reservas no dia
        if usuario and limite:
            reservas_no_dia = Reserva.objects.filter(usuario=usuario, data=timezone.now().date()).count()
            if reservas_no_dia >= limite:
                messages.error(request, f"Você atingiu o limite de {limite} reservas para hoje.")
                return redirect('minhas_reservas')


        # Captura os dados do formulário
        data = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')

        # Ajusta o horário atual caso selecionado
        if hora_inicio == 'now':
            agora = make_aware(datetime.now(), timezone=SAO_PAULO_TZ)
            hora_inicio = arredondar_horario(agora.time())
            data = agora.date()
        else:
            data_obj = datetime.strptime(data, '%Y-%m-%d').date()
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
            data = to_sao_paulo_tz(data_obj, hora_inicio).date()

        # Ajusta o horário de fim, se fornecido
        if hora_fim:
            hora_fim = datetime.strptime(hora_fim, '%H:%M').time()
        else:
            hora_fim = (to_sao_paulo_tz(data, hora_inicio) + timedelta(minutes=30)).time()

        # Verifica a disponibilidade do horário
        if not sala.esta_ocupada(data, hora_inicio, hora_fim):
            reserva = Reserva(
                sala=sala,
                data=data,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim
            )

            if usuario:
                reserva.usuario = usuario
            else:
                reserva.nome_nao_registrado = request.POST.get('nome_usuario')
                reserva.empresa_nao_registrado = request.POST.get('empresa')

            # reserva.save()
            # messages.success(request, 'Reserva criada com sucesso!')
            
            try:
                reserva.clean()  # Aplica as validações antes de salvar
                reserva.save()  # Agora a reserva sempre será salva

                if hasattr(reserva, 'mensagem_ajuste'):
                    messages.warning(request, reserva.mensagem_ajuste)
                else:
                    messages.success(request, '✅ Reserva criada com sucesso!')
            except ValidationError as e:
                messages.error(request," ".join(e.messages))  # Exibe a mensagem amigável


        else:
            messages.error(request, 'Este horário já está reservado.')

        return redirect('calendario_sala', sala_id=sala_id)

    return render(request, 'reservas/criar_reserva.html', {'sala': sala})



@login_required
def minhas_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('data', 'hora_inicio')
    return render(request, 'reservas/minhas_reservas.html', {'reservas': reservas})

@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    if request.user != reserva.usuario and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para editar esta reserva.')
        return redirect('minhas_reservas')
    
    if request.method == 'POST':
        data = request.POST.get('data')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fim = request.POST.get('hora_fim')
        
        # Passa o reserva_id para a função esta_ocupada
        if not reserva.sala.esta_ocupada(data, hora_inicio, hora_fim, reserva_id=reserva.id):
            reserva.data = data
            reserva.hora_inicio = hora_inicio
            reserva.hora_fim = hora_fim
            reserva.save()
            messages.success(request, 'Reserva atualizada com sucesso!')
            return redirect('minhas_reservas')
        else:
            messages.error(request, 'Este horário já está reservado.')
    
    return render(request, 'reservas/editar_reserva.html', {'reserva': reserva})


@login_required
def excluir_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    if request.user != reserva.usuario and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para excluir esta reserva.')
        return redirect('minhas_reservas')
    
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva excluída com sucesso!')
        return redirect('relatorio_reservas')
    
    return render(request, 'reservas/confirmar_exclusao.html', {'reserva': reserva})


def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def relatorio_reservas(request):
    hoje = timezone.localtime().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    fim_semana = inicio_semana + timedelta(days=6)
    
    # Filtros
    periodo = request.GET.get('periodo', 'semana')
    empresa = request.GET.get('empresa')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    reservas = Reserva.objects.all()
    
    if periodo == 'semana':
        reservas = reservas.filter(data__range=[inicio_semana, fim_semana])
    elif periodo == 'semana_anterior':
        reservas = reservas.filter(
            data__range=[inicio_semana - timedelta(days=7), fim_semana - timedelta(days=7)]
        )
    elif periodo == 'semana_seguinte':
        reservas = reservas.filter(
            data__range=[inicio_semana + timedelta(days=7), fim_semana + timedelta(days=7)]
        )
    elif periodo == 'mes':
        reservas = reservas.filter(
            data__year=hoje.year,
            data__month=hoje.month
        )
    elif periodo == 'mes_anterior':
        mes_anterior = hoje.replace(day=1) - timedelta(days=1)
        reservas = reservas.filter(
            data__year=mes_anterior.year,
            data__month=mes_anterior.month
        )
    elif periodo == 'personalizado' and data_inicio and data_fim:
        reservas = reservas.filter(data__range=[data_inicio, data_fim])
    
    if empresa:
        reservas = reservas.filter(
            models.Q(usuario__empresa__icontains=empresa) |
            models.Q(empresa_nao_registrado__icontains=empresa)
        )
    
    # Calcula total de horas
    total_horas = timedelta()
    for reserva in reservas:
        inicio = datetime.combine(reserva.data, reserva.hora_inicio)
        fim = datetime.combine(reserva.data, reserva.hora_fim)
        total_horas += fim - inicio

    # Converte total_horas para horas e minutos
    total_horas_minutes = int(total_horas.total_seconds() // 60)
    horas = total_horas_minutes // 60
    minutos = total_horas_minutes % 60
    total_horas_str = f"{horas:02d}:{minutos:02d}"

    
    context = {
        'reservas': reservas,
        'total_horas': total_horas_str,
        'periodo': periodo,
        'empresa': empresa,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }

    return render(request, 'reservas/relatorio.html', context)

def proxima_semana(request, data):
    data_atual = datetime.strptime(data, '%Y-%m-%d').date()
    proxima = data_atual + timedelta(days=7)
    return JsonResponse({'data': proxima.strftime('%Y-%m-%d')})

def semana_anterior(request, data):
    data_atual = datetime.strptime(data, '%Y-%m-%d').date()
    anterior = data_atual - timedelta(days=7)
    return JsonResponse({'data': anterior.strftime('%Y-%m-%d')})