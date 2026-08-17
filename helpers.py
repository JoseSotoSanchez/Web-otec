def obtener_numero_coordinador(codigoCurso):
    if not codigoCurso:
        return "56923747213"

    codigoCurso = codigoCurso.upper()

    if "AAMCE" in codigoCurso:
        return "56931749113"
    elif "TEA" in codigoCurso:
        return "56931749113"
    elif "IEMCE" in codigoCurso:
        return "56923747213"
    elif "CBC" in codigoCurso:
        return "56923747213"
    elif "CDP" in codigoCurso:
        return "56926303214"
    elif "AAC" in codigoCurso:
        return "56923751342"
    elif "AP" in codigoCurso:
        return "56923836736"
    else:
        return "56923747213"  # número por defecto