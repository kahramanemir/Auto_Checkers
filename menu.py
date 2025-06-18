import dearpygui.dearpygui as dpg

def show_ai_menu():
    dpg.create_context()
    dpg.create_viewport(title='AI Configuration', width=800, height=800)

    config = {
        "white_alg": "ABP",
        "black_alg": "MCTS",
        "white_abp_depth": 3,
        "black_abp_depth": 3,
        "white_mcts_sims": 500,
        "black_mcts_sims": 500,
        "num_games": 1
    }

    def start_callback():
        config["white_alg"] = dpg.get_value("white_alg")
        config["black_alg"] = dpg.get_value("black_alg")
        config["white_abp_depth"] = dpg.get_value("white_abp_depth")
        config["black_abp_depth"] = dpg.get_value("black_abp_depth")
        config["white_mcts_sims"] = dpg.get_value("white_mcts_sims")
        config["black_mcts_sims"] = dpg.get_value("black_mcts_sims")
        config["num_games"] = dpg.get_value("num_games")
        dpg.stop_dearpygui()

    def toggle_white_params(sender, app_data):
        alg = app_data
        dpg.configure_item("white_abp_depth", show=(alg == "ABP"))
        dpg.configure_item("white_mcts_sims", show=(alg == "MCTS"))

    def toggle_black_params(sender, app_data):
        alg = app_data
        dpg.configure_item("black_abp_depth", show=(alg == "ABP"))
        dpg.configure_item("black_mcts_sims", show=(alg == "MCTS"))

    with dpg.window(label="Configure AI Parameters", width=780, height=760):
        dpg.add_text("Note: Increasing depth or simulations may significantly slow down the game.\nPlease keep values reasonable.", color=(255, 100, 100))
        dpg.add_spacer(height=10)

        dpg.add_text("Set AI Parameters")

        dpg.add_combo(["ABP", "MCTS", "Random"], label="White AI", default_value="ABP", tag="white_alg", callback=toggle_white_params)
        dpg.add_slider_int(label="White ABP Depth", default_value=3, min_value=1, max_value=5, tag="white_abp_depth")
        dpg.add_slider_int(label="White MCTS Simulations", default_value=500, min_value=100, max_value=2000, tag="white_mcts_sims", show=False)

        dpg.add_combo(["ABP", "MCTS", "Random"], label="Black AI", default_value="MCTS", tag="black_alg", callback=toggle_black_params)
        dpg.add_slider_int(label="Black ABP Depth", default_value=3, min_value=1, max_value=5, tag="black_abp_depth", show=False)
        dpg.add_slider_int(label="Black MCTS Simulations", default_value=500, min_value=100, max_value=2000, tag="black_mcts_sims")

        dpg.add_slider_int(label="Number of Games", default_value=1, min_value=1, max_value=9, tag="num_games")
        dpg.add_button(label="Start", callback=start_callback)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    return config