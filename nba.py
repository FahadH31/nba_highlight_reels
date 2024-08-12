#! python3
# Command to run script: 
# python nba.py [ContextMeasure (FGM/FG3M/AST)] [PlayerID] [Season] [SeasonType (Regular Season/Playoffs)] [GameID (optional)]

import sys, os, requests, time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from moviepy.editor import VideoFileClip, concatenate_videoclips

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

os.makedirs('clips', exist_ok=True) # Create directory to store downloaded clips in
clips_folder = 'clips'

# Open chrome browser and navigate to the appropriate URL.
browser = webdriver.Chrome()
browser.get(page_url)
time.sleep(5) # Wait for the page to load

# Close the popup
close_popup_element = browser.find_element(By.ID, 'onetrust-reject-all-handler')
close_popup_element.click()

# Scroll down by 700 pixels (to make the clips clickable)
browser.execute_script("window.scrollBy(0, 700)")  
next_videos = browser.find_elements(By.CLASS_NAME, 'Crom_stickyRank__aN66p') # Get list of all clips on the page

# When applicable, change the filer option to display multiple pages of clips on one page.
try:
    # Attempt to find the dropdown element
    page_dropdown = browser.find_element(By.CLASS_NAME, 'DropDown_select__4pIg9')
    
    # Use the Select class to interact with the dropdown
    select = Select(page_dropdown)
        
    try:
        # Select the option by value
        select.select_by_value('-1')  # This will select the option <option value="-1">All</option>
    except:
        print("The 'All' option was not found.")
except:
    print("Dropdown element not found.")


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
    time.sleep(3)

# Concatenate clips into one final video

video_clips = []

# Load clips into the list
for filename in (os.listdir(clips_folder)):
    if filename.endswith(('.mp4')): 
        clip_path = os.path.join(clips_folder, filename)
        video_clips.append(VideoFileClip(clip_path))

# Concatenate and save the final video
final_clip = concatenate_videoclips(video_clips)
final_clip.write_videofile("output\completed_video.mp4")
