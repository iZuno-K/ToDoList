from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from modules.kanban import service as kanban_sv


class KanbanConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(KanbanConsumer, self).__init__(*args, **kwargs)
        self.consumer_id = id(self)
        self.user = None
        self.board_id = None
        self.namespace = 'board'
        self.action_map = {
            'update_card_order': self.update_card_order,
            'broadcast_board_data': self.broadcast_board_data,
            'add_pipe_line': self.add_pipe_line,
            'rename_pipe_line': self.rename_pipe_line,
            'delete_pipe_line': self.delete_pipe_line,
        }
        self.room_group_name = None

    def connect(self):
        # check authentication
        if not self.scope['user'].is_authenticated:
            self.close()
            return

        self.user = self.scope['user']
        self.board_id = self.scope['url_route']['kwargs']['board_id']
        self.accept()

        # initialize channel layer
        self.room_group_name = 'board_id_{}'.format(self.board_id)
        # join a group per board
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # return initial data to a client
        self.send_board_data()

    def update_card_order(self, content):
        """
        update card order in a board
        {
            'type': 'update_card_order',
            'pipeLineId': 1,
            'cardIdList': [3, 1]
        }
        :param content:
        :return:
        """
        pipe_line_id = content['pipeLineId']
        card_id_list = content['cardIdList']
        kanban_sv.update_card_order(pipe_line_id, card_id_list)
        # notify the same group (including itself) to call send_board_data
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_board_data',
            }
        )

    def add_pipe_line(self, content):
        """
        add pipe line
        :param content:
        :return:
        """
        board_id = content['boardId']
        pipe_line_name = content['pipeLineName']
        kanban_sv.add_pipe_line(board_id, pipe_line_name)
        self.broadcast_board_data()

    def rename_pipe_line(self, content):
        """
        rename pipe line
        :param content:
        :return:
        """
        pipe_line_id = content['pipeLineId']
        pipe_line_name = content['pipeLineName']
        kanban_sv.update_pipe_line(pipe_line_id, pipe_line_name)
        self.broadcast_board_data()

    def delete_pipe_line(self, content):
        board_id = content['boardId']
        pipe_line_id = content['pipeLineId']
        kanban_sv.delete_pipe_line(pipe_line_id)
        self.broadcast_board_data()

    def receive_json(self, content, **kwargs):
        """
        Typeに応じた処理を呼び出して実行する
        :param dict content:
        :param kwargs:
        :return:
        """
        action = self.action_map.get(content['type'])
        if not action:
            raise Exception('{} is not a valid action_type'.format(content['type']))
        action(content)

    def broadcast_board_data(self, content=None):
        """
        request all clients to re-get board data
        :param content:
        :return:
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_board_data',
            }
        )

    def send_board_data(self, event=None, *args, **kwargs):
        board_data = kanban_sv.get_board_data_by_board_id(self.board_id)
        self.send_json({
            'boardData': board_data,
            'mutation': 'setBoardData',
            'namespace': self.namespace,
        })
        print(board_data)
