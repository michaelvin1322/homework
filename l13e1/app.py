# -*- coding: utf-8 -*-
"""
Занятие №13
Задание №1

Есть гостевая книга. Похожа на статью (Post).
Нет заголовка, есть только текст, и можно подписаться только именем (любым).
Должна содержать модель GuestBookItem
Поле автор
Текст сообщения может быть любой текст длиннее 5 символов
Дата и время, когда опубликована
Должна содержать булевое поле, если захотим удалить конкретную запись
Должна отдавать все записи по адресу “/items” и методу GET в формате JSON
Должна быть возможность создавать записи по адресу “/items” и методу POST
Должна работать валидация при помощи формы модели

Задание №2(посложнее)

Отдавать конкретную запись по адресу “/items/<item_id>” и методу GET в формате JSON
На POST запрос из задания 1 надо отдавать код ответа 201 и адрес созданного объекта ( “/items/<item_id>”) в заголовке
Location и JSON в теле ответа, с созданным объектом (как в пункте 1)
Добавить поле updated_at в модель GuestBookItem, при создании нового объекта проставлять его равным дате и времени
создания
Редактировать конкретную запись по адресу “/items/<item_id>” и методу PATCH, если ресурс с таким id не существует - код
ответа 404, если ресурс отредактирован - JSON в теле ответа, с созданным объектом (как в пункте 1) и обновленным
значение поля updated_at. Передаются только поля, значение которых надо обновить.
Заменять конкретную запись по адресу “/items/<item_id>” и методу PUT, по логике, описанной в пункте 4. Поля передаются
все.
Удалять все записи, при запросе по адресу “/items” и методу PUT c пустым телом запроса, возвращается пустой список
объектов.
Удалять (проставлять поле видимости в False) по адресу “/items/<item_id>” и методу DELETE, если записи с таким id не
существует - код ответа 204

Задание №3(сложное)
Отдавать адресу “/items?page=<page_num>&per_page=<items_count_in_page>” по items_count_in_page на страницу.
Ограничить per_page так, чтобы его нельзя было сделать слишком большим
Дополнительно должен отдаваться заголовок “X-Total-Count" с полным количеством элементов, и заголовок Link. Информация
в нем должна соответствовать https://developer.github.com/v3/#link-header
GET “/items” должен поддерживать сортировку вида - /items&sort=<имя_поля_по_поторому_сортируем>, если перед именем
поля стоит “-”, то сортировку делаем в обратном порядке
GET “/items” должен поддерживать фильтрацию вида - /items&<имя_поля_по_которому_фильтруем>=<значение> и выводить
только записи, удовлетворяющие фильтру
Расширить фильтрацию, теперь перед значением можно добавлять символы “>”, “<”, “>=”, “<=”, означающие, что фильтруем
записи, значение полей которые больше, меньше и т.д. чем переданное для фильтра значение
GET “/items” должен поддерживать список полей, которые отдаются вида - /items&fields=<список полей через запятую>


"""

from flask import Flask, request, render_template, flash, Response
from flask_sqlalchemy import SQLAlchemy, Pagination
from json import dumps
import re

import config as config
from forms import *


app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application
db = SQLAlchemy(app)


@app.route('/items', methods=['GET', 'POST', 'PUT'])
def index():
    from models import GuestBookItem
    if request.method == 'POST':
        print(request.form)
        form = GuestBookForm(request.form)

        if form.validate():
            post = GuestBookItem(**form.data)
            db.session.add(post)
            db.session.commit()

            return 'items/{}'.format(str(post.id)), 201
        else:
            print(str(form.errors))
            return 'Form is not valid! Post was not created. \n' + str(form.errors), 422

    elif request.method == 'GET':
        # posts = GuestBookItem.query.filter(GuestBookItem.is_visible is True).all()
        # # user = User.query.filter(id=posts[0].user_id)
        # # user = posts[0].user
        # # print(posts)
        # return dumps([post.to_dict() for post in posts if post.is_visible is True]), 200
        print(request.base_url)
        # print(request.args)

        items_per_page = request.args.get('items_per_page', default=3, type=int)
        page_num = request.args.get('page', default=1, type=int)
        if items_per_page > 5:
            return 'Too much items per page. Try less', 422

        for parameter, value in request.args.items():
            if parameter in [column.key for column in GuestBookItem.__table__.columns]:
                column = getattr(GuestBookItem, parameter)
                query = GuestBookItem.query.filter(GuestBookItem.is_visible == True).filter(column == value)
                break

            elif value == '':
                pattern = r'(?P<parameter>\w+)(?P<operator>[>|<|>=|<=]{1,2})(?P<value>\w+)'
                parsed_params = re.match(pattern, parameter)
                parameter = parsed_params['parameter']
                operator = parsed_params['operator']
                value = parsed_params['value']

                if parameter not in [column.key for column in GuestBookItem.__table__.columns]:
                    return 'This field does not exist', 404
                column = getattr(GuestBookItem, parameter)

                if operator == '>':
                    query = GuestBookItem.query.filter(GuestBookItem.is_visible == True).filter(column > value)
                elif operator == '<':
                    query = GuestBookItem.query.filter(GuestBookItem.is_visible == True).filter(column < value)
                elif operator == '<=':
                    query = GuestBookItem.query.filter(GuestBookItem.is_visible == True).filter(column <= value)
                elif operator == '>=':
                    query = GuestBookItem.query.filter(GuestBookItem.is_visible == True).filter(column >= value)
                break

            elif parameter == 'sort_by':
                query = GuestBookItem.query.filter(GuestBookItem.is_visible == True).order_by(getattr(GuestBookItem, value))
                break

            else:
                query = GuestBookItem.query.filter(GuestBookItem.is_visible is True)

        posts = query.paginate(page=page_num,
                               per_page=items_per_page,
                               error_out=True,
                               )

        links = build_link_header(posts, request.base_url)

        return Response(response=dumps([post.to_dict() for post in posts.items]),
                        status=200,
                        headers={'X-Total-Count': len(posts.items),
                                 'Link': links,
                                 },
                        )

    elif request.method == 'PUT':
        GuestBookItem.query.update({'is_visible': False})
        db.session.commit()
        posts = GuestBookItem.query.filter(GuestBookItem.is_visible is False).all()
        return dumps(posts)


@app.route('/items/<int:item_id>', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def get_item(item_id):
    from models import GuestBookItem
#    post = GuestBookItem.query.filter(GuestBookItem.id == item_id).get_or_404(item_id)
    post = GuestBookItem.query.get_or_404(item_id)

    if request.method == 'GET':
        return dumps(post.to_dict()), 200

    elif request.method == 'PATCH':
        form = UpdateAllForm(request.form)
        # print(form.data)
        if form.validate():
            GuestBookItem.query.filter(GuestBookItem.id == item_id).update({k: v for k, v
                                                                            in form.data.items() if v != ''})
            db.session.commit()
        return dumps(post.to_dict()), 200

    elif request.method == 'PUT':
        form = UpdateAllForm(request.form)
        if form.validate():
            GuestBookItem.query.filter(GuestBookItem.id == item_id).update(form.data)
            db.session.commit()
            return dumps(post.to_dict()), 200

    elif request.method == 'DELETE':
        post.is_visible = False
        db.session.add(post)
        db.session.commit()
        return 204


# @app.route('/items?sort_by=<имя_поля_по_поторому_сортируем>', methods=['GET', ])
# def sort():
#     pass
#
#
# @app.route('/items&<имя_поля_по_которому_фильтруем>=<значение>', methods=['GET', ])
# def filter():
#     pass
# @app.route('/items&fields=<список полей через запятую>', methods=['GET', ])


def build_link_header(query, base_url):
    links = ''
    if query.has_prev:
        links += '<{}?per_page={}&page={}>; rel="prev"'.format(base_url, query.per_page, query.prev_num)
    if query.has_next:
        if links:
            links += ', '
        links += '<{}?per_page={}&page={}>; rel="next"'.format(base_url, query.per_page, query.next_num)
    else:
        return dict(Link=links)


def populate_db():
    print('Creating default user')
    # Creating new ones:
    posts = [
        GuestBookItem(user_name='Ivan', content='some comment or post.... '),
        GuestBookItem(user_name='Usr_1', content='In orci lorem, faucibus luctus urna ut, cursus sollicitudin arcu.'),
        GuestBookItem(user_name='Usr_2', content='Donec posuere leo non consectetur fringilla. Aliquam eu quam velit.'),
        GuestBookItem(user_name='Usr_3', content='Duis eget ipsum eu ligula molestie posuere vitae vitae purus.'),
        GuestBookItem(user_name='Usr_4', content='Quisque diam massa, consequat eu suscipit in, ultricies nec ante.'),
        GuestBookItem(user_name='Usr_5', content='In ligula quam, convallis viverra auctor egestas, feugiat ac ante.'),
        GuestBookItem(user_name='Usr_6', content='Interdum et malesuada fames ac ante ipsum primis in faucibus.'),
        GuestBookItem(user_name='Usr_7', content='Mauris lacus ipsum, mattis ut ante nec, commodo efficitur elit.'),
        GuestBookItem(user_name='Usr_1', content='Nulla justo neque, iaculis eget malesuada vitae, maximus quis eros.'),
        GuestBookItem(user_name='Usr_1', content='Maecenas id orci lacinia orci gravida blandit. Vivamus in nisl.'),
        GuestBookItem(user_name='Usr_2', content='Fusce laoreet erat ac egestas efficitur. Morbi varius sagittis purus.'),
          ]
    for p in posts:
        db.session.add(p)
    db.session.commit()  # note


if __name__ == '__main__':
    from models import *
    db.create_all()

    if GuestBookItem.query.count() == 0:
        populate_db()

    users = GuestBookItem.query.all()
#    print(list(map(str, GuestBookItem)))

    # Running app:
    app.run()
