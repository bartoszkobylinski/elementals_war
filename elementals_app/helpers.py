import json
from django.core import serializers


def serialize_board(board_elements, request):
    board_elements = [element for element in board_elements if element is not None]
    serialized_elements = serializers.serialize('json', board_elements, fields=('id', 'element_type', 'image'))
    serialized_board = json.loads(serialized_elements)

    for element, serialized_element in zip(board_elements, serialized_board):
        serialized_element['fields']['image'] = request.build_absolute_uri(element.image.url)

    serialized_board = [serialized_board[index:index + 3] for index in range(0, 9, 3)]
    return serialized_board
