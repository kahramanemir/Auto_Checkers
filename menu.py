import dearpygui.dearpygui as dpg

def show_ai_menu():
    dpg.create_context()
    dpg.create_viewport(title='AI Configuration', width=800, height=800)

    config = {
        "minimax_depth": 3,
        "mcts_simulations": 1000,
        "num_games": 1
    }

    def start_callback():
        config["minimax_depth"] = dpg.get_value("minimax")
        config["mcts_simulations"] = dpg.get_value("mcts")
        config["num_games"] = dpg.get_value("games")
        dpg.stop_dearpygui()

    with dpg.window(label="Configure AI Parameters", width=800, height=800, pos=(20, 0)):
        dpg.add_text("Set AI Parameters", bullet=True)
        dpg.add_slider_int(label="Minimax Depth", default_value=3, min_value=1, max_value=5, tag="minimax", width=400)
        dpg.add_slider_int(label="MCTS Simulations", default_value=1000, min_value=100, max_value=2000, tag="mcts", width=400)
        dpg.add_slider_int(label="Number of Games", default_value=1, min_value=1, max_value=9, tag="games", width=400)
        dpg.add_spacing(count=2)
        dpg.add_button(label="Start", callback=start_callback, width=100)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    return config