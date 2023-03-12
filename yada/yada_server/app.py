import cherrypy

fr

class YadaWebServer(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def index(self, **params):
        print(params)
        return {"message": "Hello World!"}


if __name__ == '__main__':
    cherrypy.quickstart(YadaWebServer())
