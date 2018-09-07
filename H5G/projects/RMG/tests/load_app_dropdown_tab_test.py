
description = 'Try to navigate to the lobby and check the dropdown tab related to paytable for hoot_loot game'

pages = ['partner_game_lobby']


def setup(data):
    pass


def test(data):
    navigate(data.env.rmg_url)
    click(partner_game_lobby.hoot_loot_game_icon)
    wait_for_element_attribute_visible(partner_game_lobby.load_anim, "style", "display: none;")
    wait(15)
    get_current_window_rect()
    get_element_location(partner_game_lobby.base_element)
    capture_crop_compare_image('rmg_spin_btn', 647, 445, 40, 70)
    click_on_target_area_with_offset('dropdown_tab', partner_game_lobby.base_element, 150, 15)
    wait(5)
    click_on_target_area_with_offset('cancle_drop_down_tab', partner_game_lobby.base_element, -150, 15)
    wait(1)
    capture_crop_compare_image('rmg_spin_btn', 647, 445, 40, 70)
    wait(5)


def teardown(data):
    pass
