from babel_imports import *
import babelfish
import babelserver
from contextlib import contextmanager

logglyfish = babelfish.LogglyFish()
datadogfish = babelfish.DatadogFish()

@contextmanager
def run_background_babelserver():
    cherrypy.engine.start()
    cherrypy.engine.wait(cherrypy.engine.states.STARTED)
    yield
    cherrypy.engine.exit()
    cherrypy.engine.block()

class TestBabelFish(unittest.TestCase):
    def test_logglyfish_to_datadog_translator(self):
        """
        Test that LogglyFish Translates to Datadog EventCreateRequest object
        """
        print("++++++ Test Case: test_loggly_to_datadog_translator")
        
        data = {"alert_name":"foo","edit_alert_link":"1","source_group":"foo","start_time":"Jan 1 00:00:00","end_time":"Jan 1 00:00:01","search_link":"foobar","query":"foo","num_hits":0,"recent_hits":[],"owner_username":"foo","owner_subdomain":"bar","owner_email":"foo"}

        result = logglyfish.translatetodatadog(data)
        print("Translation:")
        print(result.to_str())
        
        self.assertIsInstance(result, EventCreateRequest)
        
class TestBabelServer(unittest.TestCase):
    def test_babelserver(self):
        """
        Test BabelServer is able to start and respond to /health
        """
        print("\n++++++ Integration Test Case: test_babelserver")
        
        cherrypy.tree.mount(babelserver.BabelServer())
        
        with run_background_babelserver(): 
          response = requests.get('http://127.0.0.1:%s/health' % os.environ.get('BABELSERVER_PORT'))
          print(response.text)
          
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.text, "Babelserver is running")

if __name__ == '__main__':
    unittest.main()
