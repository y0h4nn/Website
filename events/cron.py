from django_cron import CronJobBase, Schedule


class RecurrentEvents(CronJobBase):
    RUN_EVERY_MINS = 120

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'events.recurrent_events'    # a unique code

    def do(self):
        pass    # do your thing here

