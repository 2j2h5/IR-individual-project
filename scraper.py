import tkinter as tk
from tkinter import ttk
from youtube_comment_downloader import YoutubeCommentDownloader
import threading

def scrape_youtube_comments(url, count, progress, result_label):
    downloader = YoutubeCommentDownloader()
    video_id = url.split("v=")[-1].split("&")[0]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    comments = []

    for i, comment in enumerate(downloader.get_comments_from_url(youtube_url=video_url, sort_by=0)):
        comments.append(f"<SOS> {comment['text'].replace('\n', ' <LF> ')} <EOS>")

        progress["value"] = (i + 1) / count * 100
        root.update_idletasks()

        if i+1 >= count:
            break

    result_label["text"] = f"{len(comments)} comments scraped!"
    progress["value"] = 100
    return comments, video_id

def save_comments_to_txt(comments, video_id):
    filename = f"youtube-comments-{video_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(comments))

def on_button_click(entry, entry_result, result_label, progress):
    url = entry.get()
    count = int(entry_result.get())

    result_label["text"] = "Scraping..."
    progress["value"] = 0

    def run_scraping():
        comments, video_id = scrape_youtube_comments(url, count, progress, result_label)
        save_comments_to_txt(comments, video_id)
    
    threading.Thread(target=run_scraping, daemon=True).start()

def init():
    root = tk.Tk()
    root.title("Youtube Comment Scraper")
    root.geometry("400x300")

    label = tk.Label(root, text="Enter youtube URL")
    label_count = tk.Label(root, text="Count")
    label_result = tk.Label(root, text="")

    entry = tk.Entry(root, width=50)
    entry_count = tk.Entry(root, width=5)
    entry_count.insert(0, "10")

    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")

    button = tk.Button(root, text="Scrape!", command=lambda: on_button_click(entry, entry_count, label_result, progress))

    label.pack(pady=10)
    entry.pack(pady=10)
    label_count.pack(pady=10)
    entry_count.pack(pady=10)
    button.pack(pady=10)
    progress.pack(pady=10)
    label_result.pack(pady=10)

    return root

if __name__ == "__main__":
    root = init()
    root.mainloop()