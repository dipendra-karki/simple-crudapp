from user import User
from db import Db
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import redirect
from werkzeug.routing import Map, Rule
from jinja2 import Environment, FileSystemLoader

class Router(object):
    @staticmethod
    def user_create(req):
        if req.method == 'POST':
            form_data = {key: req.form[key] for key in req.form}
            user = User.create(form_data)

            print(req.url)
            print(form_data)
            print(user)
            return redirect('/')
        if req.method == 'GET':
            return req.render('user.html')
        
    @staticmethod
    def user_update(req):
        if req.method == 'POST':
            form_data = {key:req.form[key] for key in req.form}
            user = User.update(req.params['user_id'], form_data)
            return redirect('/')
        if req.method == 'GET':
            return req.render('user_edit.html', user = User.find_by_id(req.params['user_id']))

    @staticmethod
    def user_remove(req):
        if req.method == 'POST':
            user = User.remove(req.params['user_id'])
            return redirect('/')

    @staticmethod
    def user_edit(req):
        return req.render('user_edit.html', params = req.params, args = req.args)
    
    @staticmethod
    def home_page(req):
        return req.render('home.html', result = User.query()) 

class App(object):
    def __init__(self,config):
        self.config = config
        self.url_map = Map([
    Rule('/', endpoint = Router.home_page),
    Rule('/users', endpoint = Router.user_create),
    Rule('/users/<id>', endpoint = Router.user_update),
    Rule('/users/remove/<id>', endpoint = Router.user_remove),
])
        self.jinja_env = Environment(loader = FileSystemLoader(config['template_path']),
        autoescape=True)

        Db.connect(config['db'])

    def render_template(self, template_name, **kwargs):
        temp = self.jinja_env.get_template(template_name)
        return Response(temp.render(kwargs), mimetype='text/html')

    def dispatch_request(self, req):
        adapter = self.url_map.bind_to_environ(req.environ)
        try:
            endpoint, values = adapter.match()
            req.params = values
            return endpoint(req)
        except NotFound:
            return req.render('404.html')
        except HTTPException as e:
            return e
        

    def wsgi_app(self, environ, start_response):
        req = Request(environ)
        req.render = self.render_template
        res = self.dispatch_request(req)
        return res(environ, start_response)

    def __call__(self, *args):
        return self.wsgi_app(*args)



