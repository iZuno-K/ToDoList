from .models import Board, PipeLine, Card
import datetime

from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

def get_board_list_by_owner(owner):
    return Board.get_list_by_owner(owner=owner)


def get_board_data_by_board_id(board_id):
    """
    :param board_id:
    :return:
    :rtype dict
    """
    board = Board.get_by_id(board_id)
    # get board
    board_data = {
        'board_id': board.id,
        'name': board.name,
        'start_date': board.start_date.strftime("%Y-%m-%d"),
        'end_date': board.end_date.strftime("%Y-%m-%d"),
        'pipe_line_list': []
    }
    # get pipe-lines connected to the board
    for pipe_line in PipeLine.get_list_by_board(board):
        pipe_line_data = {
            'pipe_line_id': pipe_line.id,
            'name': pipe_line.name,
            'card_list': []
        }
        # get cards connected to the pipe-line
        for card in Card.get_list_by_pipe_line(pipe_line):
            pipe_line_data['card_list'].append({
                'card_id': card.id,
                'title': card.title,
                'content': card.content,
                # 'expected_effort': card.expected_effort,
                # 'complete_time': card.complete_time,
            })
        board_data['pipe_line_list'].append(pipe_line_data)

    return board_data


def update_board(board_id, name=None, start_date=None, end_date=None):
    board = Board.get_by_id(board_id)
    if name:
        board.name = name
    if start_date:
        board.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        board.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    board.save()
    return board


def update_card_order(pipe_line_id, card_id_list):
    """
    :param int pipe_line_id:
    :param list card_id_list:
    :return:
    """
    pipe_line = PipeLine.get_by_id(pipe_line_id)
    complete_time = None
    task_state = None
    if pipe_line.name == 'Done':
        complete_time = datetime.datetime.now()
        task_state = "Complete"
    elif pipe_line.name == 'Doing':
        task_state = "Working"
    elif pipe_line.name == "Todo":
        task_state = "Pending"
    for i, card_id in enumerate(card_id_list):
        card = Card.get_by_id(card_id)
        card.order = i
        card.complete_time = complete_time
        if task_state is not None:
            card.task_state = task_state
        card.pipe_line = pipe_line
        card.save()


def add_board(owner, board_name, start_date, end_date):
    """
    :param owner:
    :param board_name:
    :return:
    """
    board = Board.objects.create(
        owner=owner,
        name=board_name,
        start_date=start_date,
        end_date=end_date,
    )
    return board


def add_card(pipe_line_id, card_title):
    pipe_line = PipeLine.get_by_id(pipe_line_id)
    current_count = Card.get_current_card_count_by_pipe_line(pipe_line)
    card = Card(
        title=card_title,
        content=None,
        pipe_line=pipe_line,
        order=current_count + 1,  # 現在のカード数 + 1で末尾になるはず
    )
    card.save()
    return card


def get_card_by_card_id(card_id):
    """
    :param int card_id:
    :return:
    """
    return Card.get_by_id(card_id)


def update_card(card_id, title=None, content=None, expected_effort=None, real_effort=None, complete_time=None, task_state=None):
    """
    :param int card_id:
    :param str title:
    :param str content:
    :param float expected_effort:
    :param float real_effort:
    :param datetime complete_time:
    :param str task_state:
    :return:
    """
    card = Card.get_by_id(card_id)
    if title:
        card.title = title
    if content:
        card.content = content
    if expected_effort:
        card.expected_effort = expected_effort
    if real_effort:
        card.real_effort = real_effort
    if complete_time:
        card.complete_time = complete_time
    if task_state:
        card.task_state = task_state
    card.save()
    return card


def delete_card(card_id):
    card = Card.get_by_id(card_id)
    card.delete()


def add_pipe_line(board_id, pipe_line_name):
    board = Board.get_by_id(board_id)
    current_count = PipeLine.get_current_pipe_line_count_by_board(board)
    return PipeLine.create(board=board, name=pipe_line_name, order=current_count + 1,)


def update_pipe_line(pipe_line_id, name=None):
    """
    :param int pipe_line_id:
    :param str name:
    :return:
    """
    pipe_line = PipeLine.get_by_id(pipe_line_id)
    if name:
        pipe_line.name = name
    pipe_line.save()
    return pipe_line


def delete_pipe_line(pipe_line_id):
    pipe_line = PipeLine.get_by_id(pipe_line_id)
    pipe_line.delete()


# Begin burn down chart ---------------------------------------------
def setPlt(board_id):
    """
    :param list of Task tasks:
    :return:
    """
    board = Board.get_by_id(board_id)
    # output a line graph
    # start date, end date, estimated effort, complete state
    total_effot = 0
    start_date = board.start_date
    end_date = board.end_date
    complete_time = []
    completed_efforts = []

    for p in PipeLine.get_list_by_board(board):
        for c in Card.get_list_by_pipe_line(p):
            total_effot = total_effot + c.expected_effort
            if c.complete_time is not None:
                complete_time.append(c.complete_time)
                completed_efforts.append(c.expected_effort)
    complete_time, completed_efforts = list(zip(*sorted(list(zip(complete_time, completed_efforts)), key=lambda x: x[0])))

    # plot ideal effort
    xticks = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    plt.locator_params(axis='x', nbins=len(xticks))
    fig, ax = plt.subplots()
    ax.plot([start_date.date(), end_date.date()], [total_effot, 0], label="ideal")  # ideal decay of tasks

    # plot actual effort
    efforts_decay = {start_date.date(): total_effot}
    for ct, ce in zip(complete_time, completed_efforts):
        total_effot -= ce
        efforts_decay[ct.date()] = total_effot
    ax.plot(efforts_decay.keys(), efforts_decay.values(), label='actual')  # actual decay of tasks

    # modify layout
    ax.legend()
    ax.set_title(board.name)
    ax.set_ylabel("Effort")
    ax.set_xlabel("day")
    # fig.autofmt_xdate()
    days = mdates.DayLocator(bymonthday=None, interval=1, tz=None)  # display per day
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))


# convert matplotlib
# graph into svg
def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s


def get_svg(board_id):
    setPlt(board_id)  # create the plot
    svg = pltToSvg()  # convert plot to SVG
    plt.cla()  # clean up plt so it can be re-used
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response
# End burn down chart ---------------------------------------------
