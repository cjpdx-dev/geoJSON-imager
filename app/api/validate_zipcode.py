from app.api import bp

@bp.route('/validate_zipcode/<int:zipcode>', methods=['GET'])
def find_zip(zipcode):
	pass