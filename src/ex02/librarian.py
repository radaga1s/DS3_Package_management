#!bs_pt_venv/bin/python3

import os

def main():
    venv = os.environ.get('VIRTUAL_ENV')
    if not venv:
        raise Exception('Virtual environment not runnig')
    if not venv.endswith('/ex02/bs_pt_venv'):
        raise Exception('The script was called from the wrong env')
    with open('tempreq.txt', 'w') as req:
        req.write('bs4\nPyTest\nrequests\n')
    os.system('pip install -r tempreq.txt')
    os.remove('tempreq.txt')
    os.system('pip freeze > requirements.txt')
    with open('requirements.txt', 'r') as out:
        print(out.read(), end='')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
