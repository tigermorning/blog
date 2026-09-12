from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class Ticket(TypedDict):          # ① State: 전표에 어떤 칸이 있는지 선언
    order: str      # 손님이 적은 주문 원문
    dishes: list    # 정리된 메뉴 목록
    count: int      # 접시 수
    log: str        # 어느 조리대를 거쳤는지

def take_order(state: Ticket):    # ② Node: 전표를 받아 바꾼 칸만 돌려준다
    dishes = [d.strip() for d in state["order"].split(",") if d.strip()]
    return {"dishes": dishes, "log": state["log"] + " > 접수"}

def count_dishes(state: Ticket):
    return {"count": len(state["dishes"]), "log": state["log"] + " > 집계"}

builder = StateGraph(Ticket)
builder.add_node("take_order", take_order)      # 이름이 곧 엣지의 주소
builder.add_node("count_dishes", count_dishes)
builder.add_edge(START, "count_dishes")
builder.add_edge("count_dishes", "take_order")
builder.add_edge("take_order", END)
graph = builder.compile()

print(graph.invoke({"order": " 김치찌개,  계란말이 ,공기밥 ", "log": "시작"}))