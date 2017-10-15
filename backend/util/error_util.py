import re


def error_extraction(content):
    errs = []
    lines=content.split("\n")
    for temp in lines:
        temp=temp.strip()
        temps=temp.split(">")
        if len(temps)>1:
            line=temp[2:]
        else:
            line=temp
        pattern=re.compile(r"^(.*): (fatal |)error (\w*): (.*)$")
        match=pattern.search(line)
        if match:
            position=match.group(1)
            code=match.group(3)
            message=match.group(4)
            err = {'line': line, 'position': position, 'code': code, 'message': message}
            errs.append(err)
            #print(position+"\t"+code+"\t"+message)
    return errs