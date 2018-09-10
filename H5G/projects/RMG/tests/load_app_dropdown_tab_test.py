
description = 'Try to navigate to the lobby and check the dropdown tab related to paytable for hoot_loot game'

pages = ['partner_game_lobby']


def setup(data):
    pass


def test(data):
    navigate(data.env.rmg_url)
    click(partner_game_lobby.hoot_loot_game_icon)
    wait_for_element_attribute_visible(partner_game_lobby.load_anim, "style", "display: none;")
    wait(3)
    wait_while_text_element_present('VA ULT®')
    wait(2)
    wait_while_text_element_present('Loading up the reels!')
    get_current_window_rect()
    assert_true(verify_element_exist_by_coordinates('rmg_dropdown_btn'))
    click_on_target_area_with_coordinates('rmg_dropdown_btn', partner_game_lobby.base_element, execution.data['element_x_coordinate'], execution.data['element_y_coordinate'])
    wait(5)
    assert_true(verify_element_exist_by_coordinates('paytable_icon'))
    click_on_target_area_with_coordinates('cancle_drop_down_tab', partner_game_lobby.base_element, 455, 8)
    wait(5)


def teardown(data):
    pass
