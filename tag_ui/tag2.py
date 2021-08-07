import rpa as r

def do_web_auto(search_data):
    r.init()
    r.url('https://www.google.com')
    r.click('.gLFyf.gsfi')

    r.type('.gLFyf.gsfi', f'{search_data}[enter]')
    #r.type("//*[@name='q']', 'decentralization[enter]")
    #print(r.read('result-stats'))
    r.snap('page', 'results.png')
    res = r.read('result-stats')
    r.close()
    return res

if __name__ == '__main__':
    search = 'Python'
    result = do_web_auto(search)
    print('-'*20)
    print(result)
