import subprocess
import googleapiclient.discovery

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="YOUR_API_KEY_HERE")

def search_video(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=query,
        type="video"
    )
    response = request.execute()

    results = []
    for item in response.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        title = item.get("snippet", {}).get("title")

        if not video_id or not title:
            continue

        results.append({
            "videoId": video_id,
            "title": title
        })

    if not results:
        print("No valid video found for this search.")
        return

    for i, video in enumerate(results, 1):
        print(f"{i}. {video['title']}")

    choice = int(input("Enter the number of the video to download: ")) - 1

    if choice < 0 or choice >= len(results):
        print("Invalid choice.")
        return

    selected = results[choice]

    url = f"https://www.youtube.com/watch?v={selected['videoId']}"
    configfile = input("What type of download do you want? (mp3, mp4 or webm): ")
    subprocess.run(f"yt-dlp --config-location \"templates\\{configfile}.conf\" {url}", shell=True)


answer = input("Do you want to search for a video? (y/n): ").lower()
if answer == "y":
    search_query = input("Enter the search query: ")
    search_video(search_query)

if answer == "n":
    input_url = input("Enter the URL of the video you want to download as MP3: ")
    configfile = input("What type of download do you want? (mp3, mp4 or webm): ")
    subprocess.run(f"yt-dlp --config-location \"templates\\{configfile}.conf\" {input_url}", shell=True)
