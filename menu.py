import dearpygui.dearpygui as dpg

def show_ai_menu():
    dpg.create_context()
    dpg.create_viewport(title='AI Configuration', width=800, height=800)

    config = {
        "white_type": "Minimax",
        "white_depth": 3,
        "white_simulations": 500,
        "black_type": "MCTS",
        "black_depth": 3,
        "black_simulations": 500,
        "num_games": 1
    }

    def start_callback():
        config["white_type"] = dpg.get_value("white_type")
        config["black_type"] = dpg.get_value("black_type")

        if config["white_type"] == "Minimax":
            config["white_depth"] = dpg.get_value("white_depth")
        else:
            config["white_simulations"] = dpg.get_value("white_sim")

        if config["black_type"] == "Minimax":
            config["black_depth"] = dpg.get_value("black_depth")
        else:
            config["black_simulations"] = dpg.get_value("black_sim")

        config["num_games"] = dpg.get_value("games")
        dpg.stop_dearpygui()

    def update_white_params(sender, app_data):
        dpg.configure_item("white_depth", show=app_data == "Minimax")
        dpg.configure_item("white_sim", show=app_data == "MCTS")

    def update_black_params(sender, app_data):
        dpg.configure_item("black_depth", show=app_data == "Minimax")
        dpg.configure_item("black_sim", show=app_data == "MCTS")

    with dpg.window(label="Configure AI Players", width=760, height=760, pos=(20, 20)):
        dpg.add_text("White Player Configuration", color=(200, 255, 200))
        dpg.add_combo(["Minimax", "MCTS"], label="White Algorithm", default_value="Minimax", tag="white_type", callback=update_white_params)
        dpg.add_slider_int(label="White Minimax Depth", default_value=3, min_value=1, max_value=6, tag="white_depth")
        dpg.add_slider_int(label="White MCTS Simulations", default_value=500, min_value=100, max_value=2000, tag="white_sim", show=False)

        dpg.add_spacing(count=2)
        dpg.add_text("Black Player Configuration", color=(255, 200, 200))
        dpg.add_combo(["Minimax", "MCTS"], label="Black Algorithm", default_value="MCTS", tag="black_type", callback=update_black_params)
        dpg.add_slider_int(label="Black Minimax Depth", default_value=3, min_value=1, max_value=6, tag="black_depth", show=False)
        dpg.add_slider_int(label="Black MCTS Simulations", default_value=500, min_value=100, max_value=2000, tag="black_sim")

        dpg.add_spacing(count=2)
        dpg.add_slider_int(label="Number of Games", default_value=1, min_value=1, max_value=4, tag="games")
        dpg.add_button(label="Start", callback=start_callback)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    return config