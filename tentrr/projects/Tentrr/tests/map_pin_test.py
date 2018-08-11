description = 'make sure the map pin is working'

pages = ['search_page']

def setup(data):
	pass

def test(data):
    navigate(data.url)
    click(search_page.map_pin_pioneer_farm)
    wait(3)
    print(get_current_url())
    assert_true(data.expected_text in get_current_url())

def teardown(data):
    pass