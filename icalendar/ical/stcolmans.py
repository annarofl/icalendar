from ical.events import Events

year = '2017-18'

events = Events('stcolmans', year)
#events.set_savedir(gettempdir())

events.add_events()
