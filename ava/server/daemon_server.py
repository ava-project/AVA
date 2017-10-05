import json
from os import path, makedirs
from http.server import HTTPServer
import requests
from .httprequest_handler import HTTPRequestHandler
from ..config import ConfigLoader
from ..plugins.store import PluginStore
from ..components import _BaseComponent
from avasdk.plugins.builders.event import build_event

class DaemonServer(_BaseComponent):
    """
    The DaemonServer is a minimalist http server that will allow interface
    to manage the daemon.
    """

    _user = {}
    _is_log = False

    def __init__(self, queues):
        """
        Initializer

            @param daemon: a reference to the daemon object
            @type daemon: Daemon
            @param base_url: the API URL
            @type base_url: string
        """
        super().__init__(queues)
        self._is_running = False
        self._httpd = None
        DaemonServer._queue_plugin_manage = None
        DaemonServer._plugin_store = PluginStore()
        DaemonServer._config = ConfigLoader(None, None)
        DaemonServer._base_url = DaemonServer._config.get('API_address')
        DaemonServer._mock_url = "http://127.0.0.1:3000"
        DaemonServer._download_folder = path.join(path.expanduser('~'), '.ava', 'download')
        if not path.exists(DaemonServer._download_folder):
            makedirs(DaemonServer._download_folder)

    def setup(self):
        DaemonServer._queue_plugin_manage = self._queues['QueuePluginManager']

    @staticmethod
    @HTTPRequestHandler.get('/')
    def index(request):
        """
        This URL is a test to be sure that the DaemonServer can handle a request
        """
        return requests.get(DaemonServer._mock_url + '/')

    @staticmethod
    @HTTPRequestHandler.post('/login')
    def post_user_login(request):
        """
        Login
        """
        data = {'email': request.fields['email'], 'password': request.fields['password']}
        res = requests.post(DaemonServer._base_url + '/user/login.json', data=data)
        if res.ok:
            DaemonServer._is_log = True
            DaemonServer._user['_token'] = res.json()['data']
            DaemonServer._user['_email'] = request.fields['email'][0]
        return res

    @staticmethod
    @HTTPRequestHandler.get('/logout')
    def get_user_logout(request):
        """
        Logout
        """
        if not DaemonServer._is_log:
            return DaemonServer._not_login()
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        res = requests.get(DaemonServer._base_url + '/user/logout.json', auth=auth)
        if res.ok:
            DaemonServer._is_log = False
            DaemonServer._token = None
        return res

    @staticmethod
    @HTTPRequestHandler.get('/me')
    def get_user_me(request):
        """
        Informations about the user
        """
        if not DaemonServer._is_log:
            return DaemonServer._not_login()
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        res = requests.get(DaemonServer._base_url + '/user/me.json', auth=auth)
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/')
    def get_plugins(request):
        """
        List of all plugins on the local computer
        """
        res = requests.get(DaemonServer._base_url + '/plugins/list.json')
        list_plugin = res.json()
        list_plugin_installed = DaemonServer._plugin_store.get_plugin_list()
        for plugin in list_plugin:
            plugin['installed'] = 'true' if [p for p in list_plugin_installed if p['name'] == plugin['name']] else 'false'
        res.encoding = 'utf-8'
        data = json.dumps(list_plugin)
        res._content = data.encode('utf-8')
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/:author/:name')
    def get_plugin(request):
        """
        Get a specific plugin

        Url param:
            author -> plugin's author
            name -> plugin's name
        """
        res = requests.get(DaemonServer._base_url + '/plugins/' + request.url_vars['author'] + '/' + request.url_vars['name'] + '/json')
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/:author/:plugin_name/download')
    def get_download_plugin(request):
        """
        Download a plugin

        Url param:
            author -> the plugin's author
            plugin_name -> the plugin's name
        """
        if not DaemonServer._is_log:
            return DaemonServer._not_login()
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        res = requests.get(DaemonServer._base_url + '/plugins/' + request.url_vars['author'] + '/' + request.url_vars['plugin_name'] + '/download', auth=auth)
        if res.ok:
            download_url = res.json()['url']
            download_path = DaemonServer._config.resolve_path_from_root(DaemonServer._download_folder, request.url_vars['plugin_name'])
            DaemonServer.__download_file(download_path, download_url, extension='.zip')
            plugin_path = DaemonServer._config.resolve_path_from_root(DaemonServer._download_folder, request.url_vars['plugin_name'] + '.zip')
            DaemonServer._queue_plugin_manage.put(build_event('install ' + plugin_path))
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/:plugin_name/install')
    def get_install_plugin(request):
        """
        Install a plugin

        Url param:
            plugin_name -> the plugin's name
        """
        plugin_path = DaemonServer._config.get('plugin_folder_download')
        plugin_path = DaemonServer._config.resolve_path_from_root(plugin_path, request.url_vars['plugin_name'] + '.zip')
        res = requests.Response()
        DaemonServer._queue_plugin_manage.put(build_event('install ' + plugin_path))
        res.status_code = 200
        return res

    @staticmethod
    @HTTPRequestHandler.delete('/plugins/:plugin_name')
    def delete_uninstall_plugin(request):
        """
        Uninstall a plugin

        Url param:
            plugin_name -> the plugin's name
        """
        plugin_name = request.url_vars['plugin_name']
        res = requests.Response()
        DaemonServer._queue_plugin_manage.put(build_event('uninstall ' + plugin_name))
        res.status_code = 200
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/:plugin_name/enable')
    def get_enable_plugin(request):
        """
        Enable a plugin

        Url param:
            plugin_name -> the plugin's name
        """
        plugin_name = request.url_vars['plugin_name']
        res = requests.Response()
        DaemonServer._queue_plugin_manage.put(build_event('enable ' + plugin_name))
        res.status_code = 200
        return res

    @staticmethod
    @HTTPRequestHandler.get('/plugins/:plugin_name/disable')
    def get_disable_plugin(request):
        """
        Disable a plugin

        Url param:
            plugin_name -> the plugin's name
        """
        plugin_name = request.url_vars['plugin_name']
        res = requests.Response()
        DaemonServer._queue_plugin_manage.put(build_event('disable ' + plugin_name))
        res.status_code = 200
        return res

    @staticmethod
    def __download_file(file_path, url, extension=''):
        """
        Private method allowing to download a file and save it on specified path

            @param file_path: the local path where the file will be saved
            @type file_path: string
            @param url: the url allownig the download
            @type url: string
            @param extension: extension of the local file
            @type extension: string
        """
        auth = (DaemonServer._user['_email'], DaemonServer._user['_token'])
        res = requests.get(DaemonServer._base_url + url, auth=auth, stream=True)
        with open(file_path + extension, 'wb') as dfile:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    dfile.write(chunk)

    @staticmethod
    def _not_login():
        res = requests.Response()
        res.status_code = 401
        res._content = 'You are not login'.encode('utf-8')
        return res

    def run(self, adress='127.0.0.1', port=8001):
        """
        Start the DaemonServer by listening on the specified adress

            @param adress: adress to listen on
            @type adress: string
            @param port: port to listen on
            @type port: int
        """
        self._httpd = HTTPServer((adress, port), HTTPRequestHandler)
        self._is_running = True
        print('DaemonServer is listening on %s:%d' % (adress, port))
        self._httpd.serve_forever()

    def stop(self):
        """
        Stop the DaemonServer
        """
        print('Stopping {0}...'.format(self.__class__.__name__))
        self._httpd.shutdown()
        self._is_running = False
