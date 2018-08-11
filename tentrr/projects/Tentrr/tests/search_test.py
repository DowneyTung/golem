description = 'Search an campsite in tentrr'

pages = ['search_page']

def setup(data):
	pass

def test(data):
    navigate(data.url)
    send_keys(search_page.search_input, data.search_value)
    click(search_page.search_button)
    verify_text_in_element(search_page.first_result_header, data.expected_value)

def teardown(data):
    close()