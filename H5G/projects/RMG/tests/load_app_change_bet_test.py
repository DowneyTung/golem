
description = 'Try to navigate to the lobby and change the bet option for hoot_loot game'

pages = ['partner_game_lobby']


def setup(data):
    pass


def test(data):
    navigate("http://partnerdemo.high5games.com/")
    # get_element_location(partner_game_lobby.hoot_loot_game_icon)
    # click_on_target_area_with_offset('spin_button', partner_game_lobby.hoot_loot_game_icon, 100, 200)
    click(partner_game_lobby.hoot_loot_game_icon)
    wait(70)
    get_current_window_rect()
    get_element_location(partner_game_lobby.base_element)
    click_on_target_area_with_offset('dropdown_tab', partner_game_lobby.base_element, 200, 20)
    wait(5)
    click_on_target_area_with_offset('cancle_drop_down_tab', partner_game_lobby.base_element, -300, 20)
    wait(5)


def teardown(data):
    pass
