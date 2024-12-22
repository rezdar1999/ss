import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('rezdar_financial.db')
    cursor = conn.cursor()

    # إنشاء الجداول
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender_name TEXT,
                        recipient_name TEXT,
                        sender_phone TEXT,
                        recipient_phone TEXT,
                        destination TEXT,
                        amount REAL,
                        currency TEXT,
                        commission_status TEXT,
                        is_received INTEGER DEFAULT 0)''')

    # إضافة المستخدم الافتراضي
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('rezdar', '1234'))

    conn.commit()
    conn.close()

# وظيفة تسجيل الدخول
def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('rezdar_financial.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        main_window()
    else:
        messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")

# النافذة الرئيسية للتطبيق
def main_window():
    login_window.destroy()
    root = tk.Tk()
    root.title("خدمات ريزدار المالية")
    root.geometry("900x700")
    root.configure(bg="#f0f0f0")

    # قائمة التنقل
    menu = tk.Menu(root)
    root.config(menu=menu)

    def open_send_section():
        clear_content()
        tk.Label(content_frame, text="قسم الإرسال", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        # إضافة الحقول لقسم الإرسال
        tk.Label(content_frame, text="رقم الإشعار (تلقائي):", bg="#f0f0f0").pack(pady=5)
        tk.Label(content_frame, text="سيتم إنشاؤه تلقائيًا", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

        tk.Label(content_frame, text="اسم المرسل:", bg="#f0f0f0").pack(pady=5)
        sender_name_entry = tk.Entry(content_frame, font=("Arial", 12), relief=tk.SUNKEN, bd=3)
        sender_name_entry.pack(pady=5)

        tk.Label(content_frame, text="اسم المستلم:", bg="#f0f0f0").pack(pady=5)
        recipient_name_entry = tk.Entry(content_frame, font=("Arial", 12), relief=tk.SUNKEN, bd=3)
        recipient_name_entry.pack(pady=5)

        tk.Label(content_frame, text="رقم هاتف المرسل:", bg="#f0f0f0").pack(pady=5)
        sender_phone_entry = tk.Entry(content_frame, font=("Arial", 12), relief=tk.SUNKEN, bd=3)
        sender_phone_entry.pack(pady=5)

        tk.Label(content_frame, text="رقم هاتف المستلم:", bg="#f0f0f0").pack(pady=5)
        recipient_phone_entry = tk.Entry(content_frame, font=("Arial", 12), relief=tk.SUNKEN, bd=3)
        recipient_phone_entry.pack(pady=5)

        tk.Label(content_frame, text="الوجهة:", bg="#f0f0f0").pack(pady=5)
        destination_entry = tk.Entry(content_frame, font=("Arial", 12), relief=tk.SUNKEN, bd=3)
        destination_entry.pack(pady=5)

        tk.Label(content_frame, text="المبلغ:", bg="#f0f0f0").pack(pady=5)
        amount_entry = tk.Entry(content_frame, font=("Arial", 12), relief=tk.SUNKEN, bd=3)
        amount_entry.pack(pady=5)

        tk.Label(content_frame, text="العملة:", bg="#f0f0f0").pack(pady=5)
        currency_combobox = ttk.Combobox(content_frame, values=["دولار", "يورو", "ليرة", "دينار"], font=("Arial", 12))
        currency_combobox.pack(pady=5)

        tk.Label(content_frame, text="حالة العمولة:", bg="#f0f0f0").pack(pady=5)
        commission_combobox = ttk.Combobox(content_frame, values=["تم استلام العمولة", "لم يتم استلام العمولة"], font=("Arial", 12))
        commission_combobox.pack(pady=5)

        def save_transaction():
            conn = sqlite3.connect('rezdar_financial.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO transactions (sender_name, recipient_name, sender_phone, recipient_phone, destination, amount, currency, commission_status) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (sender_name_entry.get(), recipient_name_entry.get(), sender_phone_entry.get(), recipient_phone_entry.get(),
                            destination_entry.get(), amount_entry.get(), currency_combobox.get(), commission_combobox.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("نجاح", "تم إرسال المعاملة بنجاح")
            open_send_section()

        tk.Button(content_frame, text="إرسال", font=("Arial", 12), bg="#007bff", fg="white", relief=tk.RAISED, bd=3, command=save_transaction).pack(pady=20)

    def open_receive_section():
        clear_content()
        tk.Label(content_frame, text="قسم الاستلام", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(content_frame, text="رقم الإشعار:", bg="#f0f0f0").pack(pady=5)
        notification_id_entry = tk.Entry(content_frame, font=("Arial", 12), relief=tk.SUNKEN, bd=3)
        notification_id_entry.pack(pady=5)

        def search_transaction():
            conn = sqlite3.connect('rezdar_financial.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE id = ?", (notification_id_entry.get(),))
            transaction = cursor.fetchone()
            conn.close()

            if transaction:
                clear_content()
                tk.Label(content_frame, text="بيانات المعاملة", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

                fields = ["رقم الإشعار", "اسم المرسل", "اسم المستلم", "رقم هاتف المرسل", "رقم هاتف المستلم", "الوجهة", "المبلغ", "العملة", "حالة العمولة", "تم الاستلام"]
                for field, value in zip(fields, transaction):
                    tk.Label(content_frame, text=f"{field}: {value}", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)

                def mark_received():
                    conn = sqlite3.connect('rezdar_financial.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE transactions SET is_received = 1 WHERE id = ?", (transaction[0],))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("نجاح", "تم تحديد المعاملة كمستلمة")
                    open_receive_section()

                tk.Button(content_frame, text="تم الاستلام", font=("Arial", 12), bg="#28a745", fg="white", relief=tk.RAISED, bd=3, command=mark_received).pack(pady=20)
            else:
                messagebox.showerror("خطأ", "لم يتم العثور على المعاملة")

        tk.Button(content_frame, text="بحث", font=("Arial", 12), bg="#007bff", fg="white", relief=tk.RAISED, bd=3, command=search_transaction).pack(pady=10)

    def open_accounts_section():
        clear_content()
        tk.Label(content_frame, text="قسم الحسابات", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

    def open_settings_section():
        clear_content()
        tk.Label(content_frame, text="الإعدادات", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

    def logout():
        root.destroy()
        main()

    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    menu.add_command(label="الإرسال", command=open_send_section)
    menu.add_command(label="الاستلام", command=open_receive_section)
    menu.add_command(label="الحسابات", command=open_accounts_section)
    menu.add_command(label="الإعدادات", command=open_settings_section)
    menu.add_command(label="تسجيل الخروج", command=logout)

    content_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=5)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    tk.Label(content_frame, text="مرحبًا بك في خدمات ريزدار المالية", font=("Arial", 20, "bold"), bg="#ffffff").pack(pady=20)

    root.mainloop()

def main():
    global login_window, username_entry, password_entry

    login_window = tk.Tk()
    login_window.title("خدمات ريزدار المالية - تسجيل الدخول")
    login_window.geometry("500x400")
    login_window.configure(bg="#f0f0f0")

    tk.Label(login_window, text="أهلاً بك في خدمات ريزدار المالية", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=20)

    tk.Label(login_window, text="اسم المستخدم:", bg="#f0f0f0").pack(pady=5)
    username_entry = tk.Entry(login_window, font=("Arial", 12), relief=tk.SUNKEN, bd=3)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="كلمة المرور:", bg="#f0f0f0").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 12), relief=tk.SUNKEN, bd=3)
    password_entry.pack(pady=5)

    tk.Button(login_window, text="تسجيل الدخول", font=("Arial", 12), bg="#007bff", fg="white", relief=tk.RAISED, bd=3, command=login).pack(pady=20)

    login_window.mainloop()

if __name__ == "__main__":
    init_db()
    main()
