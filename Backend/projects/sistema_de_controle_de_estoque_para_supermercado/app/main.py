
from fastapi import FastAPI

app = FastAPI(title='Sistema de Estoque')

@app.get('/health')
def health():
    return {'status': 'ok'}
