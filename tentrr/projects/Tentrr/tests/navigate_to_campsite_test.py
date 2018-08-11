description = 'navigate to searched result'

pages = ['search_page']

def setup(data):
	pass

def test(data):
    navigate(data.url)
    send_keys(search_page.search_input, data.search_value)
    click(search_page.search_button)
    verify_text_in_element(search_page.first_result_header, data.expected_value)
    click(search_page.first_search_result)
    wait(3)
    assert_true(data.expected_text in get_current_url())

def teardown(data):
    pass