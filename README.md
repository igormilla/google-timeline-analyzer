## Timeline Analyzer

Few scripts I wrote to count time I was spending at work. 

It's one thing to feel like you are spending
too much time in the office, but another is to see actual numbers of how much time you really spend there.

### Usage

1. Download your location data from Google Timeline. Navigate to [takeout.google.com](https://takeout.google.com/settings/takeout)
and select Location History item.
2. Unzip the file, rename it to data.json, and put into root dir of this repository.
3. Change locations.json and set there desired location's coordinates you would like to track   
    * Go to Google Maps, and put a pin on a desired place
    * In ULR look for a part like `@12.456789,9.87654`
    * Remove `.` from numbers and you will get your coordinates:
    ```
        {
            "place" : {
                "latitude": 12456789,
                "longitude": 987654
            }
        }   
    ```
4. Run  `python data-parser.py` to break data into years for faster processing.
5. Run `python main.py 2018` to get your stats about specified location.

### License

MIT