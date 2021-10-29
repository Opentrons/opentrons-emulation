from parsers.top_level import main_parser

if __name__ == "__main__":
    parser = main_parser()
    args = parser.parse_args()
    print(args.func(args))
