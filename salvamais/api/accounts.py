from . import api


@api.route('/test', methods=['GET'])
def test_endpoint():
    return 'Test!!!', 200
