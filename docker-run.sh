COMP=${1:-stcolmans}

docker run \
    --volume "//c/Users/gmcwilliams/OneDrive/Documents/personal:/app/ics-data" \
    --volume "//d/dev/gary/gitrepos/icalendar-data:/app/icalendar-data" \
    icalendar-app
