import cherrypy
from yada.yada_python.yada_frontend import Yada

class YadaWebServer(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def index(self, **params):
        request_code = "let x = 1;"
        result = Yada(request_code)
        print(params)
        return {"result": result}


if __name__ == '__main__':
    cherrypy.quickstart(YadaWebServer())
