# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_async_tasks.models import Problem, ProblemType
from api_async_tasks.serializers import ProblemSerializer
from api_async_tasks.tasks import *


class ProblemsViewSet(ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if serializer.data['problem_type'] == ProblemType.prime_factoring.value:
            prime_factoring.apply_async((serializer.data['argument'],), task_id=serializer.data['task_id'])
        elif serializer.data['problem_type'] == ProblemType.integrate.value:
            integration.apply_async((serializer.data['argument'],), task_id=serializer.data['task_id'])

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
