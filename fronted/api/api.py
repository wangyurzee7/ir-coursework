import api.backend as backend

def init():
    backend.init()

def search(text,page=1):
    return backend.search(text,page)

def detail(index):
    return backend.detail(index)