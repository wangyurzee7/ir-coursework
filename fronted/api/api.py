import api.backend as backend

def init():
    backend.init()

def search(text,start,count):
    return backend.search(text, start = start, count = count)

# def detail(index):
#     return backend.detail(index)