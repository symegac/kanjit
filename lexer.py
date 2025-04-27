import re
from typing import Any

KEYWORDS = {
    # definitions and assignments
    '也': "DECL",
    '是': "ASS",
    '之': "BACKASS",
    '自': "SELF",
    '定': "FUNC",
    # functions
    'を': "PARAM",
    '以': "WITH",
    '成': "RETURN",
    '斯': "STARTDEF",
    '了': "ENDSECT",
    # subgroupings
    '有': "EXISTE",
    '無': "NEXISTE",
    'ヶ': "CHILD", 'ヵ': "CHILD", '的': "CHILD",
    '内': "IN", '內': "IN",
    # program flow
    '者': "IF", '者': "IF",
    '。': "ENDCLS",
    '、': "CTXSEP",
    # loops
    '〱': "LOOP",
    '〲': "ENDLOOP",
    '今': "CURR",
    # artihmetic ops
    '足': "ADD",
    '引': "SUB",
    '掛': "MULT",
    '割': "DIV",
    '増': "INCR", '增': "INCR",
    '減': "DECR",
    '半': "HALF",
    '倍': "DOUBLE",
    '乗': "POW", '乘': "POW",
    '根': "SQRT",
    # relational ops
    '当': "EQ", '當': "EQ",
    '超': "GT",
    '未満': "LT", '未滿': "LT",
    '以上': "GE",
    '以下': "LE",
    '中': "INBETW",
    '乃至': "ANDBETW",
    # logical ops
    '及': "AND",
    '又': "OR",
    '若': "MAYBE",
    '': "NOT",
    # directional ops (bitshr, rotr, trimstr, ceasarchar)
    '右': "RIGHT",
    '左': "LEFT",
    # data types
    '字': "CHAR",
    '言': "STR",
    '数': "INT", '數': "INT",
    "分数": "FLOAT",
    # booleans
    '空': "NULL",
    '偽': "FALSE", '僞': "FALSE",
    '真': "TRUE", '眞': "TRUE",
    '零': "ZERO", '〇': "ZERO",
    '壱': "ONE", '壹': "ONE", '弌': "ONE", '一': "ONE",
    # strings
    '「': "LCHAR",
    '」': "RCHAR",
    '『': "LSTR",
    '』': "RSTR",
    '丈': "LEN",
    '伸': "APPEND",
    '切': "SLICE",
    # other
    '々': "REP",
    '分': "DECSEP",
    # '※': "COMMENT"
}
DIGITS = (
    '貳', '貮', '弍', '弐', '二',
    '參', '参', '弎', '三',
    '肆', '亖', '四',
    '伍', '五',
    '陸', '六',
    '漆', '柒', '質', '七',
    '捌', '八',
    '玖', '九',
    '拾', '什', '十',
    '卄', '廿',
    '卅', '丗',
    '卌', 
    '陌', '佰', '百',
    '阡', '仟', '千',
    '萬', '万',
    '億'
)
MULTI = ('以', '未', '乃', '分')

def lex(
    source: str | list[str],
    keywords: dict[str] = KEYWORDS,
    multi: tuple[str] = MULTI
) -> list[tuple[str, Any, tuple[int, int], tuple[int, int]]]:
    tokens = []
    buffer = ''
    last_index = -1
    last_line = 0
    kome = False

    def push(
        val,
        lln, li,
        ln, i,
        bf = False
    ) -> tuple[str, Any, tuple[int, int], tuple[int, int]]:
        return (
            keywords[val] if val in keywords else "IDENT",
            val,
            (lln, li+1),
            (ln, i+1 if not bf else i)
        )

    for line, code in enumerate(source):
        for index, char in enumerate(code):
            if re.match(r"\s", char) is not None:
                if not buffer:
                    last_index += 1
                continue
            # comments
            if kome:
                if char == '※':
                    kome = False
                continue
            if char == '※':
                kome = True
                continue
            # start multichar keyword or digit sequence
            if char in multi:
                # push built-up buffer if exists
                if buffer:
                    tokens.append(push(buffer, last_line, last_index, line, index, bf=True))
                    last_index = index - 1
                    last_line = line
                    buffer = ''
                buffer += char
                continue
            # append monochar keyword
            if char in keywords:
                # push built-up buffer if exists
                if buffer:
                    tokens.append(push(buffer, last_line, last_index, line, index, bf=True))
                    last_index = index - 1
                    last_line = line
                    buffer = ''
                tokens.append(push(char, last_line, last_index, line, index))
                last_index = index
                last_line = line
                continue
            # add if yet unidentified
            buffer += char
            # check if end multichar keyword
            if buffer in keywords:
                tokens.append(push(buffer, last_line, last_index, line, index))
                last_index = index
                last_line = line
                buffer = ''
        if not buffer:
            last_line += 1
            last_index = -1
    if buffer:
        if isinstance(source, str):
            raise SyntaxError(f"第{line+1}列に残りがあった。（{buffer}）")
        raise SyntaxError(f"{line+1}行{last_index+1+1}列に残りがあった。（{buffer}）")
    else:
        *_, end = tokens[-1]
        tokens.append(("EOF", '\0', end, end))
    return tokens

if __name__ == "__main__":
    test = open("test.kj", 'r', encoding="utf-8").readlines()
    print(lex(test))
    ##### 入力 #########################################################################
    #
    # 定   言入 力     データを切以数ゟ若零数迄若入力デ
    #                 ータヶ丈数毎若壱成言出力データ斯。以々〱出自伸
    # 入力データヶ今　〲。成。了。
    #
    ##### 出力 #########################################################################
    #
    # [
    #   ('FUNC', '定', (0, 0), (0, 1)), ('STR', '言', (3, 1), (0, 5)),
    #   ('IDENT', '入力データ', (0, 5), (0, 16)), ('PARAM', 'を', (0, 5), (0, 17)),
    #   ('SLICE', '切', (0, 17), (0, 18)), ('WITH', '以', (0, 18), (0, 19)),
    #   ('INT', '数', (0, 18), (0, 20)), ('IDENT', 'ゟ', (0, 20), (0, 21)),
    #   ('MAYBE', '若', (0, 20), (0, 22)), ('ZERO', '零', (0, 22), (0, 23)),
    #   ('INT', '数', (0, 23), (0, 24)), ('IDENT', '迄', (0, 24), (0, 25)), 
    #   ('MAYBE', '若', (0, 24), (0, 26)), ('IDENT', '入力データ', (0, 26), (1, 22)),
    #   ('CHILD', 'ヶ', (1, 26), (1, 23)), ('LEN', '丈', (1, 23), (1, 24)),
    #   ('INT', '数', (1, 24), (1, 25)), ('IDENT', '毎', (1, 25), (1, 26)),
    #   ('MAYBE', '若', (1, 25), (1, 27)), ('ONE', '壱', (1, 27), (1, 28)),
    #   ('RETURN', '成', (1, 28), (1, 29)), ('STR', '言', (1, 29), (1, 30)),
    #   ('IDENT', '出力データ', (1, 30), (1, 35)), ('STARTDEF', '斯', (1, 30), (1, 36)),
    #   ('ENDCLS', '。', (1, 36), (1, 37)), ('WITH', '以', (1, 37), (1, 38)),
    #   ('REP', '々', (1, 37), (1, 39)), ('LOOP', '〱', (1, 39), (1, 40)),
    #   ('IDENT', '廿弐', (1, 40), (1, 42)), ('INBETW', '中', (1, 42), (1, 43)),
    #   ('IDENT', '參', (1, 43), (1, 44)), ('ANDBETW', '乃至', (1, 44), (1, 46)),
    #   ('IDENT', '佰', (1, 46), (1, 47)), ('IF', '者', (1, 47), (1, 48)),
    #   ('IDENT', '出', (1, 48), (1, 49)), ('SELF', '自', (1, 49), (1, 50)),
    #   ('APPEND', '伸', (1, 50), (1, 51)), ('IDENT', '入力データ', (2, 4), (2, 9)), 
    #   ('CHILD', 'ヶ', (2, 9), (2, 10)), ('CURR', '今', (2, 10), (2, 11)),
    #   ('ENDLOOP', '〲', (2, 12), (2, 13)), ('ENDCLS', '。', (2, 13), (2, 14)),
    #   ('RETURN', '成', (2, 14), (2, 15)), ('ENDCLS', '。', (2, 15), (2, 16)),
    #   ('ENDSECT', '了', (2, 16), (2, 17)), ('ENDCLS', '。', (2, 17), (2, 18)),
    #   ('EOF', '\x00', (2, 18), (2, 18))
    # ]
    #
    ####################################################################################
