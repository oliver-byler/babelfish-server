from babel_imports import *

class Detector:
   def determineorigin(self, data):
        cherrypy.log('Determining origin of recieved input')
        # Would be cool to have this, but obviously out of scope

class LogglyFish: 
    def translatetodatadog(self, data):
        cherrypy.log('Beginning translation of Loggly to Datadog')
        cherrypy.log('Translating the following message: %s' % (json.dumps(data)))

        # Convert from Loggly alert format to Datadog EventCreateRequest format
        # Datadog: https://github.com/DataDog/datadog-api-client-python/blob/master/docs/v1/EventCreateRequest.md
        # Loggly: https://documentation.solarwinds.com/en/success_center/loggly/content/admin/alert-endpoints.htm

        translation = EventCreateRequest(
        alert_type=EventAlertType("info"),
        date_happened=int(dateutil_parser.parse(data["start_time"]).timestamp()),
        priority=EventPriority("low"),
        related_event_id=int(data["edit_alert_link"].split("/").pop()),
        source_type_name="loggly",
        text="Original Loggly Message: %s" % (json.dumps(data)),
        title="[LogglyAlert] %s" % (data["alert_name"])
        )

        cherrypy.log('Translated!')
        return translation

class DatadogFish:
    def transmit(self, translation):
        cherrypy.log('Configuring Datadog client')

        configuration = datadog_api_client.v1.Configuration(host = "https://api.datadoghq.com")
        configuration.api_key['appKeyAuth'] = os.getenv('DD_APP_KEY')
        configuration.api_key['apiKeyAuth'] = os.getenv('DD_API_KEY')

        cherrypy.log('Transmitting translation to datadog')

        # Call CreateEvent from the EventsApi in data-api-client V1
        # API Docs: https://docs.datadoghq.com/api/latest/events/
        # NOTE: Documentation is very messy for the python api client, would suggest moving to V2 ASAP

        with datadog_api_client.v1.ApiClient(configuration) as api_client:
            api_instance = events_api.EventsApi(api_client)
            try:
                api_response = api_instance.create_event(translation)
                cherrypy.log("Datadog acknowledged transmission with the following response: %s" % api_response)
                return 200 # Return mock status as datadog does not provide any here, very annoying
            except ApiException as e:
                cherrypy.log("Datadog Exception when calling EventsApi->create_event: %s" % e)
                return e.status # Capture status code and pass it back to cherrypy
