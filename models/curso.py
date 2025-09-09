class Curso:
    def __init__(self, id, nombre, codigo_curso, horario, dias, fecha_inicio, fecha_fin):
        self.id = id
        self.nombre = nombre
        self.codigo_curso = codigo_curso
        self.horario = horario
        self.dias = dias
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "codigo_curso": self.codigo_curso,
            "horario": self.horario,
            "dias": self.dias,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin
        }