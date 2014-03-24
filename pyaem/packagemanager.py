import bagofrequests as bag
import handlers
import json
import pycurl

class PackageManager(object):


	def __init__(self, url, **kwargs):

		def _handler_ok(response, **kwargs):

			data    = json.loads(response['body'])
			message = data['msg']

			result = {
				'status' : 'success' if data['success'] == True else 'failure',
				'message': message
			}

			return result

		self.url      = url
		self.kwargs   = kwargs
		self.handlers = {
			200: _handler_ok,
			401: handlers.auth_fail,
			405: handlers.method_not_allowed
		}


	def create_package(self, group_name, package_name, package_version, **kwargs):

		params   = {
			'cmd'           : 'create',
			'groupName'     : group_name,
			'packageName'   : package_name,
			'packageVersion': package_version,
			'_charset_'     : 'utf-8'
		}
		method   = 'post'
		url      = '{0}/crx/packmgr/service/.json/etc/packages/{1}'.format(self.url, package_name)
		params   = dict(params.items() + kwargs.items())
		handlers = self.handlers
		opts     = self.kwargs

		return bag.request(method, url, params, handlers, **opts)


	def update_package(self, group_name, package_name, package_version, **kwargs):

		params   = {
			'groupName'  : group_name,
			'packageName': package_name,
			'version'    : package_version,
			'path'       : '/etc/packages/{0}/{1}-{2}.zip'.format(group_name, package_name, package_version),
			'_charset_'  : 'utf-8'
		}
		method   = 'get'
		url      = '{0}/crx/packmgr/update.jsp'.format(self.url)
		params   = dict(params.items() + kwargs.items())
		handlers = self.handlers
		opts     = self.kwargs

		return bag.request(method, url, params, handlers, **opts)


	def build_package(self, group_name, package_name, package_version, **kwargs):

		params   = {
			'cmd': 'build'
		}
		method   = 'post'
		url      = '{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}-{3}.zip'.format(self.url, group_name, package_name, package_version)
		params   = dict(params.items() + kwargs.items())
		handlers = self.handlers
		opts     = self.kwargs

		return bag.request(method, url, params, handlers, **opts)


	def download_package(self, group_name, package_name, package_version, **kwargs):

		def _handler_ok(response, **kwargs):

			result = {
				'status' : 'success',
				'message': '{0} was successfully downloaded'.format(kwargs['file_name'])
			}

			return result

		_handlers = {
			200: _handler_ok
		}
		opts      = {
			'file_name': '{0}-{1}.zip'.format(package_name, package_version)
		}
		method    = 'get'
		url       = '{0}/etc/packages/{1}/{2}-{3}.zip'.format(self.url, group_name, package_name, package_version)
		params    = kwargs
		_handlers = dict(self.handlers.items() + _handlers.items())
		opts      = dict(self.kwargs.items() + opts.items())

		return bag.download_file(url, params, _handlers, **opts)


	def upload_package(self, group_name, package_name, package_version, **kwargs):

		def _handler_ok(response, **kwargs):

			data = json.loads(response['body'])

			result = {
				'status' : 'success' if data['success'] == True else 'failure',
				'message': data['msg']
			}

			return result

		file_name = '{0}-{1}.zip'.format(package_name, package_version)
		params    = {
			'cmd'    : 'upload',
			'package': (pycurl.FORM_FILE, file_name)
		}
		_handlers = {
			200: _handler_ok
		}
		opts      = {
			'file_name': file_name
		}
		url       = '{0}/crx/packmgr/service/.json/'.format(self.url)
		params    = dict(params.items() + kwargs.items())
		_handlers = dict(self.handlers.items() + _handlers.items())
		opts      = dict(self.kwargs.items() + opts.items())

		return bag.upload_file(url, params, _handlers, **opts)


	def install_package(self, group_name, package_name, package_version, **kwargs):

		params   = {
			'cmd': 'install'
		}
		method   = 'post'
		url      = '{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}-{3}.zip'.format(self.url, group_name, package_name, package_version)
		params   = dict(params.items() + kwargs.items())
		handlers = self.handlers
		opts     = self.kwargs

		return bag.request(method, url, params, handlers, **opts)


	def replicate_package(self, group_name, package_name, package_version, **kwargs):

		params   = {
			'cmd': 'replicate'
		}
		method   = 'post'
		url      = '{0}/crx/packmgr/service/.json/etc/packages/{1}/{2}-{3}.zip'.format(self.url, group_name, package_name, package_version)
		params   = dict(params.items() + kwargs.items())
		handlers = self.handlers
		opts     = self.kwargs

		return bag.request(method, url, params, handlers, **opts)