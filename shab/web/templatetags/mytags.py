from django import template

register = template.Library()

@register.filter
def mystrip(value):
    res = ""
    skip = 0
    i = 0
    while i < len(value):
        if value[i:i+4] == '<br>':
            i = i+4
            res += '<br/>'
            continue
        if value[i:i+4] == '</p>':
            i = i+4
            res += '</p>'
            continue
        if value[i:i+3] == '</h' :
            i = i + 5
            res += '</p>'
            continue
        if value[i:i+5] == '<br/>':
            i = i+5
            res += '<br/>'
            continue
        if value[i] == '<':
            skip = 1
            if value[i:i+2] == '<p' or value[i:i+2] == '<h':
                res += '<p class="card-text">'
            i += 1
            continue
        if value[i] == '>' and skip:
            i = i+1
            skip = 0
            continue
        if not skip :
            res += value[i]
            i = i+1
            continue
        i += 1
    print(res)
    return res
