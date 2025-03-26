import cv2
import numpy as np


def graph_show(graph):
    buff = graph.get_graph().draw_mermaid_png()
    img = np.frombuffer(buff, dtype=np.uint8)
    cv_img = cv2.imdecode(img, 1)
    cv2.imshow("graph", cv_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()