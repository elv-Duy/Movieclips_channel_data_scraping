# Movieclips_channel_data_scraping
A script to extract metadata from YouTube's Movieclips channel using a provided list of video URLs separated by year of upload

## Installation
```
pip install selenium beautifulsoup4 lxml
```

## Provided URLs separated by year of upload
```
video_info_2020.txt
video_info_2021.txt
video_info_2022.txt
video_info_2023.txt
video_info_2024.txt
...
```

## Command
```
python movieclips_scraping.py
```

## Process
* Iterate through each year.
* For each year, access the corresponding list of URLs.
* For each URL, scrape the title, query, copyright, clip description, film description, cast, directors, producers, and screenwriters.
* Store the data in an output JSON file, organized by year.
  ```
  movieCLIP_dataset_2020.json
  movieCLIP_dataset_2021.json
  movieCLIP_dataset_2022.json
  movieCLIP_dataset_2023.json
  movieCLIP_dataset_2024.json
  ...
  ```

## Sample Output
```
{
   "Annie (2014) - Tomorrow (Reprise) Scene (9_9)": {
      "id": "3-pIrRGYw-o",
      "year": 2020,
      "url": "https://www.youtube.com/watch?v=3-pIrRGYw-o",
      "title": "Annie (9/9) - 2014",
      "query": "Tomorrow (Reprise)",
      "clip_description": "Annie (Quvenzhané Wallis) leads New York in singing \"Tomorrow.\"",
      "film_description": "Ever since her parents left her as a baby, little Annie (Quvenzhané Wallis) has led...",
      "copyright": "TM & © Sony (2014)",
      "cast": [
         "Cameron Diaz",
         "David Zayas",
         "Jamie Foxx",
         "Quvenzhané Wallis",
         "Rose Byrne"
      ],
      "director": [
         "Will Gluck"
      ],
      "screenwriter": [
         "Aline Brosh McKenna",
         "Will Gluck"
      ],
      "producer": [],
      "display_title": "Annie 2014"
   },
   "Annie (2014) - Stacks Adopts Annie Scene (8_9)": {
      "id": "q-ftYeag-Ss",
      "year": 2020,
      "url": "https://www.youtube.com/watch?v=q-ftYeag-Ss",
      "title": "Annie (8/9) - 2014",
      "query": "Stacks Adopts Annie",
      "clip_description": "Stacks (Jamie Foxx) adopts Annie (Quvenzhané Wallis).",
      "film_description": "Ever since her parents left her as a baby, little Annie (Quvenzhané Wallis) has led...",
      "copyright": "TM & © Sony (2014)",
      "cast": [
         "Jamie Foxx",
         "Quvenzhané Wallis"
      ],
      "director": [
         "Will Gluck"
      ],
      "screenwriter": [
         "Aline Brosh McKenna",
         "Will Gluck"
      ],
      "producer": [],
      "display_title": "Annie 2014"
   },
  ...
```

