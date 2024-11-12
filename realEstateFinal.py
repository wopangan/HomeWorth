import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score    

class AboutWindow:
    def __init__(self, master, continue_callback):
        self.master = master
        self.master.title("About HomeWorth")
        self.continue_callback = continue_callback

        # Change background color of the window
        self.master.configure(bg="midnightblue")

        # Set window geometry
        self.master.geometry("1100x600")
        
        # Load and resize the image
        image = Image.open("RealEstate.jpg")
        image = image.resize((300, 200), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(image)

        # About message
        about_msg_1 = (
            "HomeWorth: Real Estate Price Prediction\n\n"
        )

        about_msg_2 = (
            "HomeWorth is a comprehensive real estate price prediction tool designed to assist "
            "homeowners, buyers, and real estate professionals in estimating property values. "
            "\n\nUsing advanced machine learning algorithms, HomeWorth analyzes various factors such "
            "as square footage, number of bedrooms, and year built to provide accurate price "
            "predictions. \n\nWhether you're selling a house, looking to buy a new property, or "
            "simply curious about real estate trends, HomeWorth is your go-to solution."
        )
        
        # About label
        about_label_1 = tk.Label(self.master, text=about_msg_1, font=("Arial", 25, "bold"), justify="center", bg='midnightblue', fg='burlywood1')
        about_label_1.pack(padx=20, pady=20)

        about_label_2 = tk.Label(self.master, text=about_msg_2, font=("Arial", 10), justify="center", bg='midnightblue', fg='burlywood1')
        about_label_2.pack(padx=20, pady=20)

        # Image label
        image_label = tk.Label(self.master, image=self.img)
        image_label.pack(padx=20, pady=10)
        
        # Continue button
        continue_button = tk.Button(self.master, text="Continue", command=self.continue_callback, font=("Arial", 11, "bold"), bg='burlywood1', fg='midnightblue')
        continue_button.pack(pady=10)

        def continue_and_close(self):
            self.master.destroy()
            self.continue_callback()

class RealEstateApp:
    def __init__(self, master):
        self.master = master
        self.master.title("HomeWorth")
        
        # Header title
        header_title = tk.Label(self.master, text = "Real Estate Price Prediction", font = ("Rockwell", 25, "bold"), fg='burlywood1', bg = 'midnightblue')
        header_title.grid(row=0, column=0, columnspan=5, padx=5, pady=10)
        
        student_names = tk.Label(self.master, text = "Created By: Webster Pangan & Charles Raphael Sanchez, CS-301", font = ("Arial", 10, "bold"), fg='burlywood1', bg = 'midnightblue')
        student_names.grid(row=10, column=0, columnspan = 5, padx=5, pady=(0, 5), sticky = 's')

        self.num_independent_vars = 3  # Fixed number of independent variables
        self.csv_data = None
        
        self.create_widgets()
        
    def create_widgets(self):

        tk.Label(self.master, text="Upload CSV File:" , font = ("Arial", 9), fg='burlywood1', bg = 'midnightblue').grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.upload_button = tk.Button(self.master, text="Upload", command=self.upload_csv, font=("Arial", 11, "bold"), bg= 'burlywood1', fg='midnightblue')
        self.upload_button.grid(row=1, column=2, padx=3, pady=3)
        
        # Text widgets for the columns from the CSV file
        self.text_boxes = {}
        csv_columns = ["Column1", "Column2", "Column3", "Column4", "Column5"]
        for idx, col in enumerate(csv_columns):
            text_box = tk.Text(self.master, height=20, width=30, bg = 'old lace', font = ("Arial", 12))
            text_box.grid(row=2, column=idx, padx=5, pady=5)
            self.text_boxes[col] = text_box

            # Disable editing
            self.text_boxes[col].config(state=tk.DISABLED)
        
        self.predict_button = tk.Button(self.master, text="Predict", command=self.predict, font = ("Arial", 11, "bold"), bg= 'burlywood1', fg='midnightblue')
        self.predict_button.grid(row=6, column=2, columnspan=1, padx=5, pady=5)
        
        # Frame for output text
        output_frame = tk.Frame(self.master)
        output_frame.grid(row=8, column=0, columnspan=len(csv_columns), padx=5, pady=10)

        # Label for the output title
        output_title = tk.Label(output_frame, text="Output", font=("Arial", 15, "bold"))
        output_title.grid(row=0, column=0, columnspan=2, pady=(0, 5))

        # Text widget for displaying output
        self.output_text = tk.Text(output_frame, font = ("Arial", 10), height=18, width=60, wrap=tk.WORD, bg = 'old lace')
        self.output_text.grid(row=1, column=0, columnspan = 2, padx=5, pady=(0, 5))
        self.output_text.config(state=tk.DISABLED)

        # Center the output frame within the window
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)
        output_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.csv_data = pd.read_csv(file_path)

                # Display column names and data in the text boxes
                for idx, col in enumerate(self.csv_data.columns):
                    if idx < 5:  # Limit to the first five columns
                        self.text_boxes[f"Column{idx + 1}"].config(state=tk.NORMAL)
                        self.text_boxes[f"Column{idx + 1}"].delete('1.0', tk.END)
                        self.text_boxes[f"Column{idx + 1}"].insert(tk.END, f"{col}\n")
                        self.text_boxes[f"Column{idx + 1}"].insert(tk.END, "\n".join(map(str, self.csv_data[col])))
                        self.text_boxes[f"Column{idx + 1}"].config(state=tk.DISABLED)

                messagebox.showinfo("Success", "CSV file uploaded successfully!")
                self.predict_button.config(state=tk.NORMAL)  # Enable Predict button
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload CSV file: {e}")
                self.csv_data = None 
    
    def create_text_boxes(self):
        expected_colums = ["Square Footage", "Bedrooms", "Year Built", "Listed Price"]

        for idx, col in enumerate(expected_colums):
            text_box = tk.Text(self.master, height=20, width=35)
            text_box.grid(row=2, column=idx, padx=5, pady=5)
            self.text_boxes[col] = text_box
            
            # Display CSV data in Text widgets
            self.text_boxes[col].insert(tk.END, self.format_csv_data(col))
            self.text_boxes[col].config(state = tk.DISABLED)
    
    def format_csv_data(self, col):
        # Format CSV data for display in Text widget for a specific column
        formatted_data = f"{col}\n"  # Display column name
        if self.csv_data is not None:
            for value in self.csv_data[col]:
                formatted_data += f"{value}\n"
        return formatted_data
    
    def predict(self):
        if self.csv_data is None:
            messagebox.showerror("Error", "Please upload a CSV file first.")
            return
        
        # Check if CSV file contains required columns
        required_columns = ["Square Footage", "Bedrooms", "Year Built"]
        if not all(col in self.csv_data.columns for col in required_columns):
                messagebox.showerror("Error", "CSV file must contain columns: Square Footage, Bedrooms, Year Built, Listed Price")
                return
        
        csv_columns_stripped = [col.strip() for col in self.csv_data.columns]
        if not all(col in csv_columns_stripped for col in required_columns):
                messagebox.showerror("Error", "CSV file must contain columns: Square Footage, Bedrooms, Year Built, Listed Price")
                return
        
        X = self.csv_data[["Square Footage", "Bedrooms", "Year Built"]].values
        y = self.csv_data["Listed Price"].values.reshape(-1, 1)
        
        model = LinearRegression()
        model.fit(X, y)
        
        y_pred = model.predict(X)
        
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        # Verbal description of correlation coefficient
        correlation_description = ""
        if abs(r2) >= 0.8:
            correlation_description = "Strong" + (" positive" if r2 > 0 else " negative") + " correlation"
        elif abs(r2) >= 0.6:
            correlation_description = "Moderate" + (" positive" if r2 > 0 else " negative") + " correlation"
        elif abs(r2) >= 0.4:
            correlation_description = "Weak" + (" positive" if r2 > 0 else " negative") + " correlation"
        else:
            correlation_description = "No correlation"    
        
        output = f"Predicted Future Value: \n{y_pred[0][0]}\n"
        output += f"\nStandard Error of the Estimate: \n{np.sqrt(mse)}\n"
        output += f"\nCorrelation Coefficient (R^2): \n{r2}\n"
        output += f"\nCorrelation Description: \n{correlation_description}\n"
        output += f"\nBest Fit Regression Line Equation: \ny = {model.coef_[0][0]}(Square Footage) + {model.coef_[0][1]}(Bedrooms) + {model.coef_[0][2]}(Year Built) + {model.intercept_[0]}(Listed Price)\n"
        
        # Output text widget and the output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)
        
        # Centering the text in the output_text widget
        self.output_text.tag_configure("center", justify="center")
        self.output_text.tag_add("center", "1.0", "end")
        self.output_text.config(state=tk.DISABLED)  # Disable editing of output

        # Sorted values for plotting
        sorted_indices = np.argsort(self.csv_data["Square Footage"])
        x_sorted = self.csv_data["Square Footage"][sorted_indices]
        y_pred_sorted = y_pred[sorted_indices]

        # Plotting
        plt.figure(figsize=(8, 6)) #Figure size
        plt.scatter(self.csv_data["Square Footage"], y, color='blue', label='Actual Price')
        plt.plot(x_sorted, y_pred_sorted, color='red', label='Predicted Price')
        plt.xlabel("Square Footage")
        plt.ylabel("Listed Price")
        plt.title("Real Estate Prices Forecasting")
        plt.legend()
        plt.show()
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)

def main():
    root = tk.Tk()
    
    # About window
    about_window = tk.Toplevel(root)
    about_app = AboutWindow(about_window, lambda: [about_window.destroy(), root.deiconify()])
    
    root.withdraw()  # Hide the main window until About is closed
    
    app = RealEstateApp(root)
    root.configure(bg="midnightblue")
    
    root.mainloop()

if __name__ == "__main__":
    main()