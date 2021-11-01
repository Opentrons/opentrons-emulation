import sys
from parsers.top_level import top_level_parser

if __name__ == "__main__":
    parser = top_level_parser()
    args = parser.parse_args(sys.argv[1:])
    print(args.func(args))
