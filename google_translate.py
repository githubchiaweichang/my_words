import requests
import json

TKK = (lambda a=561666268, b=1526272306:
       str(406398) + '.' + str(a + b))()


def tk(a):
    # 獲取google翻譯內容的tk值
    # a:要翻譯的內容,以字串指定
    # 注意:要翻譯的內容只能是英文,即只能是包含ASCII碼的英文字串
    TKK = (lambda a=561666268, b=1526272306: str(406398) + '.' + str(a + b))()

    def b(a, b):
        for d in range(0, len(b) - 2, 3):
            c = b[d + 2]
            c = ord(c[0]) - 87 if 'a' <= c else int(c)
            c = a >> c if '+' == b[d + 1] else a << c
            a = a + c & 4294967295if '+' == b[d] else a ^ c
        return a

    e = TKK.split('.')
    h = int(e[0]) or 0
    g = []
    d = 0
    f = 0
    while f < len(a):
        c = ord(a[f])
        if 128 > c:
            g.insert(d, c)
            d += 1
            print(g)
        else:
            if 2048 > c:
                g[d] = c >> 6 | 192
                d += 1
            else:
                if (55296 == (c & 64512)) and (f + 1 < len(a)) and (56320 == (ord(a[f + 1]) & 64512)):
                    f += 1
                    c = 65536 + ((c & 1023) << 10) + (ord(a[f]) & 1023)
                    g[d] = c >> 18 | 240
                    d += 1
                    g[d] = c >> 12 & 63 | 128
                    d += 1
                else:
                    g[d] = c >> 12 | 224
                    d += 1
                    g[d] = c >> 6 & 63 | 128
                    d += 1
                    g[d] = c & 63 | 128
                    d += 1
        f += 1
        # print(c, f)print(c)
    a = h
    for d in range(len(g)):
        a += g[d]
        a = b(a, '+-a^+6')
        print(a)

    a = b(a, '+-3^+b+-f')
    a ^= int(e[1]) or 0
    if 0 > a:
        a = (a & 2147483647) + 2147483648

    a %= 1E6

    return str(int(a)) + '.' + str(int(a) ^ h)

# function tk(a) {var TKK = ((function() {var a = 561666268;var b = 1526272306;return 406398 + '.' + (a + b); })()); function b(a, b) { for (var d = 0; d < b.length - 2; d += 3) { var c = b.charAt(d + 2), c = 'a' <= c ? c.charCodeAt(0) - 87 : Number(c), c = '+' == b.charAt(d + 1) ? a >>> c : a << c; a = '+' == b.charAt(d) ? a + c &; 4294967295 : a ^ c } return a } for (var e = TKK.split('.'), h = Number(e[0]) || 0, g = [], d = 0, f = 0; f < a.length; f++) {var c = a.charCodeAt(f);128 > c ? g[d++] = c : (2048 > c ? g[d++] = c >> 6 | 192 : (55296 == (c &; 64512) &;&; f + 1 < a.length &;&; 56320 == (a.charCodeAt(f + 1) &; 64512) ? (c = 65536 + ((c &; 1023) << 10) + (a.charCodeAt(++f) &; 1023), g[d++] = c >> 18 | 240, g[d++] = c >> 12 &; 63 | 128) : g[d++] = c >> 12 | 224, g[d++] = c >> 6 &; 63 | 128), g[d++] = c &; 63 | 128)}a = h;for (d = 0; d < g.length; d++) a += g[d], a = b(a, '+-a^+6');a = b(a, '+-3^+b+-f');a ^= Number(e[1]) || 0;0 > a &;&; (a = (a &; 2147483647) + 2147483648);a %= 1E6;return a.toString() + '.' + (a ^ h) }
def main():
    # content = input('請翻譯內容:')
    content = "spirit"
    if content == '':
        return None  # 未輸入內容直接退出
    else:
        content_tk = tk(content)  # 獲取tk值
        if tk != 320089.150370:
            raise AssertionError(content_tk, "Fail")

        content_url_template = 'https://translate.google.cn/translate_a/single?client=webapp&;sl=auto&;tl=zh-CN&;hl=zh-CN&;dt=at&;dt=bd&;dt=ex&;dt=ld&;dt=md&;dt=qca&;dt=rw&;dt=rm&;dt=ss&;dt=t&;source=bh&;ssel=0&;tsel=0&;kc=1&;tk={tk}&;q={q}'
        content_url = content_url_template.format(tk='{}'.format(content_tk), q='{}'.format(content))
        # 根據待翻譯content和tk值拼湊URL
        response = requests.get(content_url)
        # 根據URL獲取翻譯資料
        json_data = response.text
        print(json_data)
        data = json.loads(json_data)
    return data


if __name__ == '__main__':
    print(main())
