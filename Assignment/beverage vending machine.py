import tkinter as tk
from tkinter import messagebox, simpledialog

class VendingMachineApp:
    def __init__(self, master):
        self.master = master
        master.title("파이썬 자판기")
        master.geometry("800x700")
        master.resizable(False, False)

        self.drinks = {
            "콜라": {"price": 1000, "stock": 10},
            "사이다": {"price": 1000, "stock": 10},
            "환타": {"price": 900, "stock": 10},
            "웰치스": {"price": 900, "stock": 10},
            "물": {"price": 600, "stock": 10},
            "아메리카노": {"price": 1500, "stock": 10},
            "콘트라베이스": {"price": 2100, "stock": 10}
            # 실제 자판기 음료를 여기에 추가하세요.
        }

        self.coins = {
            "500원": 10,
            "100원": 10,
            "50원": 10
        }
        self.bills = {
            "1000원": 0
        }
        self.current_deposit = 0  # 현재 투입된 금액

        # 관리자 비밀번호 (임시)
        self.admin_password = "admin"

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # 상단 프레임 (잔액 표시 및 모드 선택)
        top_frame = tk.Frame(self.master, bd=2, relief="groove", padx=10, pady=10)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.deposit_label = tk.Label(top_frame, text=f"현재 투입 금액: {self.current_deposit}원", font=("Arial", 16, "bold"),
                                      fg="blue")
        self.deposit_label.pack(side="left", padx=10)

        self.mode_frame = tk.Frame(top_frame)
        self.mode_frame.pack(side="right")
        self.customer_mode_btn = tk.Button(self.mode_frame, text="소비자 모드", command=self.switch_to_customer_mode,
                                           font=("Arial", 10))
        self.customer_mode_btn.pack(side="left", padx=5)
        self.admin_mode_btn = tk.Button(self.mode_frame, text="관리자 모드", command=self.check_admin_password,
                                        font=("Arial", 10))
        self.admin_mode_btn.pack(side="left")

        # 음료 선택 프레임 (소비자 모드)
        self.customer_frame = tk.Frame(self.master, bd=2, relief="groove", padx=10, pady=10)
        self.customer_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.drink_buttons_frame = tk.Frame(self.customer_frame)
        self.drink_buttons_frame.pack(pady=10)

        self.drink_buttons = {}
        for i, (drink, data) in enumerate(self.drinks.items()):
            row = i // 3
            col = i % 3
            btn = tk.Button(self.drink_buttons_frame,
                            text=f"{drink}\n({data['price']}원)",
                            width=15, height=5,
                            command=lambda d=drink: self.purchase_drink(d),
                            font=("Arial", 12))
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.drink_buttons[drink] = btn

        # 금액 투입 및 반환 프레임
        self.transaction_frame = tk.Frame(self.customer_frame, bd=2, relief="groove", padx=10, pady=10)
        self.transaction_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.transaction_frame, text="금액 투입:", font=("Arial", 12)).pack(side="left", padx=5)
        tk.Button(self.transaction_frame, text="1000원", command=lambda: self.insert_money(1000),
                  font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(self.transaction_frame, text="500원", command=lambda: self.insert_money(500), font=("Arial", 10)).pack(
            side="left", padx=5)
        tk.Button(self.transaction_frame, text="100원", command=lambda: self.insert_money(100), font=("Arial", 10)).pack(
            side="left", padx=5)
        tk.Button(self.transaction_frame, text="50원", command=lambda: self.insert_money(50), font=("Arial", 10)).pack(
            side="left", padx=5)
        tk.Button(self.transaction_frame, text="잔돈 반환", command=self.return_change, font=("Arial", 12),
                  bg="orange").pack(side="right", padx=5)

        # 관리자 모드 프레임
        self.admin_frame = tk.Frame(self.master, bd=2, relief="groove", padx=10, pady=10)
        # self.admin_frame.pack(fill="both", expand=True, padx=10, pady=5) # 초기에는 숨김

        tk.Label(self.admin_frame, text="--- 관리자 모드 ---", font=("Arial", 16, "bold"), fg="red").pack(pady=10)

        # 재고 관리
        stock_frame = tk.LabelFrame(self.admin_frame, text="재고 관리", padx=10, pady=10)
        stock_frame.pack(fill="x", pady=5)

        self.stock_entries = {}
        for i, (drink, data) in enumerate(self.drinks.items()):
            row = i // 2
            col = (i % 2) * 2  # 레이블과 엔트리를 위한 2열 간격
            tk.Label(stock_frame, text=f"{drink} 재고:", font=("Arial", 10)).grid(row=row, column=col, padx=5, pady=2,
                                                                                sticky="w")
            entry = tk.Entry(stock_frame, width=5, font=("Arial", 10))
            entry.grid(row=row, column=col + 1, padx=5, pady=2, sticky="w")
            entry.insert(0, str(data["stock"]))
            self.stock_entries[drink] = entry

        stock_btn_row = len(self.drinks) // 2 + (len(self.drinks) % 2)
        tk.Button(stock_frame, text="재고 업데이트", command=self.update_stock, font=("Arial", 10), bg="lightgray").grid(
            row=stock_btn_row, column=0, padx=5, pady=10, sticky="ew")  # column=0 추가
        tk.Button(stock_frame, text="재고 보충 (모두 10개)", command=self.refill_drinks, font=("Arial", 10),
                  bg="lightgray").grid(
            row=stock_btn_row, column=1, padx=5, pady=10, sticky="ew")  # column=1 추가

        # 금액 현황
        money_frame = tk.LabelFrame(self.admin_frame, text="금액 현황", padx=10, pady=10)
        money_frame.pack(fill="x", pady=5)

        self.money_labels = {}
        for i, (coin, count) in enumerate(self.coins.items()):
            lbl = tk.Label(money_frame, text=f"{coin}: {count}개", font=("Arial", 10))
            lbl.grid(row=i, column=0, padx=5, pady=2, sticky="ew")  # <--- sticky="ew" 추가
            self.money_labels[coin] = lbl

        for i, (bill, count) in enumerate(self.bills.items()):
            lbl = tk.Label(money_frame, text=f"{bill}: {count}개", font=("Arial", 10))
            lbl.grid(row=i, column=1, padx=5, pady=2, sticky="ew")  # <--- sticky="ew" 추가
            self.money_labels[bill] = lbl

        tk.Button(money_frame, text="금액 수거", command=self.collect_money, font=("Arial", 10), bg="lightgray").grid(
            row=max(len(self.coins), len(self.bills)), column=0, padx=5, pady=10, sticky="ew")
        tk.Button(money_frame, text="잔돈 보충", command=self.refill_charge, font=("Arial", 10), bg="lightgray").grid(
            row=max(len(self.coins), len(self.bills)), column=1, padx=5, pady=10, sticky="ew")
        self.toast_window = None

    def update_display(self):
        self.deposit_label.config(text=f"현재 투입 금액: {self.current_deposit}원")
        for drink, data in self.drinks.items():
            button = self.drink_buttons[drink]
            if data["stock"] == 0:
                button.config(state="disabled", text=f"{drink}\n(품절)", bg="red", fg="white")
            elif self.current_deposit >= data["price"]:
                button.config(state="normal", text=f"{drink}\n({data['price']}원)", bg="lightgreen", fg="black")
            else:
                button.config(state="disabled", text=f"{drink}\n({data['price']}원)", bg="lightgray", fg="black")

        # 관리자 모드 금액 현황 업데이트
        if hasattr(self, 'money_labels'):
            for coin, count in self.coins.items():
                self.money_labels[coin].config(text=f"{coin}: {count}개")
            for bill, count in self.bills.items():
                self.money_labels[bill].config(text=f"{bill}: {count}개")

    def insert_money(self, amount):
        if amount == 1000:
            self.bills["1000원"] += 1
        elif amount == 500:
            self.coins["500원"] += 1
        elif amount == 100:
            self.coins["100원"] += 1
        elif amount == 50:
            self.coins["50원"] += 1
        else:
            messagebox.showerror("오류", "유효하지 않은 금액입니다.")
            return

        self.current_deposit += amount
        self.update_display()

    def refill_charge(self):
        for coin, count in self.coins.items():
            self.coins[coin] += 10
        self.update_display()

    def refill_drinks(self, amount=10):
        for drink_name in self.drinks:
            self.drinks[drink_name]["stock"] += amount

        self.show_toast_message(f"모든 음료 재고가 {amount}개씩 보충되었습니다.", duration_ms=1500)
        self.update_display()
        self.load_admin_data()  # 관리자 모드의 재고 엔트리도 업데이트


    def purchase_drink(self, drink_name):
        drink_info = self.drinks.get(drink_name)
        if not drink_info:
            messagebox.showerror("오류", "알 수 없는 음료입니다.")
            return

        price = drink_info["price"]
        stock = drink_info["stock"]

        if stock <= 0:
            messagebox.showerror("오류", f"{drink_name}은(는) 품절입니다.")
            return

        if self.current_deposit < price:
            messagebox.showerror("오류", "투입 금액이 부족합니다.")
            return

        # 구매 성공
        self.drinks[drink_name]["stock"] -= 1
        self.current_deposit = self.current_deposit - price  # 투입 금액 초기화

        # messagebox.showinfo("구매 성공", f"{drink_name}을(를) 구매했습니다!\n")
        self.show_toast_message(f"{drink_name}을(를) 구매했습니다!\n");
        self.update_display()

    def calculate_change(self, amount):
        change = {
            "500원": 0,
            "100원": 0,
            "50원": 0
        }
        temp_coins = self.coins.copy()

        # 500원
        num_500 = min(amount // 500, temp_coins["500원"])
        change["500원"] = num_500
        amount -= num_500 * 500
        temp_coins["500원"] -= num_500

        # 100원
        num_100 = min(amount // 100, temp_coins["100원"])
        change["100원"] = num_100
        amount -= num_100 * 100
        temp_coins["100원"] -= num_100

        # 50원
        num_50 = min(amount // 50, temp_coins["50원"])
        change["50원"] = num_50
        amount -= num_50 * 50
        temp_coins["50원"] -= num_50

        if amount == 0:
            return change
        else:
            messagebox.showerror("거스름돈 반환", "거스름돈이 부정확하게 나누어 떨어집니다.")
            return None

    def return_change(self):
        if self.current_deposit == 0:
            messagebox.showinfo("잔돈 반환", "반환할 잔돈이 없습니다.")
            return

        change_amount = self.current_deposit
        change_breakdown = self.calculate_change(change_amount)

        if change_breakdown is None:
            messagebox.showerror("잔돈 부족", "자판기 잔돈이 부족하여 반환할 수 없습니다. 관리자에게 문의하세요.")
            return

        change_msg = "잔돈이 반환됩니다:\n"
        for coin, count in change_breakdown.items():
            if count > 0:
                change_msg += f"{coin} {count}개\n"
                # 자판기 내 동전 개수 감소
                self.coins[coin] -= count

        messagebox.showinfo("잔돈 반환", change_msg)
        self.current_deposit = 0
        self.update_display()

        # 다시 자판기 내 동전/지폐 현황을 업데이트해줘야 함 (관리자 모드 대비)
        self.update_admin_money_display()

    def switch_to_customer_mode(self):
        self.admin_frame.pack_forget()
        self.customer_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.update_display()

    def check_admin_password(self):
        self.switch_to_admin_mode()
        # password = simpledialog.askstring("관리자 모드", "비밀번호를 입력하세요:", show='*')
        # if password == self.admin_password:
        #     self.switch_to_admin_mode()
        # else:
        #     messagebox.showerror("오류", "잘못된 비밀번호입니다.")

    def switch_to_admin_mode(self):
        self.customer_frame.pack_forget()
        self.admin_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.load_admin_data()  # 현재 재고 및 금액 현황을 불러옴
        self.update_display()  # 금액 표시 등 업데이트

    def load_admin_data(self):
        # 재고 엔트리 업데이트
        for drink, entry in self.stock_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(self.drinks[drink]["stock"]))

        # 금액 현황 레이블 업데이트
        self.update_admin_money_display()

    def update_admin_money_display(self):
        for coin, count in self.coins.items():
            self.money_labels[coin].config(text=f"{coin}: {count}개")
        for bill, count in self.bills.items():
            self.money_labels[bill].config(text=f"{bill}: {count}개")

    def update_stock(self):
        try:
            for drink, entry in self.stock_entries.items():
                new_stock = int(entry.get())
                if new_stock < 0:
                    raise ValueError("재고는 0보다 작을 수 없습니다.")
                self.drinks[drink]["stock"] = new_stock
            messagebox.showinfo("재고 업데이트", "재고가 성공적으로 업데이트되었습니다.")
            self.update_display()
        except ValueError as e:
            messagebox.showerror("오류", f"유효하지 않은 재고 값입니다: {e}")

    def collect_money(self):
        total_collected = 0
        for coin, count in self.coins.items():
            total_collected += (int(coin.replace("원", "")) * count)
            self.coins[coin] = 0  # 수거 후 0으로 초기화

        for bill, count in self.bills.items():
            total_collected += (int(bill.replace("원", "")) * count)
            self.bills[bill] = 0  # 수거 후 0으로 초기화

        self.show_toast_message(f"총 {total_collected}원이 수거되었습니다.")
        self.update_admin_money_display()
        self.update_display()  # 소비자 모드에도 영향 줄 수 있으므로 업데이트

    def show_toast_message(self, message, duration_ms=2000):
        # 이미 토스트 창이 있다면, 타이머를 취소하고 메시지를 업데이트
        if self.toast_window is not None:
            if self.toast_timer_id:
                self.master.after_cancel(self.toast_timer_id) # 이전 타이머 취소
            self.toast_label.config(text=message) # 메시지 업데이트
            self.update_toast_position(self.toast_window) # 위치 다시 계산 (텍스트 길이에 따라 달라질 수 있으므로)
            self.toast_window.lift() # 최상위로 올림
        else:
            # 토스트 창이 없다면 새로 생성
            self.toast_window = tk.Toplevel(self.master)
            self.toast_window.overrideredirect(True)
            # 투명도 설정 (선택 사항)
            # self.toast_window.attributes('-alpha', 0.9)

            self.toast_label = tk.Label(self.toast_window, text=message, bg="black", fg="white", font=("Arial", 10), padx=10, pady=5)
            self.toast_label.pack(expand=True, fill="both")

            self.update_toast_position(self.toast_window) # 초기 위치 설정

        # 새로운 타이머 설정
        self.toast_timer_id = self.master.after(duration_ms, self._destroy_toast)

    def update_toast_position(self, toast_win):
        # 윈도우 크기 업데이트하여 실제 위젯 크기 반영
        toast_win.update_idletasks()

        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()

        toast_width = toast_win.winfo_width()
        toast_height = toast_win.winfo_height()

        # 오른쪽 하단에 20px 정도 여백을 두고 배치
        x = master_x + master_width - toast_width - 20
        y = master_y + master_height - toast_height - 20

        toast_win.geometry(f"+{x}+{y}")

    def _destroy_toast(self):
        """내부적으로 토스트 창을 파괴하고 관련 변수를 초기화합니다."""
        if self.toast_window:
            self.toast_window.destroy()
            self.toast_window = None
            self.toast_label = None
            self.toast_timer_id = None # 타이머 ID도 초기화


if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineApp(root)
    root.mainloop()