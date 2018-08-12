description = 'make sure the map pin is working'

pages = ['search_page']

def setup(data):
	pass

def test(data):
    navigate(data.url)
    window_number_gen(0, "first_windown")
    click(search_page.map_pin_pioneer_farm)
    window_number_gen(1, "second_window")
    switch_window(execution.data['second_window'])
    wait(3)
    assert_true(data.expected_text in get_current_title())

def teardown(data):
    pass