import rich
from lark import Lark

with open("grammar.lark", 'r', encoding="utf-8") as grammar:
    parser = Lark(grammar, parser="lalr")

if __name__ == "__main__":
    test = ''.join(open("test.kj", 'r', encoding="utf-8").readlines())
    # Tokenizer/lexer
    lex = parser.lex(test)
    # Parser
    par = parser.parse(test)

    # List of tokens
    print(list(lex))
    # Two different ways to print AST
    print(par.pretty())
    rich.print(par)
