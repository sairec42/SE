import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import datetime

# Update get_menu to include an optional `current_hour` argument
def get_menu(current_hour=None):
    if current_hour is None:
        current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        return {
            "Main Dishes": {
                "Idli": 30.00,
                "Dosa": 40.00,
                "Masala Dosa": 50.00,
                "Upma": 35.00,
                "Pongal": 40.00,
                "Vada": 20.00,
            },
            "Side Dishes": {
                "3 varieties of Chutney": 0.00,
                "Sambar": 0.00,
                "Vadacurry": 0.00,
                "Tea": 15.00,
                "Coffee": 20.00,
            }
        }
    elif current_hour < 16:
        return {
            "Main Dishes": {
                "Sambar Rice": 60.00,
                "Fried Rice": 70.00,
                "Curd Rice": 50.00,
                "Parotta with Curry": 80.00,
                "Chicken Biryani": 230.00,
                "Mutton Biriyani": 250.00,
                "Fish Biriyani": 190.00,
                "Vegetable Biryani": 120.00,
                "Pulao": 80.00,
            },
            "Side Dishes": {
                "Raita": 0.00,
                "Papad": 0.00,
                "Salad": 0.00,
                "Pickle": 0.00,
                "Paneer Butter Masala": 150.00,
                "Chicken Butter Masala": 225.00,
                "Kadai Chicken": 180.00,
                "Chicken Chettinadu Gravy": 175.00,
                "Mutton Chukka": 180.00,
            }
        }
    elif current_hour < 19:
        return {
            "Main Dishes": {
                "Samosa": 15.00,
                "Pani Puri": 10.00,
                "Bhaji": 20.00,
                "Bhelpuri": 25.00,
            },
            "Side Dishes": {
                "Tea": 15.00,
                "Coffee": 20.00,
                "Chutney": 0.00,
            }
        }
    else:
        return {
            "Main Dishes": {
                "Naan": 25.00,
                "Butter Naan": 25.00,
                "Vegetable Biryani": 100.00,
                "Chole Bhature": 80.00,
                "Parotta": 25.00,
                "Egg Curry": 120.00,
                "Fish Curry": 180.00,
            },
            "Side Dishes": {
                "Kadai Chicken": 180.00,
                "Chicken Chettinadu Gravy": 175.00,
                "Mutton Chukka": 180.00,
                "Paneer Butter Masala": 150.00,
                "Chicken Butter Masala": 225.00,
                "Gulab Jamun": 0.00,
                "Raita": 0.00,
                "Salad": 0.00,
            }
        }

class FoodOrderingApp:
    def __init__(self, master):
        self.master = master
        master.title("Quickbite Food Menu")
        master.geometry("400x600")
        master.config(bg="#f0f8ff")
        
        title_label = tk.Label(master, text="Quickbite Food Menu", font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#333")
        title_label.pack(pady=10)
        
        self.label = tk.Label(master, text="Select your food and quantity:", font=("Helvetica", 14), bg="#f0f8ff")
        self.label.pack(pady=5)
        
        # Load menu based on current hour
        self.menu = get_menu()
        self.selected_foods = []
        self.menu_frame = tk.Frame(master, bg="#f0f8ff")
        self.menu_frame.pack(pady=10)
        
        # Store variables for food items
        self.food_vars = {}
        
        # Generate menu interface
        for category, items in self.menu.items():
            category_label = tk.Label(self.menu_frame, text=category, font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#006400")
            category_label.pack(pady=5)
            
            for food, price in items.items():
                food_frame = tk.Frame(self.menu_frame, bg="#f0f8ff")
                food_frame.pack(anchor=tk.W, pady=2)
                
                var = tk.BooleanVar()
                quantity_var = tk.StringVar()  # Allow empty input initially
                self.food_vars[food] = (var, price, quantity_var)
                
                check_button = tk.Checkbutton(food_frame, text=f"{food} - ₹{price:.2f}" if price > 0 else f"{food} (Free)", variable=var, bg="#f0f8ff", font=("Helvetica", 12))
                check_button.pack(side=tk.LEFT)
                
                quantity_entry = tk.Entry(food_frame, textvariable=quantity_var, width=5, font=("Helvetica", 12))
                quantity_entry.pack(side=tk.LEFT, padx=5)
        
        # Proceed button
        self.proceed_button = tk.Button(master, text="Proceed", command=self.proceed_order, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        self.proceed_button.pack(pady=20)
        
    def proceed_order(self):
        # Get selected items
        self.selected_foods = [food for food, (var, price, qty) in self.food_vars.items() if var.get()]
        
        if not self.selected_foods:
            messagebox.showwarning("No Selection", "Please select at least one food item.")
            return
        
        order_details = []
        total_price = 0
        
        for food in self.selected_foods:
            qty_var = self.food_vars[food][2]
            try:
                quantity = int(qty_var.get())
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Quantity", f"Please enter a valid quantity for {food}.")
                return
            
            price = self.food_vars[food][1]
            subtotal = price * quantity if price > 0 else 0
            order_details.append(f"{food} - ₹{subtotal:.2f} (Qty: {quantity})" if price > 0 else f"{food} (Free)")
            total_price += subtotal
        
        order_summary = "Order:\n" + "\n".join(order_details) + f"\n\nTotal: ₹{total_price:.2f}"
        self.generate_qr_code(order_summary)
        
    def generate_qr_code(self, order_details):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(order_details)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save("qr_code.png")
        self.show_qr_code()
    
    def show_qr_code(self):
        # Show QR code in new window
        qr_window = tk.Toplevel(self.master)
        qr_window.title("Your QR Code")
        qr_image = Image.open("qr_code.png")
        qr_photo = ImageTk.PhotoImage(qr_image)
        qr_label = tk.Label(qr_window, image=qr_photo)
        qr_label.image = qr_photo
        qr_label.pack()
        
        done_button = tk.Button(qr_window, text="Done", command=qr_window.destroy, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        done_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodOrderingApp(root)
    root.mainloop()
