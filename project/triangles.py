from pygraphblas import Matrix, BOOL, INT64
from pygraphblas.descriptor import T0


def triangles_by_vertex__count(graph: Matrix):
    """Calculates number of triangles for each vertex of undirected graph that contain the vertex

    :param graph: graph as Matrix
    :return: count of triangles that contain vertex i as List
    """
    check_matrix(graph)
    res = graph.mxm(graph, cast=INT64, mask=graph).reduce_vector(desc=T0)
    fill = 0
    if res.nvals != 0:
        fill = res
    res = res.dense(INT64, res.size, fill)
    return [count // 2 for count in res.vals]


def sandia_triangles_count(graph: Matrix):
    """Calculates total number of triangles in an undirected graph with Sandia algorithm

    :param graph: graph as Matrix
    :return: count of triangles
    """
    check_matrix(graph)
    upper_t = graph.triu()
    return sum(upper_t.mxm(upper_t, cast=INT64, mask=upper_t).vals)


def cohen_triangles_count(graph: Matrix):
    """Calculates total number of triangles in an undirected graph with Cohen algorithm

    :param graph: graph as Matrix
    :return: count of triangles
    """
    check_matrix(graph)
    lower_t = graph.tril()
    upper_t = graph.triu()
    return sum(lower_t.mxm(upper_t, cast=INT64, mask=graph).vals) // 2


def check_matrix(m: Matrix):
    if not (m.square and m.type == BOOL and m.iseq(m.transpose())):
        raise Exception(
            "Given matrix is not an adjacency matrix of an undirected graph!"
        )
