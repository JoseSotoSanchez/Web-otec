class Aspirante:
    def __init__(self, form, hostname, ip,environ):
        self.nombre = self.upper_first(form['nombre'].lower())
        self.apellido = self.upper_first(form['apellido'].lower())
        self.rut = form['rut']
        self.sexo = form['sexo']
        self.edad = form['edad']
        self.nacionalidad = form['nacionalidad']
        self.ecivil = form['ecivil']
        self.correo = form['email']
        self.telefono = form['telefono']
        self.profesion = form['profesion']
        self.nestudios = form['nestudios']
        self.slaboral = form['slaboral']
        self.direccion = form['direccion']
        self.region = form['region']
        self.curso = form['curso']
        self.ingreso = form['ingreso']
        self.hostname = hostname
        self.IPAddr = environ['REMOTE_ADDR']
        self.hostnameAddr = f"{self.hostname} / {self.IPAddr}"
    
    def upper_first(self, texto):
        return texto[0].upper() + texto[1:] if texto else texto

class AspiranteJSON:
    def __init__(self, data):
        self.nombre = self.upper_first(data['nombre'])
        self.apellido = self.upper_first(data['apellido'])
        self.rut = data['rut']
        self.sexo = data['sexo']
        self.edad = data['edad']
        self.nacionalidad = data['nacionalidad']
        self.ecivil = data['ecivil']
        self.correo = data['email']
        self.telefono = data['telefono']
        self.profesion = data['profesion']
        self.nestudios = data['nestudios']
        self.slaboral = data['slaboral']
        self.direccion = data['direccion']
        self.region = data['region']
        self.curso = data['curso']
        self.ingreso = data['ingreso']
        self.hostname = data['IPAddr']
        self.IPAddr = data['IPAddr']
        self.hostnameAddr = data['IPAddr']+" / "+data['IPAddr']

    def upper_first(self, texto):
        return texto[0].upper() + texto[1:] if texto else texto