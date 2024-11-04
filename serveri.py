class Server:
    IP_SERVER = 0

    def __new__(cls, *args, **kwargs):
        cls.IP_SERVER += 1
        return super().__new__(cls)

    def __init__(self):
        self.buffer = []
        self.ip = self.IP_SERVER
        self.routers = None

    def get_data(self):
        copy = self.buffer.copy()
        self.buffer = []
        return copy

    def get_ip(self):
        return self.ip

    def send_data(self, data):
        self.routers.buffer.append(data)

    def __str__(self):
        return f'Server with ip = {self.IP_SERVER}'


class Router:
    IP_ROUTER = 0

    def __new__(cls, *args, **kwargs):
        cls.IP_ROUTER += 1
        return super().__new__(cls)

    def __init__(self):
        self.ROUTER_LIST = {}
        self.buffer = []
        self.ip = self.IP_ROUTER

    def link(self, server):
        self.ROUTER_LIST[server.ip] = server
        self.ROUTER_LIST[server.ip].routers = self

    def unlink(self, server):
        self.ROUTER_LIST[server.ip].routers = None
        del self.ROUTER_LIST[server.ip]

    def send_data(self):
        for i in self.buffer:
            if i.ip in self.ROUTER_LIST.keys():
                self.ROUTER_LIST[i.ip].buffer.append(i)
        self.buffer = []


class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


router = Router()
sv_from = Server()
sv_from2 = Server()
router.link(sv_from)
router.link(sv_from2)
router.link(Server())
print(router.ROUTER_LIST)
router.unlink(sv_from)
print(router.ROUTER_LIST)
router.link(Server())
sv_to = Server()
router.link(sv_to)
sv_from2.send_data(Data("Hello", sv_to.get_ip()))
sv_to.send_data(Data("Hi", sv_from.get_ip()))
router.send_data()
print(router.buffer)
print(sv_from.get_data())
print(sv_to.get_data())
print(router.buffer)
