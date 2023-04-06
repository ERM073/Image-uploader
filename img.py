import tkinter as tk
from tkinter import filedialog
import requests
import pyperclip
import json
from PIL import ImageTk, Image



# アップロードするファイルのデフォルトディレクトリ
DEFAULT_DIRECTORY = "."

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # ファイル選択ダイアログを表示するボタンを作成
        self.file_button = tk.Button(self, text="ファイルを選択", command=self.select_file)
        self.file_button.pack()

        # アップロードボタンを作成
        self.upload_button = tk.Button(self, text="アップロード", command=self.upload_file)
        self.upload_button.pack()

        # アップロードされたファイルのURLを表示するテキストボックスを作成
        self.url_textbox = tk.Text(self, height=1)
        self.url_textbox.pack()

        # コピーするボタンを作成
        self.copy_button = tk.Button(self, text="コピー", command=self.copy_url)
        self.copy_button.pack()

        # 選択した画像のプレビューを表示するキャンバスを作成
        self.canvas = tk.Canvas(self, width=300, height=300)
        self.canvas.pack()

    def select_file(self):
        # ファイル選択ダイアログを表示
        filename = tk.filedialog.askopenfilename(initialdir=DEFAULT_DIRECTORY)

        # 選択されたファイルを保存
        self.file = open(filename, "rb")

        # 選択した画像のプレビューを表示
        image = Image.open(filename)
        image = image.resize((300, 300))
        self.image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

    def upload_file(self):
        # アップロード先のURLを指定
        url = "https://img.freehostbox.net/api/index.php"

        # ファイルをアップロードする
        response = requests.post(url, files={"file": self.file})

        # アップロードに成功した場合は、アップロードされたファイルのURLを表示
        if response.status_code == 200:
            # アップロードされたファイルのURLを構築
            filename = response.json()["filename"]
            url = f"{filename}"

            # is.gd APIで短縮URLに変換する
            isgd_url = f"https://is.gd/create.php?format=json&url={filename}"
            isgd_response = requests.get(isgd_url)

            # 短縮URLを取得して表示
            if isgd_response.status_code == 200:
                result = json.loads(isgd_response.text)
                short_url = result["shorturl"]
            self.url_textbox.delete("1.0", tk.END)
            self.url_textbox.insert(tk.END, short_url)



    def copy_url(self):
        # URLをクリップボードにコピーする
        url = self.url_textbox.get("1.0", tk.END).strip()
        if url:
            pyperclip.copy(url)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("画像共有ツール")
    app = Application(master=root)
    app.mainloop()
