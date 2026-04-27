import subprocess
import googleapiclient.discovery

youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="YOUR_API_KEY")

def search_video(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=5, # Limit the number of results to 5 for better user experience
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
    print("" \
    "Configs available:\n" \
    "1. mp3 \n" \
    "2. mp4 \n" \
    "3. webm\n" \
    "4. mp3 [music]\n" \
    "")
    configfile = input("What type of download do you want? (type a number): ")
    make_folder = input("Do you want to save it in a folder? (y/n): ").lower()
    add_metadata = input("Do you want to embed metadata? (y/n): ").lower()
    embed_thumb = input("Do you want to embed the thumbnail? (y/n): ").lower()

    extra_flags = ""

    if make_folder == "y":
        folder_name = input("Enter the folder name: ")
        extra_flags += f" -o \"{folder_name}/%(title)s.%(ext)s\""
    
    if make_folder == "n": 
        extra_flags += " -o \"%(title)s.%(ext)s\""
    
    
    if add_metadata == "y":
        extra_flags += " --add-metadata"
        extra_flags += " --parse-metadata \"title:%(artist)s - %(title)s\""

    if embed_thumb == "y":
        extra_flags += " --embed-thumbnail"

    subprocess.run(f"yt-dlp --config-location \"templates\\{configfile}.conf\"{extra_flags} {url}", shell=True)


answer = input("Do you want to search for a video? (y/n): ").lower()

if answer == "y":
    search_query = input("Enter the search query: ")
    search_video(search_query)

elif answer == "n":
    input_url = input("Enter the URL of the video you want to download: ")
    print("" \
    "Configs available:\n" \
    "1. mp3 \n" \
    "2. mp4 \n" \
    "3. webm\n" \
    "4. mp3 [music]\n" \
    "")
    configfile = input("What type of download do you want? (type a number): ")
    
    make_folder = input("Do you want to save it in a folder? (y/n): ").lower()
    add_metadata = input("Do you want to embed metadata? (y/n): ").lower()
    embed_thumb = input("Do you want to embed the thumbnail? (y/n): ").lower()

    extra_flags = ""

    if make_folder == "y":
        folder_name = input("Enter the folder name: ")
        extra_flags += f" -o \"{folder_name}/%(title)s.%(ext)s\""

    if make_folder == "n": 
        extra_flags += " -o \"%(title)s.%(ext)s\""
    
    if add_metadata == "y":
        extra_flags += " --add-metadata"

    if embed_thumb == "y":
        extra_flags += " --embed-thumbnail"

    subprocess.run(
        f"yt-dlp --config-location \"templates\\{configfile}.conf\"{extra_flags} {input_url}",
        shell=True
    )
