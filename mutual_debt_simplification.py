from data_structures import Graph


# # # Input # # #
def debt_list_to_graph(debt_list: list, name_translation: dict = None) -> Graph:
    """
    Make a graph from a list of debts
    :param debt_list: A list of 3 element lists or tuples with (str:debtor, str:collector, float:debt_value)
    :param name_translation: Optional: A dictionary that maps full length names to the names used in the debt_list
    :return: the debt_graph described by the debt_list
    """
    debt_graph = Graph()
    for debt in debt_list:
        debtor = name_translation[debt[0]] if name_translation else debt[0]
        collector = name_translation[debt[1]] if name_translation else debt[1]
        value = debt[2]

        debt_graph.edge(debtor, collector, value)

    return debt_graph


# # # Business Logic # # #
def simplify_debt_graph(debt_graph: Graph) -> Graph:
    """
    Simplifies the graph to the minimum required transaction
    :param debt_graph:
    :return: the simplified graph
    """
    collectors, debtors = collectors_and_debtors(debt_graph)
    return graph_from_collectors_and_debtors(collectors, debtors)


def collectors_and_debtors(debt_graph: Graph) -> (dict, dict):
    """
    Get the dicts of collectors (owed more money than they owe) and debtors (owe more money than they are owed)
    :param debt_graph:
    :return: dict of collectors, dict of debtors
    """

    collectors, debtors = {}, {}
    for participant in debt_graph:
        total_owed = sum([value for collector, value in debt_graph.get_node_edges(participant)])  # add the positive debt
        total_owed -= sum([value for collector, value in debt_graph.get_node_reverse_edges(participant)])  # subtract the negative debt (credit)
        
        if total_owed > 0:  # positive debt, is a debtor
            debtors[participant] = total_owed
        elif total_owed < 0:  # negative debt, is a collector
            collectors[participant] = -total_owed  # invert the sign since it's now a credit instead of a debt

    return collectors, debtors


def graph_from_collectors_and_debtors(collectors: dict, debtors: dict) -> Graph:
    """
    Create the simplified graph from the information contained in the collector and debtor dicts
    :param collectors:
    :param debtors:
    :return: the simplified graph
    """
    debt_graph = Graph()
    for collector in sorted(collectors):  # from biggest collector (negative numbers, no need to reverse)
        for debtor in sorted(debtors, reverse=True):  # from biggest debtor
            credit, debt = collectors[collector], debtors[debtor]

            if credit != 0 and debt != 0:
                transaction_value = min(credit, debt)
                debt_graph.edge(debtor, collector, transaction_value)

                if credit >= debt:
                    collectors[collector] += debt
                    debtors[debtor] = 0
                else:
                    collectors[collector] = 0
                    debtors[debtor] -= credit

    return debt_graph


# # # Output # # #
def draw_graph(debt_graph: Graph, graph_name: str, open_file: bool = True) -> None:
    """
    Draw the graph in a pdf file or print it to the console (if graphviz isn't installed)
    :param open_file:
    :param graph_name:
    :param debt_graph:
    """
    print('%s: ' % graph_name, debt_graph)
    try:
        from graphviz import Digraph
    except ImportError:
        Digraph = None

    if Digraph:
        viz = Digraph(graph_name)
        viz.node_attr.update(color='orangered', shape='box', style='rounded', penwidth='2')
        for participant in debt_graph:
            if debt_graph.get_node_edges(participant):
                viz.node(participant)
                for debt in debt_graph.get_node_edges(participant):
                    viz.edge(participant, debt[0], xlabel=str(debt[1]))
        
        viz.view() if open_file else viz.render()
        print('Render saved as %s.gv.pdf' % graph_name)
    else:
        print('(Please install graphviz for a much cleaner visualization of the graph)')


if __name__ == '__main__':
    import json
    debts = json.load(open('debt_list', 'r'))

    initial_debt_graph = debt_list_to_graph(debts['debt_list'], debts['names'])
    draw_graph(initial_debt_graph, 'Initial_Mutual_Debt', open_file=False)
    simplified_debt_graph = simplify_debt_graph(initial_debt_graph)
    draw_graph(simplified_debt_graph, 'Simplified_Mutual_Debt')
