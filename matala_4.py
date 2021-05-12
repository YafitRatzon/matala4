import requests

# Basic Values
checkSmallerNum = 0
mostFarByDis = []
listOfMostFar = []
detailsOfDest = {}
dest_file = open("dests.txt", "r", encoding='utf-8')
API_KEY = 'PUT API_KEY HERE'
source = "תל אביב"
try:
    for dest in dest_file:
        # Get Destination Matrix Information
        urlMatrix = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
        response_DMatrix_data = requests.get(urlMatrix + source + "&destinations=" + dest + "&key=" + API_KEY)
        # Get Geocode Information
        urlDecode = "https://maps.googleapis.com/maps/api/geocode/json?address="
        response_geocode_data = requests.get(urlDecode + dest + "&key=" + API_KEY)

        # Calculate Distance
        distanceInMeters = response_DMatrix_data.json()["rows"][0]["elements"][0]["distance"]["value"]
        distanceInKm = int(distanceInMeters) / 1000

        # Calculate Time
        timeInSeconds = response_DMatrix_data.json()["rows"][0]["elements"][0]["duration"]["value"]
        hours = int((int(timeInSeconds) / 60) / 60)
        minutes = int((int(timeInSeconds) / 60) % 60)

        # Calculate latitude
        latitude = response_geocode_data.json()["results"][0]["geometry"]["location"]["lat"]

        # Calculate Longitude
        longitude = response_geocode_data.json()["results"][0]["geometry"]["location"]["lng"]

        # Create the tuple and add it to the dictionary
        infoEachDest = (distanceInKm, str(hours) + " Hours " + str(minutes) + " Minutes", latitude, longitude)

        detailsOfDest[dest.replace('\n', '')] = infoEachDest

    # Print all the details
    for dest in detailsOfDest:
        print("The distance between Tel Aviv to :" + str(dest) + " is " + str(detailsOfDest[dest][0]) + " km")
        print("Travel time is: " + str(detailsOfDest[dest][1]))
        print("The latitude is: " + str(detailsOfDest[dest][2]) + " and the longitude is: " + str(detailsOfDest[dest][3]))
        print()

    # Check most far destinations from the dictionary
    for dest in detailsOfDest:
        mostFarByDis.append(detailsOfDest[dest][0])
    mostFarByDis.sort()
    mostFarByDis = mostFarByDis[len(mostFarByDis)-3:]

    # Get the names of the destinations from the dictionary
    for dest in detailsOfDest:
        for i in mostFarByDis:
            if i == detailsOfDest[dest][0]:
                listOfMostFar.append(str(dest))

    # Print all the most far cities
    print("The most far cities from Tel Aviv are: ")
    print(*listOfMostFar, sep=',')
except:
    print("There is an Error with the destinations")