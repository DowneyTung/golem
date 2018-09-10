
description = 'Try to navigate to the lobby and change the bet option for Gypsy game'

pages = ['partner_game_lobby']


def setup(data):
    pass


def test(data):
    navigate(data.env.rmg_url)
    click(partner_game_lobby.gypsy_game_icon)
    wait_for_element_attribute_visible(partner_game_lobby.load_anim, "style", "display: none;")
    wait(3)
    wait_while_text_element_present('VA ULT®')
    wait(2)
    wait_while_text_element_present('Loading up the reels!')
    wait(2)
    get_current_window_rect()
    get_element_location(partner_game_lobby.base_element)
    assert_true(verify_element_exist_by_coordinates('change_bet_option_btn'))
    click_on_target_area_with_coordinates('change_bet_option_btn', partner_game_lobby.base_element, execution.data['element_x_coordinate'], execution.data['element_y_coordinate'])
    wait(2)
    click_on_target_area_with_coordinates('choose_one_type_of_bet', partner_game_lobby.base_element, 312, 339)
    wait(5)


def teardown(data):
    pass
