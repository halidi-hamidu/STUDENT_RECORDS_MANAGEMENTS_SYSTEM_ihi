import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(3,4))
    plt.title("Relationship between male \n and female student")
    plt.bar(x,y, color=["lightgray"] )
    plt.xlabel("Gender")
    plt.ylabel("Number of students")
    plt.tight_layout()
    graph=get_graph()
    return graph

def get_graph_cnt(x,y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(3,4))
    plt.title("Relationship Between  Male \n and female \n continuous student")
    plt.xlabel("Gender")
    plt.ylabel("Number of Students")
    plt.bar(x, y, color="lightgrey")
    plt.tight_layout()
    graph=get_graph()
    return graph
def get_graph_cmp(x,y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(3,4))
    plt.title("Relationship Between  Male \n and female \n completed student")
    plt.bar(x,y, color=["lightgrey"])
    plt.xlabel("Gender")
    plt.ylabel("Number of students")
    plt.tight_layout()
    graph=get_graph()
    return graph

def get_graph_fnl(x,y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(3,4))
    plt.title("Relationship Between  Male \n and female \n finalist student")
    plt.bar(x,y,color=["lightgrey"])
    plt.xlabel("Gender")
    plt.ylabel("Number of students")
    # plt.figure(figsize=(3,4))
    plt.tight_layout()
    graph=get_graph()
    return graph

def get_graph_pst(x,y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(3,4))
    plt.title("Relationship Between  Male \n and female \n postponed student")
    plt.bar(x,y,color=["lightgrey"])
    plt.xlabel("Gender")
    plt.ylabel("Number of students")
    plt.tight_layout()
    graph=get_graph()
    return graph

def get_graph_phd(x,y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(3,4))
    plt.title("Relationship Between  Male \n and female \n phd student")
    plt.bar(x,y,color=["lightgrey"])
    plt.xlabel("Gender")
    plt.ylabel("Number of students")
    plt.tight_layout()
    graph=get_graph()
    return graph

def get_graph_mst(x, y):
    plt.switch_backend("AGG")
    plt.figure(figsize=(3,4))
    plt.title("Relationship Between  Male \n and female \n Masters student")
    plt.xlabel("gender")
    plt.ylabel("Number of student")
    plt.bar(x, y, color=["lightgrey"])
    plt.tight_layout()
    graph=get_graph()
    return graph
