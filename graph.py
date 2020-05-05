import os

import matplotlib.pyplot as plt

from fetch import getData


def plot(axes, x, y, color=None, ylabel=None, title=None):
    """ To plot the graph"""
    # Plot the inputs x,y in the provided color
    if color is None:
        axes.plot(x, y)
    else:
        axes.plot(x, y, color=color)

    # Set title and labels for axes
    axes.set(ylabel=ylabel,
             title=title)

    # Set major locator for x-axis
    axes.xaxis.set_major_locator(plt.MaxNLocator(10))

    # Rotate date labels automatically
    plt.gcf().autofmt_xdate()


def create_graph(country, case_type, color_scheme):
    """ To plot a graph of one of the case_type {confirmed, recovered, death} for a country"""
    url = os.path.join('historical', country)
    data = getData(url)['timeline']
    cases = data[case_type]
    x_axis = [*cases]
    y_axis = [*cases.values()]

    title = "Total No. of Covid-19 cases- " + case_type
    fig, axes = plt.subplots(figsize=(8, 6))
    plot(axes, x_axis, y_axis, color_scheme, "No. of Cases", title=title)
    # Set legend
    plt.legend([case_type])
    # Save fig as graph.png to send it to the user
    fig.savefig('graph.png')


def create_vs_graph(country, case_types):
    """ To plot a graph between two of the case_type {confirmed, recovered, death} for a country"""
    url = os.path.join('historical', country)
    params = {'lastdays': 60}
    data = getData(url, params=params)['timeline']
    fig, axes = plt.subplots(figsize=(8, 6))
    title = "New {} vs New {}".format(case_types[0], case_types[1])
    for case_type in case_types:
        cases = data[case_type]
        x_axis = [*cases]
        cases = [*cases.values()]
        new_cases = cases[:1] + [cases[i + 1] - cases[i]
                                 for i in range(len(cases)-1)]
        y_axis = new_cases
        plot(axes, x_axis, y_axis, ylabel="No. of Cases", title=title)
    # Set legend
    plt.legend(case_types)
    # Save fig as graph.png to send it to the user
    fig.savefig('graph.png')
