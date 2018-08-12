description = 'navigate to searched result'

pages = ['search_page']

def setup(data):
	pass

def test(data):
    navigate(data.url)
    send_keys(search_page.search_input, data.search_value)
    click(search_page.search_button)
    verify_text_in_element(search_page.first_result_header, data.expected_value)
    window_number_gen(0, "first_windown")
    click(search_page.first_search_result)
    wait(3)
    window_number_gen(1, "second_window")
    switch_window(execution.data['second_window'])
    assert_true(data.expected_text in get_current_title())

def teardown(data):
    pass