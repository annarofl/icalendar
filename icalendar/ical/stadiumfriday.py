from ical.events import Events

year = '2017-18'

events = Events('stadiumfriday', year)
#events.set_savedir(gettempdir())

events.add_events()
