#encoding: UTF-8
import re
import sys

with open(sys.argv[1] + ".lua", "r") as f:
    file = f.read()
    className = re.findall(r"\b(.*) = \{\}\nlocal this = \1", file)
    if className:
        print "export class", className[0]
        className = className[0]
        # 块注释
        result = re.sub(r"--\[\[((.*\n)*?.*?)\]\]", "/*\\1*/", file)
        # 类
        result = re.sub(r"\b(.*) = \{\}\nlocal this = \1\n", "export class " + className + "{", result)
        result = re.sub(r"" + className + "\.", "this.", result)        
        # 局部变量
        result = re.sub(r"\tlocal(.*=)", "\tlet\\1", result)
        # 成员变量
        result = re.sub(r"\blocal (.*)", "private \\1", result)
        # 整体缩进
        result = re.sub(r"\n", "\n\t", result)
        # 类结束
        result = result + "\n}"
        # 符号
        result = re.sub(r"\n\t*\band\b", "&&", result)
        result = re.sub(r"\sand\s", " && ", result)
        result = re.sub(r"\n\t*\bor\b", "||", result)
        result = re.sub(r"\sor\s", " || ", result)
        result = re.sub(r"\bnot ", "!", result)        
        result = re.sub(r"\.\.", "+", result)
        result = re.sub(r"~=", "!=", result)
        result = re.sub(r"#((\w|\.)*)", "\\1.length", result)
        # for if
        result = re.sub(r"\bfor (\w)( = \d),\s*(.*)\s*do", "for (let \\1\\2; \\1 < \\3; ++\\1) {", result)
        result = re.sub(r"\bif((.*\n)*?.*?)then", "if (\\1) {", result)
        result = re.sub(r"\belseif(.*)then", "} else if (\\1) {", result)
        result = re.sub(r"\belse(\t*)\n", "} else {\n", result)
        result = re.sub(r"--(.*\n)", "//\\1", result)
        result = re.sub(r"\bend\s*\n", "}\n", result)
        # 函数 方法名改为小写开头
        def functionName(m):
            first = m.group(1)
            first = first.lower()
            return first + m.group(2) + " {"
        result = re.sub(r"\bfunction " + className + ".(\w)(.*)", functionName, result)
        result = re.sub(r"\bfunction this.(\w)(.*)", functionName, result)
        result = re.sub(r"(\bfunction\(.*\))(.*)\n", "\\1{\\2\n", result)
        result = re.sub(r"end(,|\)|\s.*)", "}\\1", result)
        result = re.sub(r"new(\(\) {)", "constructor\\1", result)
        # nil 转 null
        result = re.sub(r"nil", "null", result)
        
        with open(sys.argv[1] + ".ts", "w") as f:
            f.write(result)