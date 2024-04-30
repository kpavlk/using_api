import blueprint as blueprint
import flask
from flask import jsonify, make_response, request

from data import db_session
from data.user import User


blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id',
                                    'surname',
                                    'name',
                                    'age',
                                    'position',
                                    'speciality',
                                    'address',
                                    'email',
                                    'hashed_password',
                                    'modified_date'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify({'users': users.to_dict(
        only=('id',
              'surname',
              'name',
              'age',
              'position',
              'speciality',
              'address',
              'email',
              'hashed_password',
              'modified_date')
    )})


@blueprint.route('/api/users', methods=['POST'])
def add_user():
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    users = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password']
    )
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'id': users.id})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def add_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id).first()
    if not users:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(users)
    users = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password']
    )
    db_sess.add(users)
    db_sess.commit()
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})