from flask import Flask
from flask import abort, jsonify, request
from handlers.response_objects import Item, User, Trade, Error
from handlers.db_handler import DBHandler
from handlers.user_handler import UserHandler
from handlers.item_handler import ItemHandler
from handlers.trade_handler import TradeHandler
from handlers.search_handler import SearchHandler

# create the app instance
app = Flask(__name__)

# create the MySQL database handler instance
db_handler = DBHandler(app)
user_handler = UserHandler(db_handler)
item_handler = ItemHandler(db_handler)
trade_handler = TradeHandler(db_handler)
search_handler = SearchHandler(db_handler)

# these are all the mock API end points.
# ---------------------------------------------------------------------
# -------------------------- MOCK -------------------------------------
# ---------------------------------------------------------------------

# ------ USER ------
# get_user
# create_user
# update_user
# delete_user
# get_wishlist
# set_wishlist
# get_inventory
# * helper methods

@app.route('/mock/api/get_user/<int:user_id>', methods=['GET'])
def mock_get_user(user_id):
	if user_id > 9000:
		return jsonify(error='mock_get_user: OH NO, USERS OVER 9000 DON\'T EXIST!')

	# just a dummy value for now
	return jsonify(user=make_dummy_user(user_id), error='')

@app.route('/mock/api/create_user', methods=['POST'])
def mock_create_user():
	json = request.get_json()

	# check for malformed json request
	if not is_valid_json(['email'], json):
		abort(400, 'mock_create_user: invalid POST data')

	return jsonify(user_id='9000', error='')

@app.route('/mock/api/update_user', methods=['PUT'])
def mock_update_user():
	json = request.get_json()

	# check for malformed json request
	if not is_valid_json(['user_id', 'name', 'zipcode', 'avatar'], json):
		abort(400, 'mock_update_user: invalid PUT data')
	
	return jsonify(error='')

@app.route('/mock/api/delete_user/<int:user_id>', methods=['DELETE'])
def mock_delete_user(user_id):
	if user_id > 9000:
		return jsonify(error='mock_delete_user: OH NO, USERS OVER 9000 DON\'T EXIST!')

	return jsonify(error='')

@app.route('/mock/api/get_wishlist/<int:user_id>', methods=['GET'])
def mock_get_wishlist(user_id):
	if user_id > 9000:
		return jsonify(error='mock_delete_user: OH NO, USERS OVER 9000 DON\'T EXIST!')

	return jsonify(
		wishlist=[
			'cool_stuff',
			'awful_stuff',
			'a_banana_for_scale'],
		error=''
		)
	
@app.route('/mock/api/set_wishlist', methods=['PUT'])
def mock_set_wishlist():
	json = request.get_json()
	
	if not is_valid_json(['user_id', 'wishlist'], json):
		abort(400, 'mock_set_wishlist: invalid PUT data')
	
	return jsonify(error='')
	
@app.route('/mock/api/get_inventory/<int:user_id>', methods=['GET'])
def mock_get_inventory(user_id):
	if user_id > 9000:
		return jsonify(error='mock_get_inventory: OH NO, USERS OVER 9000 DON\'T EXIST!')

	return jsonify(
		items=[
			make_dummy_item(1),
			make_dummy_item(2),
			make_dummy_item(3)],
		error=''
		)

# helper method
def make_dummy_user(user_id):
	return {
		'user_id': user_id,
		'zipcode': 12345,
		'name': 'test_user_' + str(user_id),
		'email': 'test_email_' + str(user_id) + '@email.com',
		'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Hausziege_04.jpg/220px-Hausziege_04.jpg',
		'wishlist': ['test_tag_1', 'test_tag_2'],
		'inventory': [
			make_dummy_item(1, user_id),
			make_dummy_item(2, user_id)]
		}

# ------ ITEM ------
# get_item
# create_item
# update_item
# delete_item
# * helper methods

@app.route('/mock/api/get_item/<int:item_id>', methods=['GET'])
def mock_get_item(item_id):
	if item_id > 9000:
		return jsonify(error='mock_get_item: OH NO, ITEM IDS OVER 9000 DON\'T EXIST!')

	return jsonify(item=make_dummy_item(item_id), error='')


@app.route('/mock/api/create_item', methods=['POST'])
def mock_create_item():
	json = request.get_json()

	if not is_valid_json(['user_id', 'title', 'description', 'tags', 'item_image'], json):
		abort(400, 'mock_create_item: invalid POST data')

	return jsonify(item_id=100, item_image_url='i.imgur.com/ibsZi5R.png', error='')

@app.route('/mock/api/update_item', methods=['PUT'])
def mock_update_item():
	json = request.get_json()

	if not is_valid_json(['item_id'], json):
		abort(400, 'mock_update_item: invalid PUT data')

	return jsonify(error='')

@app.route('/mock/api/delete_item/<int:item_id>', methods=['DELETE'])
def mock_delete_item(item_id):
	if item_id > 9000:
		return jsonify(error='mock_delete_item: OH NO, ITEM IDS OVER 9000 DON\'T EXIST!')

	return jsonify(error='')

# helper method
def make_dummy_item(item_id, user_id=1234):
	return {
		'item_id': item_id,
		'user_id': user_id,
		'name': 'test_item_' + str(item_id),
		'image_url': 'http://cdn.newsapi.com.au/image/v1/26a2476dc344c27ac3e7670c9df711b2?width=650',
		'tags': ['test_item_tag_1', 'test_item_tag_2']
		}

# ------ TRADE ------ 
# get_trade
# get_trades
# start_trade
# accept_trade
# deny_trade
# * helper methods

@app.route('/mock/api/get_trade/<int:trade_id>', methods=['GET'])
def mock_get_trade(trade_id):
	if trade_id > 9000:
		return jsonify(error='mock_get_trade: OH NO, TRADE IDS OVER 9000 DON\'T EXIST!')
	
	return jsonify(trade=make_dummy_trade(trade_id), error='')

@app.route('/mock/api/get_trades/<int:user_id>', methods=['GET'])
def mock_get_trades(user_id):
	if user_id > 9000:
		return jsonify(error='mock_get_trades: OH NO, USERS OVER 9000 DON\'T EXIST!')
	
	return jsonify(
		trades=[
			make_dummy_trade(1),
			make_dummy_trade(2),
			make_dummy_trade(3)],
		error=''
		)

@app.route('/mock/api/start_trade', methods=['POST'])
def mock_start_trade():
	json = request.get_json()

	if not is_valid_json(['initiator_id', 'recipient_id' ,'offered_item_ids' ,'requested_item_ids'], json):
		abort(400, 'mock_start_trade: invalid POST data')

	return jsonify(trade_id=100, error='')

@app.route('/mock/api/accept_trade', methods=['PUT'])
def mock_accept_trade():
	json = request.get_json()

	if not is_valid_json(['user_id', 'trade_id'], json):
		abort(400, 'mock_accept_trade: invalid PUT data')

	return jsonify(error='')

@app.route('/mock/api/deny_trade', methods=['PUT'])
def mock_deny_trade():
	json = request.get_json()

	if not is_valid_json(['user_id', 'trade_id'], json):
		abort(400, 'mock_deny_trade: invalid PUT data')

	return jsonify(error='')

# helper method
def make_dummy_trade(trade_id):
	return {
		'trade_id': trade_id,
		'initiator_id': 1000,
		'recipient_id': 2000,
		'requested_item_ids': [1, 2, 3],
		'offered_item_ids': [1000, 1001],
		'status': '',
	}


# ---------------------------------------------------------------------
# --------------------------- API -------------------------------------
# ---------------------------------------------------------------------

@app.route('/api/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
	# check for malformed request
	if user_id <= 0:
		abort(400, 'get_user: only accepts positive user IDs')
	
	return user_handler.get_user(user_id)

@app.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	# check for malformed request
	if user_id <= 0:
		abort(400, 'delete_user: only accepts positive user IDs')
	
	return user_handler.delete_user(user_id)

@app.route('/api/create_user', methods=['POST'])
def create_user():
	json = request.get_json()
	# check for malformed json request
	if not is_valid_json(['email'], json):
		abort(400, 'create_user: invalid POST data')
	return user_handler.create_user(json)

@app.route('/api/update_user', methods=['PUT'])
def update_user():
	json = request.get_json()

	# check for malformed json request
	if not is_valid_json(['user_id'], json):
		abort(400, 'update_user: invalid PUT data')
	
	return user_handler.update_user(json)

#----------------------------------------------------------------#

@app.route('/api/get_item/<int:item_id>', methods=['GET'])
def get_item(item_id):
	return item_handler.get_item(item_id)

@app.route('/api/create_item', methods=['POST'])
def create_item():
	json = request.get_json()
	if not is_valid_json(('user_id', 'title', 'description', 'tags', 'item_image'), json):
		abort(400, 'create_item: invalid PUT data')
	return item_handler.create_item(json)

@app.route('/api/update_item', methods=['PUT'])
def update_item():
	json = request.get_json()
	if not is_valid_json_update('item_id', ('title', 'description', 'tags', 'item_image'), json):
		abort(400, 'update_item: invalid PUT data')
	return item_handler.update_item(json)

@app.route('/api/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
	return item_handler.delete_item(item_id)

@app.route('/api/get_all_items', methods=['GET']) # basically for testing
def get_all_items():
	return item_handler.get_all_items()

@app.route('/api/get_inventory/<int:user_id>', methods=['GET'])
def get_inventory(user_id):
	return item_handler.get_inventory(user_id)
	
#----------------------------------------------------------------#

@app.route('/api/set_wishlist', methods=['PUT']) # TODO won't work until wishlistitem table is up
def set_wishlist():
	json = request.get_json()
	if not is_valid_json(('user_id', 'wishlist'), json):
		abort(400, 'set_wishlist: invalid PUT data')
	return item_handler.set_wishlist(json)

@app.route('/api/get_wishlist/<int:user_id>', methods=['GET'])
def get_wishlist(user_id):
	return item_handler.get_wishlist(user_id)
	
#----------------------------------------------------------------#

@app.route('/api/get_trade/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
	return trade_handler.get_trade(trade_id)

@app.route('/api/get_trades/<int:user_id>', methods=['GET'])
def get_trades(user_id):
	return trade_handler.get_trades(user_id)

@app.route('/api/start_trade', methods=['POST'])
def start_trade():
	json = request.get_json()

	if not is_valid_json(['initiator_id', 'recipient_id' ,'offered_item_ids' ,'requested_item_ids'], json):
		abort(400, 'start_trade: invalid POST data')

	return trade_handler.start_trade(json)

@app.route('/api/accept_trade', methods=['PUT'])
def accept_trade():
	json = request.get_json()

	if not is_valid_json(['user_id', 'trade_id'], json):
		abort(400, 'accept_trade: invalid PUT data')

	return trade_handler.accept_trade(json)

@app.route('/api/deny_trade', methods=['PUT'])
def deny_trade():
	json = request.get_json()

	if not is_valid_json(['user_id', 'trade_id'], json):
		abort(400, 'deny_trade: invalid PUT data')

	return trade_handler.deny_trade(json)
	
# ONLY FOR TESTING DO NOT USE
@app.route('/api/delete_trade/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
	return trade_handler.delete_trade(trade_id)
#----------------------------------------------------------------#

@app.route('/api/get_users_within_radius', methods=['GET', 'POST'])
def get_users_within_radius():
	json = request.get_json()
	zipcode = json['zipcode']
	radius = json['radius']

	
	if zipcode is None or radius is None:
		abort(400, 'get_users_within_radius: invalid GET arguments')
	
	result = search_handler.get_users_within_radius(zipcode, radius)
	
	# check if there was an error
	if result is None:
		return jsonify(error="invalid zipcode")
		
		
	return result


#------------------------------ utility -------------------------------#

def is_valid_json(expected_fields, json):
	# check that there is json data
	if not json:
		return False
	
	# validate the expected fields exist
	for field in expected_fields:
		if field not in json:
			return False
	
	return True

# check that there is an id field and at least one other valid field
def is_valid_json_update(required_field, expected_fields, json):
	if not json:
		return False

	if required_field not in json:
		return False

	flag = False 
	for field in expected_fields:
		if field in json:
			flag = True
	return flag

if __name__ == '__main__':
	app.run()
