from .models import Board as Boards

def boards_context_processor(request):
    boards = Boards.objects.all()
    return {'boards': boards}