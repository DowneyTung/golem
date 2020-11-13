from golem import execution
description = 'Try to navigate to the lobby and click on the spin button.'

pages = ['partner_game_lobby']


def setup(data):
    pass


def test(data):
    store("game_url", data.env.partial_game_url + "gameID=" + data.game_id + "&userId=tester" + str(random_with_N_digits(9)))
    navigate(execution.data['game_url'])
    wait(20)
    wait_for_element_attribute_visible(partner_game_lobby.load_anim, "style", "display: none;")
    wait(10)
    wait_for_element_attribute_visible(partner_game_lobby.spin_btn, "style", "display: block;") 
    reload_games(partner_game_lobby.spin_btn, "style", "display: block;")
    click(partner_game_lobby.spin_btn)
    wait(3)
    click(partner_game_lobby.spin_btn)
    wait(3)
    click(partner_game_lobby.spin_btn)

    wait(10)


def teardown(data):
    pass
