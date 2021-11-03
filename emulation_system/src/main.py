from parsers.top_level_parser import TopLevelParser

if __name__ == "__main__":
    commands = TopLevelParser().parse()
    commands.run_commands()
