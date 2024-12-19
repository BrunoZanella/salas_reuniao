from django import template
from datetime import datetime, date, time  # Import explícito de date e time
import colorsys

register = template.Library()

@register.filter
def get_reserva(reservas, chave):
    """
    Retorna a reserva para a data e hora fornecidas.
    """
    if isinstance(chave, date):
        return reservas.get(chave, {})
    if isinstance(chave, time):
        return reservas.get(chave)
    return None


 

@register.filter
def get_user_color(user_id):
    """
    Gera uma cor única para cada usuário baseada no ID
    """
    hue = (user_id * 0.618033988749895) % 1  # Proporção áurea
    saturation = 0.4  # Saturação mais suave
    value = 0.95  # Valor alto para cores mais claras
    
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    return f'rgba({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)}, 0.7)'

@register.filter
def get_text_color(user_id):
    """
    Retorna uma cor de texto baseada no ID do usuário.
    """
    if not isinstance(user_id, int):
        return "#000000"  # Valor padrão para evitar erros

    # Exemplo de lógica para calcular uma cor (substitua se necessário)
    try:
        base_color = (user_id * 12345) % 16777215  # Gera um valor hexadecimal
        return f"#{base_color:06x}"  # Formata como cor hexadecimal
    except Exception:
        return "#000000"  # Valor padrão em caso de erro