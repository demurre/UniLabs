import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from storage import (
    load_data,
    save_data,
    get_access_level_name,
    get_user_access_level,
    set_user_access_level,
    ACCESS_LEVELS,
)
from auth_logic import (
    hash_pw,
    check_variant2_letters,
    verify_password,
    check_password_strength,
    encrypt_password_lg,
)
from questions import question_manager
from demoware_manager import demoware_manager
from bmp_handler import BMPValidator, BMPFile
from vigenere_cipher import VigenereCipher

try:
    from captcha_manager import captcha_manager

    CAPTCHA_AVAILABLE = True
except ImportError:
    CAPTCHA_AVAILABLE = False
    print("Warning: CAPTCHA modules not available")

MAX_ATTEMPTS = 3


class AuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentication System — Version 2")
        self.data = load_data()
        self.attempts = 0
        self.current_user = None
        self.current_session = None
        self.build_login_ui()

    # LOGIN UI
    def build_login_ui(self):
        for w in self.root.winfo_children():
            w.destroy()
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Login to System", font=("TkDefaultFont", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 10)
        )
        ttk.Label(frm, text="Username:").grid(row=1, column=0, sticky=tk.W)
        self.entry_user = ttk.Entry(frm)
        self.entry_user.grid(row=1, column=1, sticky=tk.EW)
        ttk.Label(frm, text="Password:").grid(row=2, column=0, sticky=tk.W)
        self.entry_pw = ttk.Entry(frm, show="*")
        self.entry_pw.grid(row=2, column=1, sticky=tk.EW)
        frm.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Login", command=self.try_login).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            btn_frame, text="Register", command=self.show_register_dialog
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.quit_app).pack(
            side=tk.LEFT, padx=5
        )

        menubar = tk.Menu(self.root)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.show_about)
        helpmenu.add_command(label="Help", command=self.show_help)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.root.config(menu=menubar)

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Authentication System — Version 2\n\n"
            "Software Type: Demoware\n"
            "Limitation: BMP files only\n"
            "Cipher: Vigenere\n\n"
            "Functionality:\n"
            "• 6 users\n"
            "• 3 access levels (USER, MODERATOR, ADMIN)\n"
            "• Vigenere encryption\n"
            "• 10 security questions (3 min retry)\n"
            "• 4 questions per iteration\n"
            "• BMP file processing\n"
            "• Demoware limitation (10 sessions/day)\n"
            "• >8 software features",
        )

    def show_help(self):
        messagebox.showinfo(
            "Help",
            "Authentication System — Version 2\n\n"
            "Access Levels:\n"
            "• USER (0) - basic access\n"
            "• MODERATOR (1) - moderator\n"
            "• ADMIN (2) - administrator\n\n"
            "Main Features:\n"
            "• User authentication\n"
            "• Security system (questions)\n"
            "• Access control management\n"
            "• Password strength analysis\n"
            "• Vigenere encryption\n"
            "• BMP file processing\n"
            "• Demoware limitation\n\n"
            "Note: This is a demo version with feature limitations",
        )

    # REGISTRATION
    def show_register_dialog(self):
        """Register a new user."""
        if len(self.data) >= 6:
            messagebox.showerror(
                "Error", "Maximum 6 users. List is full."
            )
            return

        uname = simpledialog.askstring("Register", "Enter new username:")
        if not uname:
            return

        uname = uname.strip()
        if uname in self.data:
            messagebox.showerror("Error", "Username already exists.")
            return

        self.data[uname] = {
            "password": "",
            "locked": False,
            "restriction": True,
            "access_level": 0,
            "questions_completed": 0,
        }
        save_data(self.data)
        messagebox.showinfo("Done", f"User '{uname}' registered.")

    # LOGIN LOGIC
    def try_login(self):
        user = self.entry_user.get().strip()
        pw = self.entry_pw.get()
        if not user:
            if messagebox.askyesno(
                "No username", "Username not entered. Try again?"
            ):
                return
            else:
                self.quit_app()
                return

        if user not in self.data:
            if messagebox.askyesno(
                "Unknown user",
                f"User '{user}' not found. Try again?",
            ):
                return
            else:
                self.quit_app()
                return

        rec = self.data[user]
        if rec.get("locked"):
            messagebox.showerror("Locked", "Account is locked.")
            return

        if rec.get("password", "") == "":
            messagebox.showinfo("First Login", "You need to set a password.")
            self.set_initial_password(user)
            return

        # Check Demoware restrictions
        can_start, demoware_msg = demoware_manager.start_session(user)
        if not can_start:
            messagebox.showwarning("Demoware Limitation", demoware_msg)
            return

        if verify_password(rec.get("password", ""), pw):
            self.attempts = 0
            self.current_user = user

            # CAPTCHA перевірка (якщо доступна)
            if CAPTCHA_AVAILABLE:
                if not self.verify_captcha(user):
                    return

            self.data = load_data()

            access_level = get_user_access_level(self.data, user)
            if access_level == 2:  # ADMIN
                self.open_admin_panel()
            elif access_level == 1:  # MODERATOR
                self.open_moderator_panel()
            else:  # USER
                self.open_user_panel()
        else:
            self.attempts += 1
            if self.attempts >= MAX_ATTEMPTS:
                messagebox.showerror(
                    "Exit",
                    "Too many failed attempts. Application is closing.",
                )
                self.quit_app()
            else:
                messagebox.showerror(
                    "Invalid Password",
                    f"Invalid password. Attempts {self.attempts}/{MAX_ATTEMPTS}.",
                )

    # CAPTCHA VERIFICATION
    def verify_captcha(self, user: str) -> bool:
        """
        Запускає CAPTCHA верифікацію користувача.
        Повертає True якщо верифікація пройдена, False в іншому разі.
        """
        # Починаємо CAPTCHA сеанс
        success, message = captcha_manager.start_verification(user)

        if not success:
            remaining_seconds = captcha_manager.get_session(
                user
            ).get_retry_remaining_time()
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            messagebox.showwarning(
                "CAPTCHA",
                f"Wait {minutes}m {seconds}s before next CAPTCHA verification",
            )
            return False

        # Створюємо вікно для CAPTCHA верифікації
        return self.show_captcha_window(user)

    def show_captcha_window(self, user: str) -> bool:
        """
        Shows CAPTCHA window for verification.
        Returns True if user successfully passed verification.
        """
        captcha_win = tk.Toplevel(self.root)
        captcha_win.title("CAPTCHA Verification")
        captcha_win.geometry("400x350")
        captcha_win.resizable(False, False)
        captcha_win.grab_set()
        
        # Position window in center of parent window
        captcha_win.transient(self.root)
        captcha_win.lift()

        frm = ttk.Frame(captcha_win, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frm, text="CAPTCHA Verification", font=("TkDefaultFont", 14, "bold")
        ).pack(pady=10)

        # Show CAPTCHA image
        try:
            from PIL import Image, ImageTk

            img = captcha_manager.get_captcha_image(user)
            if img:
                img_tk = ImageTk.PhotoImage(img)
                img_label = ttk.Label(frm, image=img_tk)
                img_label.image = img_tk
                img_label.pack(pady=10)
            else:
                ttk.Label(frm, text="(CAPTCHA image)").pack(pady=10)
        except ImportError:
            ttk.Label(
                frm, text="(CAPTCHA image not available - Pillow required)"
            ).pack(pady=10)
        except Exception as e:
            ttk.Label(frm, text=f"Error: {str(e)}").pack(pady=10)

        ttk.Label(frm, text="Enter text from image:", font=("TkDefaultFont", 10)).pack(pady=5)

        entry_captcha = ttk.Entry(frm, width=30)
        entry_captcha.pack(pady=5)
        entry_captcha.focus()

        def submit_captcha():
            user_input = entry_captcha.get().strip()
            success, message = captcha_manager.verify_captcha(user, user_input)

            if success:
                messagebox.showinfo("CAPTCHA", message)
                captcha_win.destroy()
                return
            else:
                messagebox.showerror("CAPTCHA", message)
                if "exhausted" in message.lower():
                    captcha_win.destroy()
                    return
                else:
                    entry_captcha.delete(0, tk.END)
                    entry_captcha.focus()

        def on_window_close():
            if not captcha_manager.is_verified(user):
                messagebox.showwarning("Cancel", "CAPTCHA verification not passed.")
            captcha_win.destroy()

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Verify", command=submit_captcha).pack(
            side=tk.LEFT, padx=8
        )
        ttk.Button(btn_frame, text="Cancel", command=on_window_close).pack(
            side=tk.LEFT, padx=8
        )

        captcha_win.protocol("WM_DELETE_WINDOW", on_window_close)
        captcha_win.wait_window()

        # Повертаємо результат верифікації
        return captcha_manager.is_verified(user)

    # PASSWORD SETUP
    def set_initial_password(self, user):
        while True:
            p1 = simpledialog.askstring(
                "Set Password", "Enter password:", show="*"
            )
            if p1 is None:
                if messagebox.askyesno("Cancel", "Exit?"):
                    self.quit_app()
                    return
                else:
                    continue

            is_strong, strength_msg = check_password_strength(p1)
            if not is_strong:
                if not messagebox.askyesno(
                    "Warning", f"{strength_msg}. Use anyway?"
                ):
                    continue

            p2 = simpledialog.askstring(
                "Confirm", "Confirm password:", show="*"
            )
            if p2 is None:
                messagebox.showinfo(
                    "Confirm", "No confirmation entered. Try again."
                )
                continue
            if p1 != p2:
                messagebox.showerror("Error", "Passwords do not match.")
                continue
            if self.data[user].get("restriction", False) and not check_variant2_letters(
                p1
            ):
                if messagebox.askyesno(
                    "Mismatch",
                    "Password must contain lowercase and uppercase letters. Try another?",
                ):
                    continue
                else:
                    self.quit_app()
                    return
            self.data[user]["password"] = hash_pw(p1)
            save_data(self.data)
            messagebox.showinfo("Done", "Password set.")
            return

    # ADMIN PANEL
    def open_admin_panel(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title("ADMIN — Panel")
        frm = ttk.Frame(self.root, padding=8)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(
            frm, text="Administration Panel", font=("TkDefaultFont", 12, "bold")
        ).pack(side=tk.TOP, anchor=tk.W)

        btns = ttk.Frame(frm)
        btns.pack(fill=tk.X, pady=6)
        ttk.Button(
            btns, text="Change Password", command=self.change_admin_password
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="Add User", command=self.add_user).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btns, text="Block/Unblock", command=self.toggle_lock_selected).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(
            btns,
            text="Change Access Level",
            command=self.change_access_level_selected,
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="Test BMP", command=self.test_bmp_handler).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btns, text="Test Vigenere", command=self.test_vigenere).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btns, text="Refresh", command=self.refresh_user_list).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btns, text="Exit", command=self.quit_app).pack(
            side=tk.RIGHT, padx=4
        )

        list_frame = ttk.Frame(frm)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=6)
        self.user_list = tk.Listbox(list_frame, height=12)
        self.user_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.user_list.yview
        )
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.user_list.config(yscrollcommand=scrollbar.set)
        self.user_list.bind("<<ListboxSelect>>", lambda e: self.show_selected_info())

        right = ttk.Frame(list_frame, padding=(8, 0))
        right.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(right, text="Information:").pack(anchor=tk.NW)
        self.info_text = tk.Text(right, width=40, height=10, state=tk.DISABLED)
        self.info_text.pack()

        nav = ttk.Frame(frm)
        nav.pack(fill=tk.X, pady=4)
        ttk.Button(
            nav, text="To Beginning", command=lambda: self.user_list.yview_moveto(0)
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            nav, text="To End", command=lambda: self.user_list.yview_moveto(1)
        ).pack(side=tk.LEFT, padx=4)

        self.refresh_user_list()

    def refresh_user_list(self):
        self.data = load_data()
        self.user_list.delete(0, tk.END)
        for uname in sorted(self.data.keys()):
            rec = self.data[uname]
            status = []
            if rec.get("locked"):
                status.append("🔒")
            level_name = get_access_level_name(rec.get("access_level", 0))
            status.append(level_name)
            self.user_list.insert(tk.END, f"{uname:12} {' '.join(status)}")

    def show_selected_info(self):
        sel = self.user_list.curselection()
        if not sel:
            return
        idx = sel[0]
        item = self.user_list.get(idx).split()[0]
        uname = item
        rec = self.data.get(uname, {})
        level_name = get_access_level_name(rec.get("access_level", 0))
        info = (
            f"Name: {uname}\n"
            f"Locked: {'Yes' if rec.get('locked') else 'No'}\n"
            f"Access Level: {level_name}\n"
            f"Password: {'Set' if rec.get('password') else 'Not Set'}\n"
            f"Questions Completed: {rec.get('questions_completed', 0)}"
        )
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)

    def add_user(self):
        if len(self.data) >= 6:
            messagebox.showerror("Error", "Maximum 6 users.")
            return

        uname = simpledialog.askstring("New User", "Enter unique name:")
        if not uname:
            return
        uname = uname.strip()
        if uname in self.data:
            messagebox.showerror("Error", "User already exists.")
            return
        self.data[uname] = {
            "password": "",
            "locked": False,
            "restriction": True,
            "access_level": 0,
            "questions_completed": 0,
        }
        save_data(self.data)
        messagebox.showinfo("Done", f"User '{uname}' added.")
        self.refresh_user_list()

    def toggle_lock_selected(self):
        sel = self.user_list.curselection()
        if not sel:
            messagebox.showinfo("Selection", "Select a user.")
            return
        idx = sel[0]
        item = self.user_list.get(idx).split()[0]
        uname = item
        if uname == "ADMIN" and not messagebox.askyesno(
            "Warning", "Continue changing ADMIN lock status?"
        ):
            return
        self.data[uname]["locked"] = not self.data[uname].get("locked", False)
        save_data(self.data)
        self.refresh_user_list()

    def change_access_level_selected(self):
        """Changes the access level of a user."""
        sel = self.user_list.curselection()
        if not sel:
            messagebox.showinfo("Selection", "Select a user.")
            return
        idx = sel[0]
        item = self.user_list.get(idx).split()[0]
        uname = item

        level_str = simpledialog.askstring(
            "Access Level",
            f"Enter access level for '{uname}':\n"
            f"0 - USER\n"
            f"1 - MODERATOR\n"
            f"2 - ADMIN",
        )

        if level_str is None:
            return

        try:
            new_level = int(level_str)
            if new_level in ACCESS_LEVELS:
                set_user_access_level(self.data, uname, new_level)
                save_data(self.data)
                messagebox.showinfo(
                    "Done", f"Access level changed to {ACCESS_LEVELS[new_level]}"
                )
                self.refresh_user_list()
            else:
                messagebox.showerror("Error", "Invalid access level.")
        except ValueError:
            messagebox.showerror("Error", "Enter a number (0, 1, or 2).")

    def change_admin_password(self):
        old = simpledialog.askstring(
            "Old Password", "Enter old password:", show="*"
        )
        if old is None:
            return
        if not verify_password(self.data["ADMIN"].get("password", ""), old):
            messagebox.showerror("Error", "Old password is incorrect.")
            return
        while True:
            p1 = simpledialog.askstring(
                "New Password", "Enter new password:", show="*"
            )
            if p1 is None:
                return

            is_strong, strength_msg = check_password_strength(p1)
            if not is_strong and not messagebox.askyesno(
                "Warning", f"{strength_msg}. Use anyway?"
            ):
                continue

            p2 = simpledialog.askstring(
                "Confirmation", "Confirm new password:", show="*"
            )
            if p2 is None:
                return
            if p1 != p2:
                messagebox.showerror("Error", "Passwords do not match.")
                continue
            if self.data["ADMIN"].get(
                "restriction", False
            ) and not check_variant2_letters(p1):
                messagebox.showerror(
                    "Error", "Password must contain lowercase and uppercase letters."
                )
                continue
            self.data["ADMIN"]["password"] = hash_pw(p1)
            save_data(self.data)
            messagebox.showinfo("Done", "Password changed.")
            return

    # MODERATOR PANEL
    def open_moderator_panel(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title(f"{self.current_user} — Panel (MODERATOR)")
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(
            frm,
            text=f"Moderator Panel — {self.current_user}",
            font=("TkDefaultFont", 12, "bold"),
        ).pack(anchor=tk.W)

        ttk.Button(frm, text="Change Password", command=self.change_user_password).pack(
            pady=6, anchor=tk.W
        )
        ttk.Button(
            frm, text="Pass Security Check", command=self.start_security_questions
        ).pack(pady=6, anchor=tk.W)
        ttk.Button(
            frm, text="View Users", command=self.view_users_limited
        ).pack(pady=6, anchor=tk.W)
        ttk.Button(frm, text="Exit", command=self.quit_app).pack(
            pady=6, anchor=tk.W
        )

    def view_users_limited(self):
        """Moderator can view the user list (without changes)."""
        messagebox.showinfo(
            "Users",
            "User List:\n"
            + "\n".join([f"• {u}" for u in sorted(self.data.keys())]),
        )

    # USER PANEL
    def open_user_panel(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title(f"{self.current_user} — Panel")
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(
            frm,
            text=f"Welcome, {self.current_user}",
            font=("TkDefaultFont", 12, "bold"),
        ).pack(anchor=tk.W)
        ttk.Button(frm, text="Change Password", command=self.change_user_password).pack(
            pady=6, anchor=tk.W
        )
        ttk.Button(
            frm, text="Pass Security Check", command=self.start_security_questions
        ).pack(pady=6, anchor=tk.W)
        ttk.Button(frm, text="Exit", command=self.quit_app).pack(
            pady=6, anchor=tk.W
        )

    def change_user_password(self):
        user = self.current_user
        old = simpledialog.askstring(
            "Old Password", "Enter old password:", show="*"
        )
        if old is None:
            return
        if not verify_password(self.data[user].get("password", ""), old):
            messagebox.showerror("Error", "Old password is incorrect.")
            return
        while True:
            p1 = simpledialog.askstring(
                "New Password", "Enter new password:", show="*"
            )
            if p1 is None:
                return

            is_strong, strength_msg = check_password_strength(p1)
            if not is_strong and not messagebox.askyesno(
                "Warning", f"{strength_msg}. Use anyway?"
            ):
                continue

            p2 = simpledialog.askstring(
                "Confirmation", "Confirm new password:", show="*"
            )
            if p2 is None:
                return
            if p1 != p2:
                messagebox.showerror("Error", "Passwords do not match.")
                continue
            if self.data[user].get("restriction", False) and not check_variant2_letters(
                p1
            ):
                if messagebox.askyesno(
                    "Mismatch",
                    "Password must contain lowercase and uppercase letters. Try another?",
                ):
                    continue
                else:
                    return
            self.data[user]["password"] = hash_pw(p1)
            save_data(self.data)
            messagebox.showinfo("Done", "Password changed.")
            return

    # SECURITY QUESTIONS
    def start_security_questions(self):
        """Starts the security question system."""
        user = self.current_user
        can_start, message = question_manager.start_session(user)

        if not can_start:
            remaining = question_manager.sessions[user].get_remaining_time()
            minutes = remaining // 60
            seconds = remaining % 60
            messagebox.showwarning(
                "Wait",
                f"You have already passed the check.\n"
                f"Time remaining until next iteration: {minutes}m {seconds}s.",
            )
            return

        self.show_security_question(user, 0)

    def show_security_question(self, user, question_index):
        """Shows a security question to the user."""
        session = question_manager.sessions[user]

        if question_index >= len(session.current_questions):
            correct, total, passed = session.end_session()
            self.data = load_data()
            self.data[user]["questions_completed"] = correct
            save_data(self.data)

            result_msg = (
                f"Result: {correct}/{total}\n"
                f"Status: {'✓ Passed' if passed else '✗ Failed'}"
            )
            messagebox.showinfo("Complete", result_msg)
            return

        question_obj = session.current_questions[question_index]
        answer = simpledialog.askstring(
            f"Question {question_index + 1}/{len(session.current_questions)}",
            question_obj.question,
        )

        if answer is None:
            messagebox.showinfo("Cancelled", "Check cancelled.")
            return

        is_correct, message = session.submit_answer(question_index, answer)
        messagebox.showinfo("Result" if is_correct else "Error", message)

        self.show_security_question(user, question_index + 1)

    def quit_app(self):
        self.root.quit()
        try:
            self.root.destroy()
        except:
            pass
        sys.exit(0)

    def test_bmp_handler(self):
        """Validates a BMP file (allows selecting a file from disk)."""
        file_path = filedialog.askopenfilename(
            title="Select file to validate",
            filetypes=[("BMP Files", "*.bmp"), ("All Files", "*.*")],
        )

        if not file_path:
            return

        is_valid, message = BMPValidator.validate_file(file_path)

        if is_valid:
            try:
                bmp = BMPFile(file_path)
                info = bmp.get_info()
                result = (
                    f"✓ File is valid BMP\n\n"
                    f"Path: {file_path}\n"
                    f"File Size: {bmp.get_file_size_kb():.2f} KB\n"
                    f"Resolution: {info['width']}x{info['height']} pixels\n"
                    f"Color Depth: {info['color_format']}\n"
                    f"Total Pixels: {bmp.get_pixel_count():,}"
                )
                messagebox.showinfo("BMP Validation Result", result)
            except Exception as e:
                messagebox.showerror("Error", f"Processing error: {str(e)}")
        else:
            messagebox.showerror("Validation Error", message)

    def test_vigenere(self):
        """Interactive demonstration of the Vigenere cipher."""
        choice = messagebox.askyesnocancel(
            "Vigenere Cipher",
            "Select operation:\n\n"
            "YES - Encrypt text\n"
            "NO - Decrypt text\n"
            "CANCEL - Cancel",
        )

        if choice is None:
            return

        if choice:  # Encryption
            plaintext = simpledialog.askstring(
                "Vigenere Encryption", "Enter text to encrypt:"
            )
            if not plaintext:
                return

            password = simpledialog.askstring(
                "Vigenere Encryption", "Enter password/key:"
            )
            if not password:
                return

            try:
                key = VigenereCipher.generate_key_from_password(
                    password, len(plaintext)
                )
                cipher = VigenereCipher(key)
                encrypted = cipher.encrypt(plaintext)

                result = (
                    f"ENCRYPTED\n\n"
                    f"Original Text: {plaintext}\n"
                    f"Password: {password}\n"
                    f"Key (derived): {key}\n"
                    f"Result: {encrypted}"
                )
                messagebox.showinfo("Encryption Result", result)
            except Exception as e:
                messagebox.showerror("Error", f"Encryption error: {str(e)}")

        else:  # Decryption
            ciphertext = simpledialog.askstring(
                "Vigenere Decryption", "Enter encrypted text:"
            )
            if not ciphertext:
                return

            password = simpledialog.askstring(
                "Vigenere Decryption", "Enter password/key:"
            )
            if not password:
                return

            try:
                key = VigenereCipher.generate_key_from_password(
                    password, len(ciphertext)
                )
                cipher = VigenereCipher(key)
                decrypted = cipher.decrypt(ciphertext)

                result = (
                    f"DECRYPTED\n\n"
                    f"Encrypted Text: {ciphertext}\n"
                    f"Password: {password}\n"
                    f"Key (derived): {key}\n"
                    f"Result: {decrypted}"
                )
                messagebox.showinfo("Decryption Result", result)
            except Exception as e:
                messagebox.showerror("Error", f"Decryption error: {str(e)}")
