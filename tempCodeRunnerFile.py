        mkdir("userFiles")
        with open("userFiles/data.json", "w", encoding="utf8") as file:
            self.file = {
                "notes_dict": self.notes_dict,
                "last": self.last
            }
            json.dump(self.file, file, indent=4)
            self.redraw_list_menu()