from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from sonic import SearchClient

app = FastAPI()

# 判断查询数据是否为中文
def is_chinese_string(string):
    for char in string:
        if not ('\u4e00' <= char <= '\u9fff'):
            return False
    return True

@app.get("/")
async def read_search():
    return HTMLResponse(content=open("search.html",encoding="utf-8").read(), status_code=200)


@app.get("/get_suggestions")
async def get_suggetions(term: str = Query(default=None)):
    with SearchClient("10.0.1.65", 1491, "SecretPassword") as querycl:
        print(querycl.ping())
        suggestions = querycl.suggest("wiki", "articles", term)
        return suggestions

@app.get("/search")
async def search(term: str = Query(default=None)):
    with SearchClient("10.0.1.65", 1491, "SecretPassword") as querycl:
        print(querycl.ping())
        if is_chinese_string(term):
            response = querycl.query("wiki", "articles", term, lang='cmn')
        else:
            response = querycl.query("wiki", "articles", term)
        print(response)
        return response
