from rest_framework import serializers

from api_async_tasks.models import Problem, ProblemType


class ProblemSerializer(serializers.ModelSerializer):
    task_id = serializers.CharField(read_only=True)
    problem_type = serializers.ChoiceField(choices=[(x.value, x.value) for x in ProblemType])
    argument = serializers.JSONField(default={})
    state_realtime = serializers.JSONField(read_only=True)
    result_realtime = serializers.JSONField(read_only=True)

    class Meta:
        model = Problem
        fields = ('id', 'task_id', 'problem_type', 'argument', 'result_realtime', 'state_realtime')
