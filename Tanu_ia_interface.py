# Importing the required libraries

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import requests
import os
import datetime
from zipfile import ZipFile
import csv
from PyQt6.QtWidgets import *

app = QApplication(sys.argv)

main_window = QWidget()
main_window.setWindowTitle("Market Analysis")
# If exited from fullscreen, this would be its dimensions
main_window.setGeometry(10, 50, 1000, 500)
main_window_layout = QHBoxLayout(main_window)

# Create a stacked widget to hold different pages
# This is the main window that will be shown when the app is run
date_string = ''
stacked_widget = QStackedWidget()
main_window_layout.addWidget(stacked_widget)

sidebar_width = 220

# Creating a function to create the download interface where the user can select the date and download that day's data
def download_interface():
    global date_string
    date_selection_page = QWidget()
    date_selection_layout = QVBoxLayout(date_selection_page)
    title_lable = QLabel("Trading Assistant")
    title_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_lable.setStyleSheet("font-size: 20px; font-weight: bold;")  # Style the label better
    date_selection_label = QLabel("Select Date")
    date_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    date_picker = QDateEdit()
    date_picker.setCalendarPopup(True)
    date_picker.setDate(QDate.currentDate())
    date_picker.setDisplayFormat("yyyyMMdd")  # Set the display format to YYYY-MM-DD

    download_button = QPushButton("Download")

    date_selection_layout.addStretch()
    date_selection_layout.addWidget(date_selection_label)
    date_selection_layout.addWidget(date_picker)
    date_selection_layout.addWidget(download_button)
    date_selection_layout.addStretch()

    date_string = date_picker.text()  # Get the date from the QDateEdit widget

    def download_data():
        global date_string
        date_string = date_picker.text()  # Get the date from the QDateEdit widget
        global downloaded
        downloaded = False  # Reset the downloaded flag

        # URL of the CSV file
        url = f'https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{date_string}_F_0000.csv.zip'

        # Folder where you want to save the file
        ### CHANGE TO DESIRED PATH WHEN RUNNING
        save_folder = r'C:\\Tanu\\Coding\\CSC IA\\Code\\Files\\'
        os.makedirs(save_folder, exist_ok=True)

        # File name to save as
        file_name = f'Bhavcopy_FO_{date_string}.zip'
        save_path = os.path.join(save_folder, file_name)

        # Set headers to simulate a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Download the file with the headers
        print("Attempting to download the file...")
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"File saved successfully at: {save_path}")
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")
                QMessageBox.warning(None, "Error", f"Failed to download the file. Status code: {response.status_code}")
                return
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while trying to download the file: {e}")
            QMessageBox.warning(None, "Error", f"An error occurred while trying to download the file: {e}")
            return

        # Extract the zip file
        try:
            with ZipFile(save_path, "r") as zip:
                print('Extracting all the files now...')
                zip.extractall(save_folder)
                QMessageBox.information(None, "Success", "File downloaded and extracted successfully!")
                downloaded = True
        except FileNotFoundError:
            QMessageBox.warning(None, "Error", f"File not found at: {save_path}")
            return
        except Exception as e:
            QMessageBox.warning(None, "Error", f"An error occurred during extraction: {e}")
            return

        # Sort and save the extracted file
        try:
            # Read the CSV file
            ### CHANGE TO CORRECT PATH WHEN RUNNING
            file_path = f"C:\\Tanu\\Coding\\CSC IA\\Code\\Files\\BhavCopy_NSE_FO_0_0_0_{date_string}_F_0000.csv"
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                rows = list(reader)

            rows.sort(key=lambda row: (row[7], datetime.datetime.strptime(row[9], '%Y-%m-%d'), row[12], row[11]))

            # Write the sorted data to a new CSV file
            ### CHANGE TO DESIRED PATH WHEN RUNNING
            sorted_file_path = f"C:\\Tanu\\Coding\\CSC IA\\Code\\Files\\Sorted_BhavCopy_{date_string}.csv"
            with open(sorted_file_path, "w", newline='', encoding='utf-8') as sorted_file:
                writer = csv.writer(sorted_file)
                selected_headers = [header[7], header[9], header[11], header[12], header[13], header[14], header[15], header[16], header[17], header[18], header[19], header[20]]
                writer.writerow(selected_headers)
                for row in rows:
                    selected_columns = [row[7], row[9], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20]]
                    writer.writerow(selected_columns)

            print(f"Sorted file saved successfully at: {sorted_file_path}")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"An error occurred while sorting the file: {e}")
            return

        # Switch to the main interface page
        if downloaded:
            main_interface()  # Initialize the main interface
            stacked_widget.setCurrentIndex(1)  # Switch to the main interface page

    download_button.clicked.connect(download_data)
    
    # Add the date selection page to the stacked widget
    stacked_widget.addWidget(date_selection_page)

# The main interface function that will be shown after the data is downloaded
# This is the main window that will be shown when the app is run
def main_interface():
    global date_string
    global sidebar_width
    ### Main interface

    window = QWidget()
    window.setWindowTitle("Market Analysis")
    window.setGeometry(10, 50, 1000, 500)
    window_layout = QHBoxLayout(window)

    # The sidebar layout
    sidebar = QVBoxLayout()
    sidebar_container = QWidget()
    sidebar_container.setLayout(sidebar)
    sidebar_width = 220
    sidebar_container.setFixedWidth(sidebar_width)

    # Expand sidebar:
    expand_button = QPushButton("☰")
    expand_button.setFixedHeight(40)
    sidebar.addWidget(expand_button)

    # Menu buttons
    menu_buttons = []
    menu_items = ["Dashboard", "Preset Filter", "Watchlist", "Search", "Log"]

    for item in (menu_items):
        button = QPushButton(item)
        button.setFixedHeight(50)
        menu_buttons.append(button)
        sidebar.addWidget(button)

    ## To push many items to the top
    sidebar.addStretch()

    content_area = QStackedWidget()

    #Pages with content

    def dashboard_page():
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addStretch()
        label = QLabel("Welcome Subbu!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")  # Style the label better
        label.move(1000, 100)
        layout.addWidget(label)
        layout.addStretch()
    
        return page

    # The data will be filtered based on the client's request during the interview and displayed in a table format
    def preset_page():
        page = QWidget()
        layout = QVBoxLayout(page)
        table = QTableWidget(10000, 12)
        # This is the table in which the filtered data will be displayed
        table.setHorizontalHeaderLabels(["Stock", "Expiry Date", "Strike Price", "Option type", "Fin Instr Num", "Open", "High", "Low", "Closing", "Last Traded", "Prev. Close", "Underlying"])    
        
        # The code accesses the file in which the data is stored 
        ### CHANGE TO CORRECT PATH WHEN RUNNING
        file_path = "C:\\Tanu\\Coding\\CSC IA\\Code\\Files\\Sorted_BhavCopy_"+date_string+".csv" 

        filter_label = QLabel("Filtered Data")

        with open(file_path, "r") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)
            row_index = 0
            for row in rows[:-1]:
                if row[3] == "CE":
                    # compare the value of the row with the value of the next row
                    if float(row[8]) < float(rows[rows.index(row)+1][8]):
                        # add the row to the table
                        for column_index in range(len(header)):
                            table.setItem(row_index, column_index, QTableWidgetItem(rows[rows.index(row)][column_index])) 
                        row_index = row_index + 1
                elif row[3] == "PE":
                    # compare the value of the row with the value of the next row
                    if float(row[8]) > float(rows[rows.index(row)+1][8]):
                        for column_index in range(len(header)):
                            table.setItem(row_index, column_index, QTableWidgetItem(rows[rows.index(row)][column_index])) 
                        row_index = row_index + 1    

        layout.addWidget(filter_label)
        layout.addWidget(table)
        return page

    # This is the page that will be shown when the user selects the watchlist option
    # The user can add stocks to the watchlist and track their own performance in those stocks
    def watchlist_page():
        page = QWidget()
        layout = QHBoxLayout(page)
        # Main layout
        main_layout = QVBoxLayout()

        title = QLabel("Monitor and Track Selected Stocks and Their Growth")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Content layout

        content_layout = QHBoxLayout()

        # LEFT PANEL: Watchlist
        watchlist_frame = QFrame()
        watchlist_frame.setFrameShape(QFrame.Shape.StyledPanel)
        watchlist_layout = QVBoxLayout(watchlist_frame)

        watchlist_label = QLabel("Stocks Being Tracked")
        watchlist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        stock_list = QListWidget()
        
        # Reads the stocks from the Watchlist CSV file and adds them to the list
        ### CHANGE TO CORRECT PATH WHEN RUNNING
        watchlist_file = "C:\\Tanu\\Coding\\CSC IA\\Code\\Watchlist.csv"
        with open(watchlist_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                stock_list.addItem(row[0])

        watchlist_layout.addWidget(watchlist_label)
        watchlist_layout.addWidget(stock_list)  

        # RIGHT PANEL: Stock Details
        right_panel_frame = QFrame()
        right_panel_frame.setFrameShape(QFrame.Shape.StyledPanel)
        right_panel_layout = QVBoxLayout(right_panel_frame)

        # The stock info and buttons will be displayed here
        stock_details_frame = QFrame()
        stock_details_frame.setFrameShape(QFrame.Shape.StyledPanel)
        stock_details_layout = QHBoxLayout(stock_details_frame)

        stock_info_frame = QFrame()
        stock_info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        stock_info_layout = QFormLayout(stock_info_frame)

        stock_info_label = QLabel("Stock Information")
        stock_info_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        stock_info_layout.addWidget(stock_info_label)

        selected_stock = stock_list.currentItem().text() if stock_list.currentItem() else "Select a stock"
        stock_name_label = QLabel(selected_stock)
        stock_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stock_name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white; margin-bottom: 10px;")  # Style the label

        stock_info_layout.setSpacing(10)

        invested_label = QLabel("Amount Invested:")
        invested_entry = QLineEdit()
        invested_entry.setPlaceholderText("Amount Invested")
        invested_entry.setReadOnly(True)  # Make it read-only
        stock_info_layout.addRow(invested_label, invested_entry)
        profits_gained_label = QLabel("Profits Gained:")
        profits_gained_entry = QLineEdit()
        profits_gained_entry.setPlaceholderText("Profits Gained")
        profits_gained_entry.setReadOnly(True)  # Make it read-only
        stock_info_layout.addRow(profits_gained_label, profits_gained_entry)
        last_traded_label = QLabel("Last Traded:")
        last_traded_entry = QLineEdit()
        last_traded_entry.setPlaceholderText("Last Traded")
        last_traded_entry.setReadOnly(True)  # Make it read-only
        stock_info_layout.addRow(last_traded_label, last_traded_entry)
        sp_label = QLabel("Strike Price:")
        sp_entry = QLineEdit()
        sp_entry.setPlaceholderText("Strike Price")
        sp_entry.setReadOnly(True)  # Make it read-only
        stock_info_layout.addRow(sp_label, sp_entry)

        notes_label = QLabel("Notes")
        notes_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        stock_notes_text = QTextEdit()
        stock_notes_text.setPlaceholderText("Enter your notes here...")
        stock_notes_text.setAlignment(Qt.AlignmentFlag.AlignLeft)    
        stock_info_layout.addWidget(notes_label)
        stock_info_layout.addWidget(stock_notes_text)

        # add a button to store the notes to a textfile
        save_button = QPushButton("Save Notes")

        def save_notes():
            selected_item = stock_list.currentItem()
            if not selected_item:
                QMessageBox.warning(None, "Warning", "Please select a stock from the watchlist.")
                return

            selected_stock = selected_item.text()
            ### CHANGE TO CORRECT PATH WHEN RUNNING
            notes_file = "C:\\Tanu\\Coding\\CSC IA\\Code\\Notes.csv"
            notes_text = stock_notes_text.toPlainText()

            # Read existing notes
            notes_data = []
            file_exists = os.path.isfile(notes_file)
            if file_exists:
                with open(notes_file, "r", newline="") as file:
                    reader = csv.reader(file)
                    notes_data = list(reader)

            # Check if the stock already exists in the file
            updated = False
            for row in notes_data:
                if row[0] == selected_stock:
                    row[1] = notes_text  # Update the note
                    updated = True
                    break

            # If the stock doesn't exist, add a new entry
            if not updated:
                notes_data.append([selected_stock, notes_text])

            # Write the updated data back to the file
            with open(notes_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(notes_data)

            QMessageBox.information(None, "Success", "Notes saved successfully!")

        save_button.clicked.connect(save_notes)

        # Function to update the stock information when a stock is selected from the watchlist
        def update_stock_info():
            selected_stock = stock_list.currentItem().text() if stock_list.currentItem() else "Select a stock"
            stock_name_label.setText(selected_stock)
            # Search the stock in the CSV file and get the total amount invested, last traded price, type traded, and profits gained
            log_file = "C:\\Tanu\\Coding\\CSC IA\\Code\\Log_Data.csv"
            with open(log_file, "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                rows = list(reader)
                total_invested = 0
                profits_gained = 0
                last_traded = ''
                sp_traded = ''
                for row in rows:
                    if row[0] == selected_stock:
                        total_invested += float(row[4])
                        profits_gained += float(row[5])
                        last_traded = row[1]
                        sp_traded = row[2]
                invested_entry.setText(str(total_invested))
                profits_gained_entry.setText(str(profits_gained))
                last_traded_entry.setText(last_traded)
                sp_entry.setText(sp_traded)

            # Read the notes from the CSV file and display them in the text box
            #### CHANGE TO CORRECT PATH WHEN RUNNING
            with open("C:\\Tanu\\Coding\\CSC IA\\Code\\Notes.csv", "r") as file:
                reader = csv.reader(file)
                rows = list(reader)
                for row in rows:
                    if row[0] == selected_stock.upper():
                        stock_notes_text.setText(row[1])
                        break
                else:
                    stock_notes_text.clear()

        stock_list.itemClicked.connect(update_stock_info)

        stock_buttons_frame = QFrame()
        stock_buttons_layout = QVBoxLayout(stock_buttons_frame)
        # add button to remove the stock from the watchlist
        remove_button = QPushButton("Remove from Watchlist")
        
        # Function to remove the selected stock from the watchlist
        def remove_stock():
            selected_item = stock_list.currentItem()
            if not selected_item:
                QMessageBox.warning(None, "Warning", "Please select a stock to remove.")
                return

            stock_name = selected_item.text()

            # Remove the stock from the watchlist CSV file
            with open(watchlist_file, "r", newline="") as file:
                rows = list(csv.reader(file))

            with open(watchlist_file, "w", newline="") as file:
                writer = csv.writer(file)
                for row in rows:
                    if row[0] != stock_name:
                        writer.writerow(row)

            # Remove the stock from the QListWidget
            stock_list.takeItem(stock_list.row(selected_item))
            QMessageBox.information(None, "Success", f"{stock_name} removed from the watchlist.")

        remove_button.clicked.connect(remove_stock)
        stock_buttons_layout.addWidget(remove_button)
        
        stock_buttons_layout.addWidget(save_button)

        # Function to add stock to the watchlist
        def add_stock():
            stock_name = add_stock_entry.text().strip().upper()
            if not stock_name:
                QMessageBox.warning(None, "Warning", "Stock name cannot be empty.")
                return

            # Check if the stock already exists in the watchlist
            if stock_name in [stock_list.item(i).text() for i in range(stock_list.count())]:
                QMessageBox.information(None, "Info", "Stock is already in the watchlist.")
                return

            # Add the stock to the watchlist CSV file
            with open(watchlist_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([stock_name])

            # Add the stock to the QListWidget
            stock_list.addItem(stock_name)
            add_stock_entry.clear()
            QMessageBox.information(None, "Success", f"{stock_name} added to the watchlist.")

        add_stock_frame = QFrame()
        add_stock_frame.setFrameShape(QFrame.Shape.StyledPanel)
        add_stock_layout = QHBoxLayout(add_stock_frame)

        add_stock_label = QLabel("Add Stock to Watchlist")
        add_stock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        add_stock_entry = QLineEdit()
        add_stock_entry.setPlaceholderText("Enter stock name")
        add_stock_button = QPushButton("Add")
        add_stock_button.clicked.connect(add_stock)

        add_stock_layout.addWidget(add_stock_label)
        add_stock_layout.addWidget(add_stock_entry)
        add_stock_layout.addWidget(add_stock_button)


        stock_details_layout.addWidget(stock_info_frame)
        stock_details_layout.addWidget(stock_buttons_frame)

        right_panel_layout.addWidget(stock_name_label)
        right_panel_layout.addWidget(stock_details_frame)
        right_panel_layout.addWidget(add_stock_frame)


        content_layout.addWidget(watchlist_frame)
        content_layout.addWidget(right_panel_frame)


        main_layout.addWidget(title)
        main_layout.addLayout(content_layout)

        layout.addLayout(main_layout)

        return page

    # The user can search for a stock and view its details in a table format
    def search_page():
        page = QWidget()
        layout = QVBoxLayout(page)
        search_label = QLabel("Today's Positions")
        layout.addWidget(search_label)
        search_entry = QLineEdit()
        search_entry.setPlaceholderText("Enter stock code")
        layout.addWidget(search_entry)
        table = QTableWidget()
        ### CHANGE TO CORRECT PATH WHEN RUNNING
        file2 = open("C:\\Tanu\\Coding\\CSC IA\\Code\\Files\\Sorted_BhavCopy_"+date_string+".csv", "r")

        reader = csv.reader(file2)
        header = next(reader)
        rows = list(reader)

        table.setColumnCount(len(header))
        table.setRowCount(len(rows))

        table.setHorizontalHeaderLabels(["Stock", "Expiry Date", "Strike Price", "Option type", "Fin Instr Num", "Open", "High", "Low", "Closing", "Last Traded", "Prev. Close", "Underlying"])

        for row_index in range(len(rows)-1):
            for column_index in range(len(header)-1):
                table.setItem(row_index, column_index, QTableWidgetItem(rows[row_index][column_index]))

        # Function to search for a stock and display it in the table
        def search_function():
            search_value = search_entry.text().strip().upper()
            table.setRowCount(0)

            for row in rows:
                if search_value in row[0].upper():
                    row_index = table.rowCount()
                    table.insertRow(row_index)

                    for column_index in range(len(header)-1):
                        table.setItem(row_index, column_index, QTableWidgetItem(row[column_index]))

        search_button = QPushButton("Search")
        search_button.clicked.connect(search_function)
        layout.addWidget(search_button)

        layout.addWidget(table)
        return page

    # This is the log page, where the user can add logs of their trades and view them in a table format
    def log_page():
        page = QWidget()
        page_layout = QHBoxLayout(page)
        page_layout.setContentsMargins(5, 5, 5, 5)
    
        ### ADDING A LOG
        log_frame = QFrame()
        log_frame.setFrameShape(QFrame.Shape.StyledPanel)
        log_frame.setFrameShadow(QFrame.Shadow.Raised)
        #log_frame.setStyleSheet("background-color: #2d2d2d;")
        log_frame.setGeometry(10, 10, 300, 400)
    
        page_layout.addWidget(log_frame)
        frame_layout = QFormLayout(log_frame)
        frame_layout.setSpacing(10)
        log_label = QLabel("New Log")
        log_label.setStyleSheet("font-size: 15px;") # style better
        frame_layout.addRow(log_label)
        stock_name_label = QLabel("Stock Name:")
        stock_name_entry = QLineEdit()
        frame_layout.addRow(stock_name_label, stock_name_entry)
        date_label = QLabel("Date Traded:")
        date_picker = QDateEdit()
        date_picker.setCalendarPopup(True)
        date_picker.setDate(QDate.currentDate())
        frame_layout.addRow(date_label, date_picker)
        strike_price_label = QLabel("Strike Price:")
        strike_price_entry = QLineEdit()
        frame_layout.addRow(strike_price_label, strike_price_entry)
        q_stocks_label = QLabel("No. of Stocks:")
        q_stocks_entry = QLineEdit()
        frame_layout.addRow(q_stocks_label, q_stocks_entry)
        invested_label = QLabel("Amount Invested:")
        invested_entry = QLineEdit()
        frame_layout.addRow(invested_label, invested_entry)
        profits_label = QLabel("Gained/ Lost:")
        profits_entry = QLineEdit()
        frame_layout.addRow(profits_label, profits_entry)

        log_file = "C:\\Tanu\\Coding\\CSC IA\\Code\\Log_Data.csv"
        existing_logs_table = QTableWidget()

        ### Add a new log
        def add_log():
            stock_name = stock_name_entry.text()
            date = date_picker.text()
            strike_price = strike_price_entry.text()
            q_stocks = q_stocks_entry.text()
            invested = invested_entry.text()
            profits = profits_entry.text()

            file_exists = os.path.isfile(log_file)
            header = ["Stock Name", "Date", "Strike Price", "No. of Stocks", "Amount Invested", "Profits"]

            with open(log_file, "a", newline="") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(header)
                else:
                    with open(log_file, "r", newline="") as read_file:
                        reader = csv.reader(read_file)
                        existing_header = next(reader, None)
                        if existing_header != header:
                            writer.writerow(header)
                writer.writerow([stock_name, date, strike_price, q_stocks, invested, profits])

            update_logs_table()

        def update_logs_table():
            with open(log_file, "r", newline="") as file3:
                reader = csv.reader(file3)
                try:
                    header = next(reader)
                except StopIteration:
                    header = ["Stock Name", "Date Traded", "Strike Price", "No. of Stocks", "Amount Invested", "Gained/ Lost"]
                    rows = []
                else:
                    rows = list(reader)

                existing_logs_table.setRowCount(len(rows))
                existing_logs_table.setColumnCount(len(header))
                existing_logs_table.setHorizontalHeaderLabels(header)

                for row_index in range(len(rows)):
                    for column_index in range(len(header)):
                        existing_logs_table.setItem(row_index, column_index, QTableWidgetItem(rows[row_index][column_index]))
        
        update_logs_table()

        page_layout.addWidget(existing_logs_table)
        existing_logs_table.move(1000, 20)
    
        def clear_fields():
            stock_name_entry.clear()
            date_picker.setDate(QDate.currentDate())
            strike_price_entry.clear()
            q_stocks_entry.clear()
            invested_entry.clear()
            profits_entry.clear()
    
        add_log_button = QPushButton("Add Log")
        frame_layout.addRow(add_log_button)
        add_log_button.clicked.connect(add_log)
        # Adds the log to the table next to it

        clear_fields_button = QPushButton("Clear Fields")
        frame_layout.addRow(clear_fields_button)
        add_log_button.clicked.connect(clear_fields)
        clear_fields_button.clicked.connect(clear_fields)
        return page

    pages = [dashboard_page(), preset_page(), watchlist_page(), search_page(), log_page()]

    for i in pages:
        content_area.addWidget(i)

    window_layout.addWidget(sidebar_container)
    window_layout.addWidget(content_area)

    # Define toggle function for the sidebar
    def toggle_sidebar():
        global sidebar_width
        if sidebar_container.width() == sidebar_width:
            sidebar_container.setFixedWidth(60)  # Collapse width
            expand_button.setText("►")
        
            for button in menu_buttons:
                button.setText("")  # Hide button labels
        else:
            sidebar_container.setFixedWidth(sidebar_width)  # Expand width
            expand_button.setText("☰")
            for idx, button in enumerate(menu_buttons):
                button.setText(menu_items[idx])  # Restore labels

    # Connect the expand button
    expand_button.clicked.connect(toggle_sidebar) 

    # Connect menu buttons to switch pages
    for index, button in enumerate(menu_buttons):
        button.clicked.connect(lambda _, idx=index: content_area.setCurrentIndex(idx))

    stacked_widget.addWidget(window)

# Run the download interface function to show the initial page
download_interface()

# Set the initial page to the first one
stacked_widget.setCurrentIndex(0)  

# Show the main window
main_window.show()
sys.exit(app.exec())