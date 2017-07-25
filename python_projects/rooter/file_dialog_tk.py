########################################################################

"""
Open a file using Tk
"""

import tkinter as tk
from tkinter import filedialog

########################################################################


def get_gpx_file(
        initialdir=".",
        filetypes=(
            ("gpx file", "*.gpx"),
            ("All files", "*.*")
        ),
        title="Select input file"):

    """Open file dialog for GPX file."""

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        initialdir=initialdir,
        title=title,
        filetypes=filetypes
    )
    return file_path


########################################################################

if __name__ == '__main__':

    def main():
        """Main test function for askopenfilename."""
        file_path = get_gpx_file(
            filetypes=(("All files", "*.*"), ("GPX files", "*.gpx")),
            title="This is the dialog title",
            initialdir="/"
        )
        print("file_path: '%s'" % file_path)

    main()

########################################################################
