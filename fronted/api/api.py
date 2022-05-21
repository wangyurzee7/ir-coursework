import api.backend as backend

def init():
    backend.init()

def search(text,start,count,filter=None):
    return backend.search(text, start = start, count = count, search_filter=filter)

# def detail(index):
#     return backend.detail(index)