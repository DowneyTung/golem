
description = 'Try to navigate to the lobby and click on the spin button for Triple Monkey game'

pages = ['partner_game_lobby']


def setup(data):
    pass


def test(data):
    navigate(data.env.rmg_url)
    click(partner_game_lobby.triple_monkey_game_icon)
    wait_for_element_attribute_visible(partner_game_lobby.load_anim, "style", "display: none;")
    wait(15)
    get_current_window_rect()
    get_element_location(partner_game_lobby.base_element)
    assert_true(capture_crop_compare_image('rmg_spin_btn', 647, 445, 40, 70))
    click_on_target_area_with_offset('spin_button', partner_game_lobby.base_element, 120, 464)
    wait(5)
    assert_true(capture_crop_compare_image('rmg_spin_btn', 647, 445, 40, 70))


def teardown(data):
    pass
