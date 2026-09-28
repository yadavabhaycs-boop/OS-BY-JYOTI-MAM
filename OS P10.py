import tkinter as tk
from tkinter import ttk, messagebox


class DiskScheduling:
    def __init__(self, requests, head, disk_size):
        self.requests = requests
        self.head = head
        self.disk_size = disk_size

    def fcfs(self):
        sequence = [self.head] + self.requests
        movement = sum(abs(sequence[i] - sequence[i - 1])
                       for i in range(1, len(sequence)))
        return sequence, movement

    def sstf(self):
        requests = self.requests.copy()
        current = self.head
        sequence = [current]
        movement = 0

        while requests:
            nearest = min(requests, key=lambda x: abs(x - current))
            movement += abs(nearest - current)
            current = nearest
            sequence.append(current)
            requests.remove(nearest)

        return sequence, movement

    def cscan(self):
        left = sorted([x for x in self.requests if x < self.head])
        right = sorted([x for x in self.requests if x >= self.head])

        sequence = [self.head]
        movement = 0
        current = self.head

        for request in right:
            movement += abs(request - current)
            current = request
            sequence.append(request)

        if current != self.disk_size - 1:
            movement += abs((self.disk_size - 1) - current)
            current = self.disk_size - 1
            sequence.append(current)

        if left:
            movement += self.disk_size - 1
            current = 0
            sequence.append(current)

            for request in left:
                movement += abs(request - current)
                current = request
                sequence.append(request)

        return sequence, movement

    def clook(self):
        left = sorted([x for x in self.requests if x < self.head])
        right = sorted([x for x in self.requests if x >= self.head])

        sequence = [self.head]
        movement = 0
        current = self.head

        for request in right:
            movement += abs(request - current)
            current = request
            sequence.append(request)

        if left:
            movement += abs(current - left[0])
            current = left[0]
            sequence.append(current)

            for request in left[1:]:
                movement += abs(request - current)
                current = request
                sequence.append(request)

        return sequence, movement

    def rss(self):
        requests = self.requests.copy()
        requests.sort()

        lower = [x for x in requests if x < self.head]
        upper = [x for x in requests if x >= self.head]

        sequence = [self.head]
        movement = 0
        current = self.head

        for request in upper:
            movement += abs(request - current)
            current = request
            sequence.append(request)

        for request in reversed(lower):
            movement += abs(request - current)
            current = request
            sequence.append(request)

        return sequence, movement


class SimpleFileSystem:
    def __init__(self, total_blocks=50):
        self.total_blocks = total_blocks
        self.free_blocks = set(range(total_blocks))
        self.files = {}

    def create_file(self, filename, content, blocks_required):
        if not filename:
            return False, "Enter a file name."

        if filename in self.files:
            return False, "File already exists."

        if blocks_required <= 0:
            return False, "Number of blocks must be greater than 0."

        if blocks_required > len(self.free_blocks):
            return False, "Not enough free blocks."

        allocated = sorted(list(self.free_blocks))[:blocks_required]

        for block in allocated:
            self.free_blocks.remove(block)

        self.files[filename] = {
            "content": content,
            "blocks": allocated
        }

        return True, f"File '{filename}' created successfully."

    def read_file(self, filename):
        if filename not in self.files:
            return None

        return self.files[filename]

    def delete_file(self, filename):
        if filename not in self.files:
            return False, "File not found."

        blocks = self.files[filename]["blocks"]

        for block in blocks:
            self.free_blocks.add(block)

        del self.files[filename]

        return True, f"File '{filename}' deleted successfully."

    def directory(self):
        return self.files

    def block_status(self):
        used = self.total_blocks - len(self.free_blocks)
        return used, len(self.free_blocks)


class PracticalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling and Simple File System")
        self.root.geometry("1050x700")
        self.root.resizable(False, False)

        self.file_system = SimpleFileSystem(50)

        self.create_interface()

    def create_interface(self):
        title = tk.Label(
            self.root,
            text="DISK SCHEDULING AND SIMPLE FILE SYSTEM",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        self.disk_tab = tk.Frame(notebook)
        self.file_tab = tk.Frame(notebook)

        notebook.add(self.disk_tab, text="Disk Scheduling")
        notebook.add(self.file_tab, text="Simple File System")

        self.create_disk_tab()
        self.create_file_tab()

    def create_disk_tab(self):
        input_frame = tk.LabelFrame(
            self.disk_tab,
            text="Disk Scheduling Input",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        input_frame.pack(fill="x", padx=15, pady=15)

        tk.Label(
            input_frame,
            text="Disk Size:"
        ).grid(row=0, column=0, padx=10, pady=8)

        self.disk_size_entry = tk.Entry(input_frame, width=20)
        self.disk_size_entry.insert(0, "200")
        self.disk_size_entry.grid(row=0, column=1, padx=10)

        tk.Label(
            input_frame,
            text="Initial Head:"
        ).grid(row=0, column=2, padx=10)

        self.head_entry = tk.Entry(input_frame, width=20)
        self.head_entry.insert(0, "50")
        self.head_entry.grid(row=0, column=3, padx=10)

        tk.Label(
            input_frame,
            text="Request Queue:"
        ).grid(row=1, column=0, padx=10, pady=8)

        self.request_entry = tk.Entry(input_frame, width=70)
        self.request_entry.insert(
            0,
            "82 170 43 140 24 16 190 58 65"
        )
        self.request_entry.grid(
            row=1,
            column=1,
            columnspan=3,
            padx=10,
            sticky="w"
        )

        button_frame = tk.Frame(self.disk_tab)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="FCFS",
            width=12,
            command=lambda: self.run_algorithm("FCFS")
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="SSTF",
            width=12,
            command=lambda: self.run_algorithm("SSTF")
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="C-SCAN",
            width=12,
            command=lambda: self.run_algorithm("C-SCAN")
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="C-LOOK",
            width=12,
            command=lambda: self.run_algorithm("C-LOOK")
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="RSS",
            width=12,
            command=lambda: self.run_algorithm("RSS")
        ).grid(row=0, column=4, padx=5)

        tk.Button(
            button_frame,
            text="Run All",
            width=12,
            command=self.run_all
        ).grid(row=0, column=5, padx=5)

        output_frame = tk.LabelFrame(
            self.disk_tab,
            text="Output",
            font=("Arial", 12, "bold")
        )
        output_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.disk_output = tk.Text(
            output_frame,
            height=20,
            width=115,
            font=("Consolas", 11)
        )
        self.disk_output.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        scrollbar = tk.Scrollbar(
            output_frame,
            command=self.disk_output.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.disk_output.config(
            yscrollcommand=scrollbar.set
        )

    def get_disk_data(self):
        try:
            disk_size = int(self.disk_size_entry.get())
            head = int(self.head_entry.get())

            requests = list(
                map(
                    int,
                    self.request_entry.get().split()
                )
            )

            if disk_size <= 0:
                raise ValueError

            if head < 0 or head >= disk_size:
                messagebox.showerror(
                    "Error",
                    "Head position must be within disk range."
                )
                return None

            for request in requests:
                if request < 0 or request >= disk_size:
                    messagebox.showerror(
                        "Error",
                        f"Request {request} is outside disk range."
                    )
                    return None

            return DiskScheduling(
                requests,
                head,
                disk_size
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter valid numeric values."
            )
            return None

    def run_algorithm(self, algorithm):
        scheduler = self.get_disk_data()

        if scheduler is None:
            return

        if algorithm == "FCFS":
            sequence, movement = scheduler.fcfs()

        elif algorithm == "SSTF":
            sequence, movement = scheduler.sstf()

        elif algorithm == "C-SCAN":
            sequence, movement = scheduler.cscan()

        elif algorithm == "C-LOOK":
            sequence, movement = scheduler.clook()

        elif algorithm == "RSS":
            sequence, movement = scheduler.rss()

        self.disk_output.delete("1.0", tk.END)

        self.disk_output.insert(
            tk.END,
            f"Algorithm: {algorithm}\n"
        )
        self.disk_output.insert(
            tk.END,
            "-" * 80 + "\n"
        )
        self.disk_output.insert(
            tk.END,
            "Head Movement Sequence:\n"
        )
        self.disk_output.insert(
            tk.END,
            " -> ".join(map(str, sequence))
        )
        self.disk_output.insert(
            tk.END,
            f"\n\nTotal Head Movement: {movement} cylinders\n"
        )

    def run_all(self):
        scheduler = self.get_disk_data()

        if scheduler is None:
            return

        algorithms = [
            ("FCFS", scheduler.fcfs()),
            ("SSTF", scheduler.sstf()),
            ("C-SCAN", scheduler.cscan()),
            ("C-LOOK", scheduler.clook()),
            ("RSS", scheduler.rss())
        ]

        self.disk_output.delete("1.0", tk.END)

        for name, result in algorithms:
            sequence, movement = result

            self.disk_output.insert(
                tk.END,
                f"{name}\n"
            )
            self.disk_output.insert(
                tk.END,
                "-" * 80 + "\n"
            )
            self.disk_output.insert(
                tk.END,
                "Sequence: "
                + " -> ".join(map(str, sequence))
                + "\n"
            )
            self.disk_output.insert(
                tk.END,
                f"Total Head Movement: {movement} cylinders\n\n"
            )

    def create_file_tab(self):
        input_frame = tk.LabelFrame(
            self.file_tab,
            text="File Operations",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        input_frame.pack(fill="x", padx=15, pady=15)

        tk.Label(
            input_frame,
            text="File Name:"
        ).grid(row=0, column=0, padx=10, pady=8)

        self.filename_entry = tk.Entry(
            input_frame,
            width=30
        )
        self.filename_entry.grid(
            row=0,
            column=1,
            padx=10
        )

        tk.Label(
            input_frame,
            text="Blocks Required:"
        ).grid(row=0, column=2, padx=10)

        self.blocks_entry = tk.Entry(
            input_frame,
            width=15
        )
        self.blocks_entry.insert(0, "3")
        self.blocks_entry.grid(
            row=0,
            column=3,
            padx=10
        )

        tk.Label(
            input_frame,
            text="File Content:"
        ).grid(row=1, column=0, padx=10, pady=8)

        self.content_entry = tk.Entry(
            input_frame,
            width=70
        )
        self.content_entry.grid(
            row=1,
            column=1,
            columnspan=3,
            padx=10,
            sticky="w"
        )

        button_frame = tk.Frame(self.file_tab)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Create File",
            width=15,
            command=self.create_file
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Read File",
            width=15,
            command=self.read_file
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Delete File",
            width=15,
            command=self.delete_file
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Show Directory",
            width=15,
            command=self.show_directory
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="Block Status",
            width=15,
            command=self.show_block_status
        ).grid(row=0, column=4, padx=5)

        output_frame = tk.LabelFrame(
            self.file_tab,
            text="File System Output",
            font=("Arial", 12, "bold")
        )
        output_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.file_output = tk.Text(
            output_frame,
            height=22,
            width=115,
            font=("Consolas", 11)
        )
        self.file_output.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        scrollbar = tk.Scrollbar(
            output_frame,
            command=self.file_output.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.file_output.config(
            yscrollcommand=scrollbar.set
        )

        self.show_directory()

    def create_file(self):
        filename = self.filename_entry.get().strip()
        content = self.content_entry.get()

        try:
            blocks = int(self.blocks_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter a valid number of blocks."
            )
            return

        success, message = self.file_system.create_file(
            filename,
            content,
            blocks
        )

        if success:
            messagebox.showinfo(
                "Success",
                message
            )
            self.show_directory()
            self.clear_file_inputs()
        else:
            messagebox.showerror(
                "Error",
                message
            )

    def read_file(self):
        filename = self.filename_entry.get().strip()

        if not filename:
            messagebox.showerror(
                "Error",
                "Enter a file name."
            )
            return

        file_data = self.file_system.read_file(filename)

        self.file_output.delete(
            "1.0",
            tk.END
        )

        if file_data is None:
            self.file_output.insert(
                tk.END,
                f"File '{filename}' not found."
            )
            return

        self.file_output.insert(
            tk.END,
            "FILE INFORMATION\n"
        )
        self.file_output.insert(
            tk.END,
            "=" * 60 + "\n"
        )
        self.file_output.insert(
            tk.END,
            f"File Name : {filename}\n"
        )
        self.file_output.insert(
            tk.END,
            f"Content   : {file_data['content']}\n"
        )
        self.file_output.insert(
            tk.END,
            f"Blocks    : {file_data['blocks']}\n"
        )
        self.file_output.insert(
            tk.END,
            f"Size      : {len(file_data['blocks'])} blocks\n"
        )

    def delete_file(self):
        filename = self.filename_entry.get().strip()

        if not filename:
            messagebox.showerror(
                "Error",
                "Enter a file name."
            )
            return

        success, message = self.file_system.delete_file(
            filename
        )

        if success:
            messagebox.showinfo(
                "Success",
                message
            )
            self.show_directory()
            self.clear_file_inputs()
        else:
            messagebox.showerror(
                "Error",
                message
            )

    def show_directory(self):
        self.file_output.delete(
            "1.0",
            tk.END
        )

        self.file_output.insert(
            tk.END,
            "DIRECTORY MANAGEMENT\n"
        )
        self.file_output.insert(
            tk.END,
            "=" * 80 + "\n\n"
        )

        if not self.file_system.files:
            self.file_output.insert(
                tk.END,
                "Directory is empty.\n"
            )
            return

        self.file_output.insert(
            tk.END,
            f"{'File Name':<20}"
            f"{'Blocks':<35}"
            f"{'Size':<10}\n"
        )
        self.file_output.insert(
            tk.END,
            "-" * 80 + "\n"
        )

        for filename, data in self.file_system.files.items():
            blocks = str(data["blocks"])
            size = str(len(data["blocks"]))

            self.file_output.insert(
                tk.END,
                f"{filename:<20}"
                f"{blocks:<35}"
                f"{size:<10}\n"
            )

        used, free = self.file_system.block_status()

        self.file_output.insert(
            tk.END,
            "\n"
        )
        self.file_output.insert(
            tk.END,
            f"Total Blocks : {self.file_system.total_blocks}\n"
        )
        self.file_output.insert(
            tk.END,
            f"Used Blocks  : {used}\n"
        )
        self.file_output.insert(
            tk.END,
            f"Free Blocks  : {free}\n"
        )

    def show_block_status(self):
        used, free = self.file_system.block_status()

        self.file_output.delete(
            "1.0",
            tk.END
        )

        self.file_output.insert(
            tk.END,
            "BLOCK ALLOCATION STATUS\n"
        )
        self.file_output.insert(
            tk.END,
            "=" * 70 + "\n\n"
        )

        self.file_output.insert(
            tk.END,
            f"Total Blocks : {self.file_system.total_blocks}\n"
        )
        self.file_output.insert(
            tk.END,
            f"Used Blocks  : {used}\n"
        )
        self.file_output.insert(
            tk.END,
            f"Free Blocks  : {free}\n\n"
        )

        self.file_output.insert(
            tk.END,
            "Free Block Numbers:\n"
        )
        self.file_output.insert(
            tk.END,
            str(sorted(self.file_system.free_blocks))
        )

    def clear_file_inputs(self):
        self.filename_entry.delete(
            0,
            tk.END
        )
        self.content_entry.delete(
            0,
            tk.END
        )


root = tk.Tk()
app = PracticalGUI(root)
root.mainloop()
