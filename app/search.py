from app.models import Line

def search_query(line):
    lines = []
    print(Line.get(0))
    for line in Line.query.\
        filter(Line.flavor.like('%{}%'.format(line))):
            lines.append(line)
    return lines
        
    
