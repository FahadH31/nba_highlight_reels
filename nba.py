#! python3
# [ContextMeasure (FGM/FG3M)] [PlayerID] [Season] [SeasonType (Regular Season/Playoffs)] [GameID]
import sys, os, requests, time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Variables for CMDL Arguments
context_measure = sys.argv[1]
player_id = sys.argv[2]
season = sys.argv[3]
season_type = sys.argv[4]

# If 5 cmdl args, then searching for a season (not including game_id)
if len(sys.argv) == 5:
    page_url = 'https://www.nba.com/stats/events?CFID=&CFPARAMS=&ContextMeasure='+context_measure+'&GameID=&PlayerID='+player_id+'&Season='+season+'&SeasonType='+season_type+'&TeamID=&flag=3&sct=plot&section=game'

# If 6 cmdl args, then searching for a particular game (including game_id)
elif len(sys.argv) == 6:
    game_id = sys.argv[5]
    page_url = 'https://www.nba.com/stats/events?CFID=&CFPARAMS=&ContextMeasure='+context_measure+'&GameID='+game_id+'&PlayerID='+player_id+'&Season='+season+'&SeasonType='+season_type+'&TeamID=&flag=3&sct=plot&section=game'

os.makedirs('clips', exist_ok=True) # Store clips in /clips

# Open chrome browser and navigate to the appropriate URL.
browser = webdriver.Chrome()
browser.get(page_url)
time.sleep(5) # Wait for the page to load

# Close the popup
close_popup_element = browser.find_element(By.ID, 'onetrust-reject-all-handler')
close_popup_element.click()

# Scroll down by 800 pixels (to make the clips clickable)
browser.execute_script("window.scrollBy(0, 800)")  
next_videos = browser.find_elements(By.CLASS_NAME, 'Crom_stickyRank__aN66p') # Get list of all clips on the page

# Initial counter values
video_counter = 1 
name_counter = 1

# Loop to download all video clips on page.
for x in next_videos:
    
    # Ensure correct number of loop iterations
    if(video_counter == len(next_videos)):
        break
    
    next_video = next_videos[video_counter] # Get the current clip
    next_video.click() # Click on the current clip to start playing it

    # Get the link to the clip
    try:
        video_element = browser.find_element(By.ID,'vjs_video_3_html5_api')
        video_url = video_element.get_attribute('src')
    except:
        print('Element not found.')

    # Name and download the clip
    output_file = f"clips/player{player_id}_{context_measure}_{season}_{name_counter}.mp4"
    try:
        # Stream the download
        with requests.get(video_url, stream=True) as r:
            r.raise_for_status()  # Check if the request was successful
            with open(output_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):  # 8 KB chunks
                    f.write(chunk)
        print(f"Downloaded {video_url}")
    except requests.exceptions.HTTPError as err:
        print("HTTP error occurred: {err}")
    except Exception as err:
        print("An error occurred: {err}")

    name_counter+=1
    video_counter+=1
    time.sleep(2)
