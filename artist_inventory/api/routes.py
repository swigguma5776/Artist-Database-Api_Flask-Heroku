from flask import Blueprint, request, jsonify 
from artist_inventory.helpers import token_required
from artist_inventory.models import db, User, Artist, ArtistSchema, artist_schema, artists_schema 

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required 
def getdata(current_user_token):
    return {'some': 'value'}

# Create Artist Endpoint
@api.route('/artists', methods = ['POST'])
@token_required
def create_artist(current_user_token):
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    nationality = request.json['nationality']
    art_period = request.json['art_period']
    style = request.json['style']
    most_famous_work = request.json['most_famous_work']
    scandals = request.json['scandals']
    user_token = current_user_token.token 

    print(f"BIG TESTER: {current_user_token.token}")

    artist = Artist(first_name, last_name, nationality, art_period, style, most_famous_work, scandals, user_token=user_token)

    db.session.add(artist)
    db.session.commit() 

    response = artist_schema.dump(artist)
    return jsonify(response)

# Retrieve All Artist Endpoint
@api.route('/artists', methods = ['GET'])
@token_required
def get_artists(current_user_token):
    owner = current_user_token.token
    artists = Artist.query.filter_by(user_token = owner).all()
    response = artists_schema.dump(artists)
    return jsonify(response)


# Retrieve One Artist Endpoint
@api.route('/artists/<id>', methods = ['GET'])
@token_required
def get_artist(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        artist = Artist.query.get(id)
        response = artist_schema.dump(artist)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401 


# Update Artist Endpoint
@api.route('/artists/<id>', methods = ['POST', 'PUT'])
@token_required
def update_artist(current_user_token, id):
    artist = Artist.query.get(id)

    artist.first_name = request.json['first_name']
    artist.last_name = request.json['last_name']
    artist.nationality = request.json['nationality']
    artist.art_period = request.json['art_period']
    artist.style = request.json['style']
    artist.most_famous_work = request.json['most_famous_work']
    artist.scandals = request.json['scandals']
    artist.user_token = current_user_token.token 

    db.session.commit()
    response = artist_schema.dump(artist)
    return jsonify(response)

# Delete Artist Endpoint
@api.route('/artists/<id>', methods = ['DELETE'])
@token_required
def delete_artist(current_user_token, id):
    artist = Artist.query.get(id)
    db.session.delete(artist)
    db.session.commit()
    response = artist_schema.dump(artist)
    return jsonify(response)