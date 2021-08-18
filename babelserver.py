from babel_imports import *
import babelfish

logglyfish = babelfish.LogglyFish()
datadogfish = babelfish.DatadogFish()

class BabelServer(object):
   config = {'server.socket_host': '0.0.0.0','server.socket_port': int(os.environ.get('BABELSERVER_PORT'))}
   cherrypy.config.update(config)
   @cherrypy.expose
   @cherrypy.tools.json_out()
   @cherrypy.tools.json_in()

   # Translation endpoint
   def translate(self):
      data = cherrypy.request.json

      # TODO: Add support for babelfish.Detect() to determine input format

      translation = logglyfish.translatetodatadog(data)
      response = datadogfish.transmit(translation)
      cherrypy.response.status = response

   # Health status endpoint
   @cherrypy.expose
   def health(self):
      cherrypy.log("Babelserver is running: ><_'>  ><_'>")

if __name__ == '__main__':
   cherrypy.quickstart(BabelServer())
