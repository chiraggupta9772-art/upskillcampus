"""
GYM MANAGEMENT SYSTEM - GUI + PYTHON DATA ANALYTICS
Beginner-friendly project using Tkinter, Pandas, NumPy and Matplotlib.

Run:
    pip install -r requirements.txt
    python GymManagementSystem.py

Data is stored in three CSV files in the same folder as this program.
The included records are fictional sample data. Replace them with your own
test records before using this as a real gym's record system.
"""

import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMBERS_FILE = os.path.join(BASE_DIR, "members.csv")
PAYMENTS_FILE = os.path.join(BASE_DIR, "payments.csv")
ATTENDANCE_FILE = os.path.join(BASE_DIR, "attendance.csv")

MEMBER_COLUMNS = ["member_id", "name", "phone", "join_date", "plan", "expiry_date", "status"]
PAYMENT_COLUMNS = ["payment_id", "member_id", "payment_date", "amount", "plan", "payment_status"]
ATTENDANCE_COLUMNS = ["attendance_id", "member_id", "attendance_date"]


def ensure_csv_files():
    """Create empty CSV files with headers if they do not exist."""
    for path, columns in [
        (MEMBERS_FILE, MEMBER_COLUMNS),
        (PAYMENTS_FILE, PAYMENT_COLUMNS),
        (ATTENDANCE_FILE, ATTENDANCE_COLUMNS),
    ]:
        if not os.path.exists(path):
            pd.DataFrame(columns=columns).to_csv(path, index=False)


def load_data(path, columns):
    """Read a CSV file safely and return a DataFrame."""
    try:
        df = pd.read_csv(path)
        for column in columns:
            if column not in df.columns:
                df[column] = ""
        return df[columns]
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=columns)


def save_data(df, path):
    """Save a DataFrame back to CSV."""
    df.to_csv(path, index=False)


class GymManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gym Management System")
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f3f5f9")

        ensure_csv_files()
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("Treeview", rowheight=27, font=("Arial", 10))
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.style.configure("TButton", padding=6)

        header = tk.Frame(root, bg="#172554", height=76)
        header.pack(fill="x")
        tk.Label(header, text="FITTRACK  |  GYM MANAGEMENT SYSTEM",
                 bg="#172554", fg="white", font=("Arial", 19, "bold")).pack(
                     side="left", padx=22, pady=20)
        tk.Label(header, text="Member • Payment • Attendance • Analytics",
                 bg="#172554", fg="#cbd5e1", font=("Arial", 10)).pack(
                     side="right", padx=22)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=14)

        self.members_tab = ttk.Frame(self.notebook, padding=12)
        self.payments_tab = ttk.Frame(self.notebook, padding=12)
        self.attendance_tab = ttk.Frame(self.notebook, padding=12)
        self.analytics_tab = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.members_tab, text="Members")
        self.notebook.add(self.payments_tab, text="Payments")
        self.notebook.add(self.attendance_tab, text="Attendance")
        self.notebook.add(self.analytics_tab, text="Analytics")

        self.build_members_tab()
        self.build_payments_tab()
        self.build_attendance_tab()
        self.build_analytics_tab()
        self.refresh_all()

    def make_tree(self, parent, columns, headings):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, pady=(8, 0))
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, width=130, anchor="center")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return tree

    def build_members_tab(self):
        ttk.Label(self.members_tab, text="Member Management",
                  font=("Arial", 16, "bold")).pack(anchor="w")
        form = ttk.LabelFrame(self.members_tab, text="Add a new member", padding=10)
        form.pack(fill="x", pady=10)
        self.member_name = tk.StringVar()
        self.member_phone = tk.StringVar()
        self.member_plan = tk.StringVar(value="Monthly")
        fields = [("Full name", self.member_name), ("Phone", self.member_phone)]
        for i, (label, variable) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=0, column=i*2, padx=5, pady=5, sticky="w")
            ttk.Entry(form, textvariable=variable, width=25).grid(row=0, column=i*2+1, padx=5, pady=5)
        ttk.Label(form, text="Plan").grid(row=0, column=4, padx=5, sticky="w")
        ttk.Combobox(form, textvariable=self.member_plan,
                     values=["Monthly", "Quarterly", "Yearly"],
                     state="readonly", width=14).grid(row=0, column=5, padx=5)
        ttk.Button(form, text="Add Member", command=self.add_member).grid(row=0, column=6, padx=10)
        ttk.Button(form, text="Delete Selected", command=self.delete_member).grid(row=0, column=7, padx=5)
        self.member_tree = self.make_tree(self.members_tab,
            ("member_id","name","phone","join_date","plan","expiry_date","status"),
            ("Member ID","Name","Phone","Join Date","Plan","Expiry Date","Status"))

    def build_payments_tab(self):
        ttk.Label(self.payments_tab, text="Payment Management",
                  font=("Arial", 16, "bold")).pack(anchor="w")
        form = ttk.LabelFrame(self.payments_tab, text="Record a payment", padding=10)
        form.pack(fill="x", pady=10)
        self.pay_member_id = tk.StringVar()
        self.pay_amount = tk.StringVar()
        self.pay_status = tk.StringVar(value="Paid")
        ttk.Label(form, text="Member ID").grid(row=0,column=0,padx=5,pady=5)
        ttk.Entry(form,textvariable=self.pay_member_id,width=18).grid(row=0,column=1,padx=5)
        ttk.Label(form,text="Amount (₹)").grid(row=0,column=2,padx=5)
        ttk.Entry(form,textvariable=self.pay_amount,width=15).grid(row=0,column=3,padx=5)
        ttk.Label(form,text="Status").grid(row=0,column=4,padx=5)
        ttk.Combobox(form,textvariable=self.pay_status,values=["Paid","Pending"],
                     state="readonly",width=12).grid(row=0,column=5,padx=5)
        ttk.Button(form,text="Save Payment",command=self.add_payment).grid(row=0,column=6,padx=10)
        self.payment_tree = self.make_tree(self.payments_tab,
            ("payment_id","member_id","payment_date","amount","plan","payment_status"),
            ("Payment ID","Member ID","Date","Amount (₹)","Plan","Status"))

    def build_attendance_tab(self):
        ttk.Label(self.attendance_tab, text="Attendance Management",
                  font=("Arial", 16, "bold")).pack(anchor="w")
        form = ttk.LabelFrame(self.attendance_tab, text="Mark today's attendance", padding=10)
        form.pack(fill="x", pady=10)
        self.att_member_id = tk.StringVar()
        ttk.Label(form,text="Member ID").pack(side="left",padx=6)
        ttk.Entry(form,textvariable=self.att_member_id,width=20).pack(side="left",padx=6)
        ttk.Button(form,text="Mark Present",command=self.mark_attendance).pack(side="left",padx=8)
        self.attendance_tree = self.make_tree(self.attendance_tab,
            ("attendance_id","member_id","attendance_date"),
            ("Attendance ID","Member ID","Date"))

    def build_analytics_tab(self):
        ttk.Label(self.analytics_tab, text="Gym Analytics Dashboard",
                  font=("Arial", 16, "bold")).pack(anchor="w")
        self.kpi_frame = ttk.Frame(self.analytics_tab)
        self.kpi_frame.pack(fill="x", pady=12)
        self.kpi_labels = {}
        for key, title in [("members","Total Members"),("active","Active Members"),
                           ("revenue","Paid Revenue"),("attendance","Attendance Records")]:
            card = ttk.LabelFrame(self.kpi_frame, text=title, padding=12)
            card.pack(side="left", fill="x", expand=True, padx=5)
            label = ttk.Label(card, text="0", font=("Arial", 17, "bold"))
            label.pack()
            self.kpi_labels[key] = label
        ttk.Button(self.analytics_tab, text="Refresh Analytics",
                   command=self.refresh_analytics).pack(anchor="e", pady=5)
        self.chart_frame = ttk.Frame(self.analytics_tab)
        self.chart_frame.pack(fill="both", expand=True)

    def next_id(self, df, column, prefix):
        numbers = []
        for value in df[column].astype(str):
            if value.startswith(prefix):
                try:
                    numbers.append(int(value[len(prefix):]))
                except ValueError:
                    pass
        return f"{prefix}{(max(numbers, default=0) + 1):03d}"

    def add_member(self):
        name = self.member_name.get().strip()
        phone = self.member_phone.get().strip()
        plan = self.member_plan.get()
        if not name or not phone:
            messagebox.showwarning("Missing information", "Enter both name and phone number.")
            return
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showwarning("Invalid phone", "Enter a valid phone number (at least 10 digits).")
            return
        df = load_data(MEMBERS_FILE, MEMBER_COLUMNS)
        member_id = self.next_id(df, "member_id", "M")
        today = date.today()
        months = {"Monthly": 1, "Quarterly": 3, "Yearly": 12}[plan]
        # Expiry is calculated using a simple 30-day month approximation.
        from datetime import timedelta
        expiry = today + timedelta(days=30 * months)
        new_row = {"member_id":member_id,"name":name,"phone":phone,
                   "join_date":today.isoformat(),"plan":plan,
                   "expiry_date":expiry.isoformat(),"status":"Active"}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df, MEMBERS_FILE)
        self.member_name.set(""); self.member_phone.set("")
        self.refresh_all()
        messagebox.showinfo("Success", f"Member added. ID: {member_id}")

    def delete_member(self):
        selected = self.member_tree.selection()
        if not selected:
            messagebox.showwarning("Select member", "Select a member row first.")
            return
        member_id = self.member_tree.item(selected[0])["values"][0]
        if not messagebox.askyesno("Confirm", f"Delete member {member_id}? Related records will remain in CSV files."):
            return
        df = load_data(MEMBERS_FILE, MEMBER_COLUMNS)
        df = df[df["member_id"].astype(str) != str(member_id)]
        save_data(df, MEMBERS_FILE)
        self.refresh_all()

    def add_payment(self):
        member_id = self.pay_member_id.get().strip()
        amount_text = self.pay_amount.get().strip()
        if not member_id or not amount_text:
            messagebox.showwarning("Missing information", "Enter member ID and amount.")
            return
        members_df = load_data(MEMBERS_FILE, MEMBER_COLUMNS)
        matched = members_df[members_df["member_id"].astype(str) == member_id]
        if matched.empty:
            messagebox.showerror("Unknown member", "This member ID does not exist.")
            return
        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid amount", "Enter an amount greater than zero.")
            return
        df = load_data(PAYMENTS_FILE, PAYMENT_COLUMNS)
        payment_id = self.next_id(df, "payment_id", "P")
        plan = matched.iloc[0]["plan"]
        new_row = {"payment_id":payment_id,"member_id":member_id,
                   "payment_date":date.today().isoformat(),"amount":amount,
                   "plan":plan,"payment_status":self.pay_status.get()}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df, PAYMENTS_FILE)
        self.pay_member_id.set(""); self.pay_amount.set("")
        self.refresh_all()
        messagebox.showinfo("Success", f"Payment saved. ID: {payment_id}")

    def mark_attendance(self):
        member_id = self.att_member_id.get().strip()
        members_df = load_data(MEMBERS_FILE, MEMBER_COLUMNS)
        if members_df[members_df["member_id"].astype(str) == member_id].empty:
            messagebox.showerror("Unknown member", "Enter an existing member ID.")
            return
        df = load_data(ATTENDANCE_FILE, ATTENDANCE_COLUMNS)
        today = date.today().isoformat()
        already = df[(df["member_id"].astype(str) == member_id) &
                     (df["attendance_date"].astype(str) == today)]
        if not already.empty:
            messagebox.showinfo("Already marked", "Attendance is already marked for this member today.")
            return
        attendance_id = self.next_id(df, "attendance_id", "A")
        new_row = {"attendance_id":attendance_id,"member_id":member_id,
                   "attendance_date":today}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df, ATTENDANCE_FILE)
        self.att_member_id.set("")
        self.refresh_all()
        messagebox.showinfo("Success", "Attendance marked.")

    def fill_tree(self, tree, df):
        for item in tree.get_children():
            tree.delete(item)
        for _, row in df.iterrows():
            tree.insert("", "end", values=[row[col] for col in df.columns])

    def refresh_all(self):
        self.fill_tree(self.member_tree, load_data(MEMBERS_FILE, MEMBER_COLUMNS))
        self.fill_tree(self.payment_tree, load_data(PAYMENTS_FILE, PAYMENT_COLUMNS))
        self.fill_tree(self.attendance_tree, load_data(ATTENDANCE_FILE, ATTENDANCE_COLUMNS))
        self.refresh_analytics()

    def refresh_analytics(self):
        members_df = load_data(MEMBERS_FILE, MEMBER_COLUMNS)
        payments_df = load_data(PAYMENTS_FILE, PAYMENT_COLUMNS)
        attendance_df = load_data(ATTENDANCE_FILE, ATTENDANCE_COLUMNS)

        total_members = len(members_df)
        active_members = int((members_df["status"].astype(str).str.lower() == "active").sum())
        if not payments_df.empty:
            payments_df["amount"] = pd.to_numeric(payments_df["amount"], errors="coerce").fillna(0)
            paid_revenue = float(payments_df.loc[
                payments_df["payment_status"].astype(str).str.lower() == "paid", "amount"
            ].sum())
        else:
            paid_revenue = 0.0

        self.kpi_labels["members"].config(text=str(total_members))
        self.kpi_labels["active"].config(text=str(active_members))
        self.kpi_labels["revenue"].config(text=f"₹{paid_revenue:,.0f}")
        self.kpi_labels["attendance"].config(text=str(len(attendance_df)))

        # NumPy example: calculate mean paid transaction amount.
        paid_amounts = np.array(
            payments_df.loc[payments_df["payment_status"].astype(str).str.lower() == "paid", "amount"],
            dtype=float
        ) if not payments_df.empty else np.array([])
        average_payment = float(np.mean(paid_amounts)) if paid_amounts.size else 0.0

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.8))
        if not payments_df.empty:
            status_counts = payments_df["payment_status"].astype(str).value_counts()
            axes[0].bar(status_counts.index, status_counts.values, color=["#2563eb", "#f59e0b"][:len(status_counts)])
            axes[0].set_title("Payment Status")
            axes[0].set_ylabel("Number of Payments")
        else:
            axes[0].text(0.5, 0.5, "No payment data", ha="center", va="center")
            axes[0].set_title("Payment Status")

        if not members_df.empty:
            plan_counts = members_df["plan"].astype(str).value_counts()
            axes[1].pie(plan_counts.values, labels=plan_counts.index,
                        autopct="%1.0f%%", startangle=90)
            axes[1].set_title("Membership Plans")
        else:
            axes[1].text(0.5, 0.5, "No member data", ha="center", va="center")
            axes[1].set_title("Membership Plans")

        fig.suptitle(f"Gym Overview | Average paid transaction: ₹{average_payment:,.0f}")
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)


if __name__ == "__main__":
    root = tk.Tk()
    app = GymManagementApp(root)
    root.mainloop()
