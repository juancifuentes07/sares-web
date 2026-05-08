def modelo(y, k):
    return k * (5 - y)


def determinar_iteraciones(nota_inicial):

    if nota_inicial >= 4.7:
        return 10
    elif nota_inicial >= 4.4:
        return 15
    elif nota_inicial >= 4.1:
        return 20
    elif nota_inicial >= 3.8:
        return 25
    elif nota_inicial >= 3.5:
        return 30
    elif nota_inicial >= 3.2:
        return 40
    elif nota_inicial >= 2.9:
        return 45
    elif nota_inicial >= 2.6:
        return 50
    elif nota_inicial >= 2.3:
        return 55
    elif nota_inicial >= 2.0:
        return 60
    elif nota_inicial >= 1.7:
        return 65
    else:
        return 70


def determinar_k(nota_inicial):

    if nota_inicial >= 4.0:
        return 0.03
    elif nota_inicial >= 3.0:
        return 0.045
    else:
        return 0.06


def simular_mejora(nota_inicial):

    iteraciones = determinar_iteraciones(nota_inicial)
    k = determinar_k(nota_inicial)

    y = nota_inicial
    historial = [y]

    h = 1

    for _ in range(iteraciones):

        k1 = modelo(y, k)
        k2 = modelo(y + 0.5 * h * k1, k)
        k3 = modelo(y + 0.5 * h * k2, k)
        k4 = modelo(y + h * k3, k)

        y = y + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)

        historial.append(round(y, 3))

    return {
        "nota_inicial": nota_inicial,
        "nota_final_estimada": round(y, 3),
        "iteraciones": iteraciones,
        "historial": historial
    }