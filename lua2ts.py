#encoding: UTF-8
import re
import sys

with open(sys.argv[1] + ".lua", "r") as f:
    file = f.read()
    className = re.findall(r"\b(.*) = \{\}\nlocal this = \1", file)
    if className:
        print "export class", className[0]

        # 检查是否为Unity转cc
        isU2cc = '-u2cc' in sys.argv

        className = className[0]
        # 块注释
        result = re.sub(r"--\[\[((.*\n)*?.*?)\]\]", "/*\\1*/", file)
        # 类
        result = re.sub(r"\b(.*) = \{\}\nlocal this = \1\n", "export class " + className + "{\n", result)
        result = re.sub(r"" + className + "\.", "this.", result)        
        # 局部变量
        result = re.sub(r"\tlocal(.*=)", "\tlet\\1", result)
        # 成员变量
        result = re.sub(r"\blocal m_(.*)", "private _\\1", result)
        result = re.sub(r"([^private])m_(\w+)", "\\1this._\\2", result)
        if isU2cc:
            result = re.sub(r"_transform", "_root", result)
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
        # 函数 
        result = re.sub(r"\bfunction " + className + r"\.(.*)", "\\1 {", result)
        result = re.sub(r"\bfunction this\.(.*)", "\\1 {", result)
        result = re.sub(r"(\bfunction\(.*\))(.*)\n", "\\1{\\2\n", result)
        result = re.sub(r"end(,|\)|\s.*)", "}\\1", result)
        result = re.sub(r"New(\(\) {)", "constructor\\1", result)
        result = re.sub(r"string\.gsub\((.*?), (.*?), (.*)\)", "\\1.replace(\\2, \\3)", result)
        if isU2cc:
            result = re.sub(r":GetComponent", ".getComponent", result)
            result = re.sub(r"'UILabel'", "cc.Label", result)
            result = re.sub(r"\.text = ", ".string = ", result)
            result = re.sub(r"'UIScrollView'", "cc.ScrollView", result)
            result = re.sub(r"\.gameObject", "", result)
            result = re.sub(r"\.transform", "", result)
            result = re.sub(r":Find\(\"(.*)\"", ":Find('\\1'",result)
            result = re.sub(r"(\w+(\.\w+)*?):Find\(('\w+(\/\w+)+')\)", "cc.find(\\3, \\1)", result)
            result = re.sub(r"(\w+(\.\w+)*?):Find\(('.*')\)", "\\1.getChildByName(\\3)", result)
            result = re.sub(r":SetActive\((.*)\)", ".active = \\1", result)
            result = re.sub(r"\.activeSelf", ".active", result)
            result = re.sub(r":GetChild\((.*)\)", ".children[\\1]", result)
            # 自用
            result = re.sub(r"Util.ClearChild\((.*)\)", "\\1.removeAllChildren()", result)
            result = re.sub(r"NGUITools.AddChild", "Utils.addChild", result)
            result = re.sub(r"\w(.*):AddClick\((.*),(.*this\.(\w+))\)", 'Utils.addClickEvent(\\2, this.node, \'' + className + '\', \'\\4\')', result)
            result = re.sub(r"\btonumber\(", "Number(", result)
            result = re.sub(r"\btostring\(", "String(", result)
            result = re.sub(r"LuaTableManager\.AddTable", "DataTable.loadTable", result)
            result = re.sub(r"\blog(\(.*\))", "console.log\\1", result)
            result = re.sub(r"\bUI_SystemPrompt.Open_Prompt_\d", "cc.vv.alert", result)

        # nil 转 null
        result = re.sub(r"nil", "null", result)
        
        with open(sys.argv[1] + ".ts", "w") as f:
            f.write(result)