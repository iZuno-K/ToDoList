from django.db import models


class Card(models.Model):
    pipe_line = models.ForeignKey('kanban.PipeLine', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    expected_effort = models.FloatField("Expected effort", blank=True, default=1)
    real_effort = models.FloatField("Real effort", blank=True, null=True)
    complete_time = models.DateTimeField("Complete time", blank=True, null=True)
    STATE_CHOICES = (
        ("Pending", "Pending"),
        ("Working", "Working"),
        ("Complete", "Complete"),
        ("Archived", "Archived")
    )
    max_len = max(map(lambda x: len(x[1]), STATE_CHOICES))
    task_state = models.CharField("State", choices=STATE_CHOICES, max_length=max_len, default=STATE_CHOICES[0][1])

    def __str__(self):
        return '{}: {} of {}'.format(self.pk, self.title, self.pipe_line)

    @classmethod
    def get_list_by_pipe_line(cls, pipe_line):
        return list(cls.objects.filter(pipe_line=pipe_line).order_by('order'))

    @classmethod
    def get_by_id(cls, card_id):
        try:
            return cls.objects.get(id=card_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_current_card_count_by_pipe_line(cls, pipe_line):
        return cls.objects.filter(pipe_line=pipe_line).count()
