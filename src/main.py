from .parser import Parser

def main():
    main_parser = Parser()
    print(main_parser.parse_file('data/sample_logs/log01.txt'))
    print(main_parser.get_entries())

main()