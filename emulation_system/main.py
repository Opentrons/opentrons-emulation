from emulation_system.parsers.top_level_parser import TopLevelParser

if __name__ == "__main__":
    TopLevelParser().parse().get_commands().run_commands()
