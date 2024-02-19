from flask import Flask, render_template, request, make_response, redirect
from getter_ankets_result import AutoAnkets
from navigation import *


class WebSite:
    def __init__(self, __name__):
        self.app = Flask(__name__)
        self.setup_routes()
        self.getter_ankets = AutoAnkets()
        self.cookies = ''
        self.data = {'nav': get_nav(self.app),
                     'otvet_auth': '',
                     }


    def setup_routes(self):
        @self.app.errorhandler(404)
        def handle_error(error):
            return render_template('error.html', data=self.data)

        @self.app.route('/', methods=['GET', 'POST'])
        def autorize():
            self.data['otvet_auth'] = ''
            self.data['ankets'] = []
            if request.method == 'GET':
                return render_template('authorize.html', data=self.data)
            elif request.method == 'POST':
                login = request.form['login']
                passwd = request.form['passwd']
                if self.getter_ankets.authorize(login, passwd):
                    resp = make_response(redirect('/selector'))
                    resp.set_cookie('user', 'Authorized')
                    return resp
                else:
                    self.data['otvet_auth'] = 'Авторизация не удалась'
                    return render_template('authorize.html', data=self.data)

        @self.app.route('/selector', methods=['GET', 'POST'])
        def view_ankets():
            if 'user' not in request.cookies:
                self.data['otvet_auth'] = 'Авторизуйтесь!'
                return render_template('authorize.html', data=self.data)
            if request.method == 'GET':
                self.data['otvet_ankets'] = ''
                if 'ankets' not in self.data.keys() or self.data['ankets'] is None:
                    self.data['ankets'] = self.getter_ankets.ankets_view()
                    print(self.data['ankets'])
                return render_template('ankets_selector.html', data=self.data)
            elif request.method == 'POST':
                if 'id:' in request.form:
                    self.data['id_number'] = request.form.get('id')
                    if self.data['id_number'] and self.data['id_number'] in self.data['ankets']:
                        self.getter_ankets.get_anket_from_user(self.data['id_number'])
                    if self.getter_ankets.post_data() == '1':
                        self.data['otvet_ankets'] = 'Данные отправлены'
                        return redirect('/selector')
                    else:
                        self.data['otvet_ankets'] = 'Произошла ошибка'
                        return redirect('/selector')
                else:
                    self.data['otvet_ankets'] = 'Произошла ошибка'
                    return redirect('/selector')



    def run(self, host, port, debug):
        self.app.run(host, port=port, debug=debug)

