class System(object):
    def __init__(self, system_name, ip_address, location, components):
        self._system_name = system_name
        self._ip_address = ip_address
        self._location = location

        if not hasattr(components, '__iter__'):
            raise Exception('A systems components must be a collection type')
        if len(components) < 1:
            raise Exception('A system needs at least 1 component')

        self._components = components


class Component(object):
    def __init__(self, ):
        pass


system = System('name', '192.168.114.0', 'locale', [Component(), Component()])