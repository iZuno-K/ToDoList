from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View

from modules.kanban import service as kanban_sv
import json


@method_decorator(csrf_exempt, name='dispatch')
class BoardListApi(View):

    def get(self, request):
        """
        return kanban list
        """
        board_list = []
        for board in kanban_sv.get_board_list_by_owner(request.user):
            board_list.append({
                'id': board.id,
                'name': board.name,
            })
        return JsonResponse({
            'board_list': board_list,
        })

    def post(self, request):
        """
        create new board
        :param request:
        :return:
        """
        data = json.loads(request.body)
        board_name = data.get('boardName')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        board = kanban_sv.add_board(
            owner=request.user,
            board_name=board_name,
            start_date=start_date,
            end_date=end_date,
        )
        return JsonResponse({
            'board_data': {
                'id': board.id,
                'name': board.name
            }
        })


@method_decorator(csrf_exempt, name='dispatch')
class CardApi(View):
    def post(self, request):
        """
        Add a new card
        """
        data = json.loads(request.body)
        card_title = data.get('cardTitle')
        pipe_line_id = data.get('pipeLineId')

        card = kanban_sv.add_card(
            pipe_line_id=pipe_line_id,
            card_title=card_title
        )
        return JsonResponse({
            'card_data': {
                'id': card.id,
                'name': card.title,
            }
        })


@method_decorator(csrf_exempt, name='dispatch')
class CardGetApi(View):
    def get(self, _, board_id, card_id):
        """
        get card
        """
        card = kanban_sv.get_card_by_card_id(card_id)

        return JsonResponse({
            'card_data': {
                'title': card.title,
                'content': card.content,
                'updated_at': card.updated_at,
                'expected_effort': card.expected_effort,
                'real_effort': card.real_effort,
                'complete_time': card.complete_time,
                'task_state': card.task_state,
            }
        })

    def patch(self, request, board_id, card_id):
        """
        update content of card
        """
        data = json.loads(request.body)
        title = data.get('title')
        content = data.get('content')
        expected_effort = data.get('expectedEffort')
        real_effort = data.get('realEffort')
        complete_time = data.get('completeTime')
        task_state = data.get('taskState')
        card = kanban_sv.update_card(card_id=card_id, title=title, content=content, expected_effort=expected_effort,
                                     real_effort=real_effort, complete_time=complete_time, task_state=task_state)

        return JsonResponse({
            'card_data': {
                'title': card.title,
                'content': card.content,
                'updated_at': card.updated_at,
                'expected_effort': card.expected_effort,
                'real_effort': card.real_effort,
                'complete_time': card.complete_time,
                'task_state': card.task_state,
            }
        })

    def delete(self, _, board_id, card_id):
        """
        delete card
        """
        kanban_sv.delete_card(card_id=card_id)

        return JsonResponse({
            'success': True
        })


@method_decorator(csrf_exempt, name='dispatch')
class BurnDownChartApi(View):
    def get(self, request, board_id):
        svg = kanban_sv.get_svg(board_id)
        return svg

    # def post(self, request):
    #     """
    #     plot burn down chart
    #     """
    #     data = json.loads(request.body)
    #     boardId = data.get('boardId')
    #
    #     return JsonResponse({
    #         'boardId': boardId,
    #     })

@method_decorator(csrf_exempt, name='dispatch')
class BoardUpdateApi(View):
    def patch(self, request, board_id):
        """
        update content of card
        """
        data = json.loads(request.body)
        name = data.get('name')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        board = kanban_sv.update_board(board_id=board_id, name=name, start_date=start_date, end_date=end_date)

        return JsonResponse({
            'board_data': {
                'name': board.name,
                'start_date': board.start_date.strftime('%Y-%m-%d'),
                'end_date': board.end_date.strftime('%Y-%m-%d'),
            }
        })
