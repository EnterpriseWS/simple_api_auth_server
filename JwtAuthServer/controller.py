import cherrypy
import helper


class OauthAuthServer(object):
    @cherrypy.expose
    def index(self):
        return cherrypy.request.app.config['/']['greeting']


if __name__ == '__main__':
    settings = helper.ConfigurationSettingsLocal(source='settings.json').load_all_settings()
    cherrypy.quickstart(OauthAuthServer(), '/', settings['cherryPy'])
