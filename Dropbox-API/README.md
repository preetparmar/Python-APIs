# Dropbox API

An API to get files from dropbox. I have referred to the official dropbox API, you can find the link [here](https://www.dropbox.com/developers/documentation/python)

# Usage 🛠:

I started to track my expenses on my phone, and the app that I was using had a feature where I could export my expenses in CSV format to my dropbox. The idea was to create a dashboard using Power BI and Tableau so that I could visualize my spending better. To connect the data to dropbox, I decided to download the files to local storage. This was a manual process, something which I didn't like. So I thought of automating that part and ended up writing this python script.

Please note, that there is so much you could do using the dropbox API but for now I am focusing on my use case only. I may add more functionalities later.

- Download all the files from the given dropbox folder to a folder in my local storage.
- Before copying all the files, quickly check for the existing files in the local folder and only download the new files.

---

I have also written an article about this project, feel free to give that a read [here](https://blog.preetparmar.com/dropbox-api-automating-dropbox-downloads-using-python/).
