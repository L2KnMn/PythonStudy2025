import tkinter as tk
from tkinter import messagebox, simpledialog

# 1. Drink 클래스 정의
class Drink:
    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def decrease_stock(self, quantity=1):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False

    def is_in_stock(self):
        return self.stock > 0

    def __str__(self): # 디버깅용 문자열 표현
        return f"Drink(id='{self.id}', name='{self.name}', price={self.price}, stock={self.stock})"
    
class CreditCard:
    def __init__(self, id):
        self.id = id
        self.moeny = 0
    
    def add_money(self, price):
        self.moeny += price
    
    def pay(self, price):
        if(self.moeny >= price):
            self.moeny -= price
            return True
        else:
            return False

class VendingMachineApp:
    def __init__(self, master):
        self.master = master
        master.title("한국공학대학교 자판기")
        master.geometry("1200x800")
        master.resizable(False, False)

        # 음료 데이터를 Drink 객체 리스트로 변환하여 초기화
        drinks_data = [
            ## 상열
            {"id": "isis_8.0_1", "name": "아이시스 8.0", "price": 800, "stock": 10},
            {"id": "isis_8.0_2", "name": "아이시스 8.0", "price": 800, "stock": 10},
            {"id": "aqua_zero_1", "name": "아쿠아제로", "price": 2000, "stock": 10},
            {"id": "lemon_water_1", "name": "레몬워터", "price": 1800, "stock": 10},
            {"id": "lemon_water_2", "name": "레몬워터", "price": 1800, "stock": 10},
            {"id": "corn_silk_tea_1", "name": "옥수수수염차", "price": 1300, "stock": 10},
            {"id": "corn_silk_tea_2", "name": "옥수수수염차", "price": 1300, "stock": 10},
            {"id": "golden_barley_1", "name": "황금보리", "price": 1300, "stock": 10},
            {"id": "trevi_1", "name": "트레비", "price": 1300, "stock": 10},
            {"id": "tervi_2", "name": "트레비", "price": 1300, "stock": 10},
            ## 중열
            {"id": "pepsi_zero_lime_can_1", "name": "펩시콜라 제로 라임", "price": 1100, "stock": 10},
            {"id": "pepsi_can_1", "name": "펩시콜라", "price": 1100, "stock": 10},
            {"id": "chilsung_cider_zero_can_1", "name": "칠성사이다 제로", "price": 1300, "stock": 10},
            {"id": "chilsung_cider_can_1", "name": "칠성사이다", "price": 1300, "stock": 10},
            {"id": "delmonte_mango_1", "name": "델몬트 망고", "price": 1200, "stock": 10},
            {"id": "delmonte_mango_2", "name": "델몬트 망고", "price": 1200, "stock": 10},
            {"id": "lipton_peach_1", "name": "립톤 아이스티 복숭아", "price": 1200, "stock": 10},
            {"id": "delmonte_apple_ade_1", "name": "델몬트 사과 에이드", "price": 1100, "stock": 10},
            {"id": "delmonte_apple_ade_2", "name": "델몬트 사과 에이드", "price": 1100, "stock": 10},
            {"id": "delmonte_grape_ade_1", "name": "델몬트 포도 에이드", "price": 1100, "stock": 10},
            ## 하열
            {"id": "ganachoco_1", "name": "가나초코", "price": 900, "stock": 10},
            {"id": "letsbe_mild_1", "name": "레쓰비", "price": 900, "stock": 10},
            {"id": "hot6_zero_1", "name": "HOT6 제로", "price": 1300, "stock": 10},
            {"id": "milkis_1", "name": "밀키스", "price": 1100, "stock": 10},
            {"id": "hot6_1", "name": "HOT6", "price": 1300, "stock": 10},
            {"id": "letsbe_cafetime_1", "name": "레쓰비 카페타임", "price": 1200, "stock": 10},
            {"id": "gatorade_lemon_1", "name": "게토레이 레몬", "price": 1000, "stock": 10},
            {"id": "gatorade_lemon_2", "name": "게토레이 레몬", "price": 1000, "stock": 10},
            {"id": "cocofarm_grape_1", "name": "코코팜 포도", "price": 1000, "stock": 10},
            {"id": "sikhye_1", "name": "잔치집 식혜", "price": 1000, "stock": 10}
        ]
        # drink 객체로 생성
        self.drinks = [Drink(d["id"], d["name"], d["price"], d["stock"]) for d in drinks_data]
        
        # 보유 금액
        self.coins = { "500원": 10, "100원": 10, "50원": 10 } # 초기 거스름 돈
        self.bills = { "1만원": 0, "5000원": 0, "1000원": 0 } 

        # 매핑
        self.money_unit_map = {
            10000: "1만원", 5000: "5000원", 1000: "1000원",
            500: "500원", 100: "100원", 50: "50원"
        }

        self.current_deposit = 0
        self.total_collected_money = 0
        self.total_refilled_money = 0
        self.admin_password = "1234"


        self.users_card = CreditCard(0)
        self.users_card.add_money(50000)
 
        # 카드 관련 변수
        self.card = None # 꽂힌 카드  
        self.card_inserted = False
        self.card_button = None
        self.card_status_label = None

        self.drink_buttons = {}
        self.stock_entries = {}
        self.toast_window = None
        self.toast_timer_id = None

        self.create_widgets()
        self.update_display()

    def profit(self):
        return self.total_collected_money - self.total_refilled_money

    def get_drink_by_id(self, drink_id):
        for drink_obj in self.drinks: # 이제 drink_obj는 Drink 객체
            if drink_obj.id == drink_id:
                return drink_obj
        return None

    def create_widgets(self):
        top_frame = tk.Frame(self.master, bd=2, relief="flat", padx=10, pady=10)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.deposit_label = tk.Label(top_frame, text=f"투입 금액: {self.current_deposit}원", font=("Malgun Gothic", 16, "bold"),
                                      fg="white", bg="#333333", width=18, relief="sunken", bd=2)
        self.deposit_label.pack(side="left", padx=10, pady=5)

        self.card_status_label = tk.Label(top_frame, text="카드 미사용", font=("Malgun Gothic", 10),
                                          fg="#555555", width=18, anchor="w")
        self.card_status_label.pack(side="left", padx=5, pady=5)

        self.mode_frame = tk.Frame(top_frame)
        self.mode_frame.pack(side="right", padx=10)
        self.customer_mode_btn = tk.Button(self.mode_frame, text="소비자 모드", command=self.switch_to_customer_mode,
                                           font=("Malgun Gothic", 10), width=10)
        self.customer_mode_btn.pack(side="left", padx=5)
        self.admin_mode_btn = tk.Button(self.mode_frame, text="관리자 모드", command=self.check_admin_password,
                                        font=("Malgun Gothic", 10), width=10)
        self.admin_mode_btn.pack(side="left")

        self.customer_frame = tk.Frame(self.master, bd=2, relief="groove", padx=10, pady=10)
        self.customer_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.drink_buttons_display_frame = tk.Frame(self.customer_frame)
        self.drink_buttons_display_frame.pack(pady=10, padx=10, fill="x")

        buttons_per_row = 10; button_width = 10; button_height = 4; font_size = 9

        for i, drink_obj in enumerate(self.drinks): # drink_obj는 Drink 객체
            row = i // buttons_per_row
            col = i % buttons_per_row
            
            price_str = f"{drink_obj.price:,}원" # 객체 속성 접근
            btn_text = f"{drink_obj.name}\n({price_str})" # 객체 속성 접근

            btn = tk.Button(self.drink_buttons_display_frame,
                            text=btn_text, width=button_width, height=button_height,
                            command=lambda d_id=drink_obj.id: self.purchase_drink(d_id), # 객체 속성 접근
                            font=("Malgun Gothic", font_size, "bold"), wraplength=button_width*8)
            btn.grid(row=row, column=col, padx=7, pady=7, sticky="nsew")
            self.drink_buttons[drink_obj.id] = btn # 객체 속성 접근
        
        for i in range(buttons_per_row):
            self.drink_buttons_display_frame.grid_columnconfigure(i, weight=1)

        self.transaction_frame = tk.Frame(self.customer_frame, bd=2, relief="flat", padx=10, pady=15)
        self.transaction_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(self.transaction_frame, text="금액 투입:", font=("Malgun Gothic", 12, "bold")).pack(side="left", padx=5)
        money_buttons_frame = tk.Frame(self.transaction_frame); money_buttons_frame.pack(side="left", padx=10)
        col_count = 0
        for key_str in self.bills.keys():
            money_value = self.convert_from(key_str)
            if money_value is not None:
                tk.Button(money_buttons_frame, text=key_str, width=7,
                          command=lambda current_value=money_value: self.insert_money(current_value),
                          font=("Malgun Gothic", 10)).grid(row=0, column=col_count, padx=3, pady=3)
                col_count += 1
        col_count = 0
        for key_str in self.coins.keys():
            money_value = self.convert_from(key_str)
            if money_value is not None:
                tk.Button(money_buttons_frame, text=key_str, width=7,
                          command=lambda current_value=money_value: self.insert_money(current_value),
                          font=("Malgun Gothic", 10)).grid(row=1, column=col_count, padx=3, pady=3)
                col_count +=1

        self.card_button = tk.Button(self.transaction_frame, text="카드 투입", 
                                     command=self.toggle_card, font=("Malgun Gothic", 10, "bold"), 
                                     bg="#4CAF50", fg="white", width=9, height=2, relief="raised", bd=2)
        self.card_button.pack(side="left", padx=15, pady=5)
        tk.Button(self.transaction_frame, text="잔돈\n반환", command=self.return_change, font=("Malgun Gothic", 12, "bold"),
                  bg="darkorange", fg="white", width=7, height=2, relief="raised", bd=3).pack(side="right", padx=20, pady=5)

        self.admin_frame = tk.Frame(self.master, bd=2, relief="groove", padx=10, pady=10)
        tk.Label(self.admin_frame, text="--- 관리자 모드 ---", font=("Malgun Gothic", 16, "bold"), fg="red").pack(pady=10)
        stock_canvas_frame = tk.Frame(self.admin_frame); stock_canvas_frame.pack(fill="x", pady=5)
        stock_canvas = tk.Canvas(stock_canvas_frame, borderwidth=0, height=250)
        stock_scrollbar = tk.Scrollbar(stock_canvas_frame, orient="vertical", command=stock_canvas.yview)
        self.scrollable_stock_frame = tk.Frame(stock_canvas)
        self.scrollable_stock_frame.bind("<Configure>", lambda e: stock_canvas.configure(scrollregion=stock_canvas.bbox("all")))
        stock_canvas.create_window((0, 0), window=self.scrollable_stock_frame, anchor="nw")
        stock_canvas.configure(yscrollcommand=stock_scrollbar.set)
        stock_canvas.pack(side="left", fill="x", expand=True); stock_scrollbar.pack(side="right", fill="y")
        for i, drink_obj in enumerate(self.drinks): # drink_obj는 Drink 객체
            item_frame = tk.Frame(self.scrollable_stock_frame); item_frame.pack(fill="x", pady=2)
            label_text = f"ID: {drink_obj.id}, 이름: {drink_obj.name[:15]:<15s} 현재 재고:" # 객체 속성 접근
            tk.Label(item_frame, text=label_text, font=("Malgun Gothic", 10)).pack(side="left", padx=5)
            entry = tk.Entry(item_frame, width=7, font=("Malgun Gothic", 10)); entry.pack(side="left", padx=5)
            entry.insert(0, str(drink_obj.stock)) # 객체 속성 접근
            self.stock_entries[drink_obj.id] = entry # 객체 속성 접근
        stock_btn_frame = tk.Frame(self.admin_frame); stock_btn_frame.pack(fill="x", pady=10)
        tk.Button(stock_btn_frame, text="재고 업데이트", command=self.update_stock, font=("Malgun Gothic", 10), bg="lightgray").pack(side="left", padx=10, expand=True, fill="x")
        tk.Button(stock_btn_frame, text="모든 음료 재고 10개로 보충", command=self.refill_all_drinks_to_10, font=("Malgun Gothic", 10), bg="lightgray").pack(side="left", padx=10, expand=True, fill="x")
        money_frame = tk.LabelFrame(self.admin_frame, text="금액 현황 (자판기 보유)", padx=10, pady=10, font=("Malgun Gothic", 11)); money_frame.pack(fill="x", pady=5)
        self.money_labels = {}; money_display_frame = tk.Frame(money_frame); money_display_frame.pack(fill="x")
        bill_label_frame = tk.Frame(money_display_frame); bill_label_frame.pack(side="left", padx=10, fill="y", anchor="n")
        tk.Label(bill_label_frame, text="지폐:", font=("Malgun Gothic", 10, "underline")).pack(anchor="w")
        for i, (bill, count) in enumerate(self.bills.items()):
            lbl = tk.Label(bill_label_frame, text=f"{bill}: {count}개", font=("Malgun Gothic", 10)); lbl.pack(anchor="w", padx=5, pady=1); self.money_labels[bill] = lbl
        coin_label_frame = tk.Frame(money_display_frame); coin_label_frame.pack(side="left", padx=10, fill="y", anchor="n")
        tk.Label(coin_label_frame, text="동전:", font=("Malgun Gothic", 10, "underline")).pack(anchor="w")
        for i, (coin, count) in enumerate(self.coins.items()):
            lbl = tk.Label(coin_label_frame, text=f"{coin}: {count}개", font=("Malgun Gothic", 10)); lbl.pack(anchor="w", padx=5, pady=1); self.money_labels[coin] = lbl
        money_btn_frame = tk.Frame(money_frame); money_btn_frame.pack(fill="x", pady=10)
        tk.Button(money_btn_frame, text="금액 수거", command=self.collect_money, font=("Malgun Gothic", 10), bg="lightgray").pack(side="left", padx=10, expand=True, fill="x")
        tk.Button(money_btn_frame, text="잔돈 보충 (각 동전 10개씩)", command=self.refill_change_coins, font=("Malgun Gothic", 10), bg="lightgray").pack(side="left", padx=10, expand=True, fill="x")
        self.profit_label = tk.Label(money_frame, text="총 수익: 0원", font=("Malgun Gothic", 14, "bold"), fg="purple"); self.profit_label.pack(pady=10)

    def toggle_card(self):
        self.card_inserted = not self.card_inserted
        if self.card_inserted:
            self.card = self.users_card        
        if self.card is None:
            self.card_button.config(text="카드 빼기", bg="#F44336")
            self.show_toast_message(f"카드가 투입되었습니다. 카드 잔액: {self.card.moeny:,}원", duration_ms=2000)
        else:
            self.card_button.config(text="카드 투입", bg="#4CAF50")
            self.show_toast_message("카드가 제거되었습니다.", duration_ms=1500)
        self.update_display()

    def update_display(self):
        self.deposit_label.config(text=f"투입 금액: {self.current_deposit:,}원")
        if self.card_inserted:
            self.card_status_label.config(text=f"카드 잔액: {self.card.moeny:,}원", fg="blue")
        else:
            self.card_status_label.config(text="카드 미사용", fg="#555555")

        for drink_id, button in self.drink_buttons.items():
            drink_obj = self.get_drink_by_id(drink_id) # Drink 객체 반환
            if not drink_obj:
                button.config(state="disabled", text="정보 없음", bg="gray")
                continue

            price_str = f"{drink_obj.price:,}원" # 객체 속성 접근
            btn_text = f"{drink_obj.name}\n({price_str})" # 객체 속성 접근
            
            can_purchase = False
            if self.card_inserted:
                can_purchase = self.card.moeny >= drink_obj.price # 객체 속성 접근
            else:
                can_purchase = self.current_deposit >= drink_obj.price # 객체 속성 접근

            if not drink_obj.is_in_stock(): # is_in_stock() 메서드 사용
                button.config(state="disabled", text=f"{drink_obj.name}\n(품절)", bg="#FF5733", fg="white") # 객체 속성 접근
            elif can_purchase:
                button.config(state="normal", text=btn_text, bg="#C7F0DB", fg="black")
            else:
                button.config(state="disabled", text=btn_text, bg="#E0E0E0", fg="#555555")
        
        if hasattr(self, 'money_labels') and self.admin_frame.winfo_ismapped():
            self.update_admin_money_display()

    def convert_to(self, amount):
        unit = self.money_unit_map.get(amount)
        if unit: return unit
        else: print(f"DEBUG: 유효하지 않은 금액 단위: {amount}"); return None

    def convert_from(self, key):
        reverse_map = {v: k for k, v in self.money_unit_map.items()}
        value = reverse_map.get(key)
        if value is not None: return value
        else: print(f"DEBUG: 유효하지 않은 금액 문자열: {key}"); return 0

    def insert_money(self, value):
        if self.card_inserted:
            self.show_toast_message("카드 사용 중에는 현금을 투입할 수 없습니다. 카드를 먼저 빼주세요.", duration_ms=2000, bg_color="orange")
            return
        key = self.convert_to(value)
        if key is None:
             messagebox.showerror("오류", f"{value:,}원은 유효하지 않은 금액 단위입니다.")
             return
        if key in self.coins: self.coins[key] += 1
        elif key in self.bills: self.bills[key] += 1
        else: messagebox.showerror("오류", "유효하지 않은 금액이 투입 시도되었습니다."); return
        self.current_deposit += value
        self.update_display()

    def refill_change_coins(self, amount=10):
        refilled_total_value = 0
        for coin_name in self.coins.keys():
            coin_value = self.convert_from(coin_name)
            if coin_value > 0 : self.coins[coin_name] += amount; refilled_total_value += coin_value * amount
        self.total_refilled_money += refilled_total_value
        self.show_toast_message(f"각 동전 잔돈이 {amount}개씩 보충. (총 {refilled_total_value:,}원)", duration_ms=2000)
        self.update_display()

    def refill_all_drinks_to_10(self):
        for drink_obj in self.drinks: # drink_obj는 Drink 객체
            drink_obj.stock = 10 # 객체 속성 직접 수정
        self.show_toast_message("모든 음료 재고 10개로 보충.", duration_ms=1500)
        self.update_display()
        if self.admin_frame.winfo_ismapped(): self.load_admin_data()

    def purchase_drink(self, drink_id):
        drink_obj = self.get_drink_by_id(drink_id) # Drink 객체 반환
        if not drink_obj:
            messagebox.showerror("오류", "알 수 없는 음료입니다.")
            return

        # is_in_stock() 메서드로 재고 확인
        if not drink_obj.is_in_stock():
            self.show_toast_message(f"{drink_obj.name} ({drink_obj.id})은(는) 품절입니다.", duration_ms=1500, bg_color="red")
            return

        if self.card_inserted: # 카드 결제
            if self.card.moeny < drink_obj.price:
                self.show_toast_message(f"카드 잔액이 부족합니다. (잔액: {self.card.moeny:,}원)", duration_ms=2000, bg_color="orange")
                return
            self.card.moeny -= drink_obj.price
            drink_obj.decrease_stock() # decrease_stock() 메서드 사용
            self.total_collected_money += drink_obj.price 
            self.show_toast_message(f"{drink_obj.name} 카드로 구매 완료! (카드 잔액: {self.card.moeny:,}원)", duration_ms=2000, bg_color="blue")
        else: # 현금 결제
            if self.current_deposit < drink_obj.price:
                self.show_toast_message("투입 금액이 부족합니다.", duration_ms=1500, bg_color="orange")
                return
            self.current_deposit -= drink_obj.price
            drink_obj.decrease_stock() # decrease_stock() 메서드 사용
            self.show_toast_message(f"{drink_obj.name} 구매 완료! 맛있게 드세요!", duration_ms=1800, bg_color="green")
        
        self.update_display()

    def return_change(self): # 잔돈 반환 함수 
        if self.current_deposit == 0:
            self.show_toast_message("반환할 현금이 없습니다.", duration_ms=1500)
            return
        change_to_return = self.current_deposit
        change_breakdown = self.calculate_change(change_to_return)
        if change_breakdown is None:
            self.show_toast_message("자판기 현금 잔돈 부족! 관리자에게 문의하세요.", duration_ms=2000, bg_color="red")
            return
        change_msg_parts = []
        actual_returned_amount = 0
        for coin_name, count in change_breakdown.items():
            if count > 0:
                change_msg_parts.append(f"{coin_name} {count}개")
                self.coins[coin_name] -= count
                actual_returned_amount += self.convert_from(coin_name) * count
        if not change_msg_parts and change_to_return > 0 :
             self.show_toast_message(f"{change_to_return:,}원을 반환하기 위한 정확한 동전이 부족합니다.", duration_ms=2500, bg_color="orange")
             return
        if actual_returned_amount != change_to_return :
             self.show_toast_message(f"잔돈 계산 오류! 관리자 확인 필요. (요청:{change_to_return:,}, 계산:{actual_returned_amount:,})", duration_ms=3000, bg_color="red")
             return
        change_msg = "현금 잔돈 반환: " + ", ".join(change_msg_parts)
        self.show_toast_message(change_msg, duration_ms=2500)
        self.current_deposit = 0
        self.update_display()
        if self.admin_frame.winfo_ismapped(): self.update_admin_money_display()

    def calculate_change(self, amount):
        change_details = {}; temp_coins_stock = self.coins.copy()
        for coin_name_key, coin_value in sorted([(k, self.convert_from(k)) for k in self.coins.keys()], key=lambda x: x[1], reverse=True):
            if coin_value == 0: continue
            num_to_give = min(amount // coin_value, temp_coins_stock[coin_name_key])
            if num_to_give > 0:
                change_details[coin_name_key] = num_to_give; amount -= num_to_give * coin_value
                temp_coins_stock[coin_name_key] -= num_to_give
        if amount == 0: return change_details
        else: return None
        
    def switch_to_customer_mode(self):
        self.admin_frame.pack_forget()
        self.customer_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.update_display()

    def check_admin_password(self):
        password = simpledialog.askstring("관리자 모드", "비밀번호를 입력하세요:", show='*', parent=self.master)
        if password == self.admin_password: self.switch_to_admin_mode()
        elif password is not None: messagebox.showerror("오류", "잘못된 비밀번호입니다.", parent=self.master)

    def switch_to_admin_mode(self):
        self.customer_frame.pack_forget()
        self.admin_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.load_admin_data(); self.update_display()

    def load_admin_data(self):
        for drink_id, entry in self.stock_entries.items():
            drink_obj = self.get_drink_by_id(drink_id) # Drink 객체 반환
            if drink_obj:
                entry.delete(0, tk.END)
                entry.insert(0, str(drink_obj.stock)) # 객체 속성 접근
            else:
                entry.delete(0, tk.END)
                entry.insert(0, "N/A")
        self.update_admin_money_display()

    def update_admin_money_display(self):
        if not hasattr(self, 'money_labels'): return
        for coin, count in self.coins.items():
            if coin in self.money_labels: self.money_labels[coin].config(text=f"{coin}: {count}개")
        for bill, count in self.bills.items():
            if bill in self.money_labels: self.money_labels[bill].config(text=f"{bill}: {count}개")
        current_profit = self.profit()
        self.profit_label.config(text=f"총 수익: {current_profit:,}원")
        if current_profit >= 0: self.profit_label.config(fg="green")
        else: self.profit_label.config(fg="red")

    def update_stock(self):
        try:
            for drink_id, entry in self.stock_entries.items():
                new_stock_str = entry.get()
                drink_obj = self.get_drink_by_id(drink_id) # Drink 객체 가져오기
                if not drink_obj: continue # 해당 ID의 음료가 없으면 스킵

                if not new_stock_str.isdigit(): raise ValueError(f"{drink_obj.name}(ID:{drink_obj.id}) 재고 숫자여야 함.")
                new_stock = int(new_stock_str)
                if new_stock < 0: raise ValueError("재고는 0보다 작을 수 없음.")
                drink_obj.stock = new_stock # 객체 속성 직접 수정
            self.show_toast_message("재고 업데이트 완료.", duration_ms=1500)
            self.update_display(); self.load_admin_data()
        except ValueError as e: messagebox.showerror("오류", f"유효하지 않은 재고 값: {e}", parent=self.master)

    def collect_money(self):
        collected_this_time = 0
        for coin_name, count in self.coins.items():
            coin_value = self.convert_from(coin_name)
            if coin_value > 0: collected_this_time += coin_value * count; self.coins[coin_name] = 0
        for bill_name, count in self.bills.items():
            bill_value = self.convert_from(bill_name)
            if bill_value > 0: collected_this_time += bill_value * count; self.bills[bill_name] = 0
        # 카드 판매액은 이미 purchase_drink에서 self.total_collected_money에 반영되었으므로,
        # 여기서는 현금 수거액만 self.total_collected_money에 더하는 것이 아니라,
        # 현금으로 투입되어 아직 수익으로 잡히지 않은 금액을 반영하는 개념으로 이해해야 합니다.
        # 현재 구조에서는 현금 투입(current_deposit) -> 구매 시 차감 -> 남은 금액 반환 or 수거 시 수익.
        # collect_money는 자판기 내 "현금"을 수거하는 것이므로, collected_this_time을
        # total_collected_money에 더하는 기존 로직이 맞습니다.
        # (단, purchase_drink에서 현금 구매 시 total_collected_money를 즉시 올리지 않았다는 가정 하에)
        # 만약 purchase_drink에서 현금 구매 시에도 total_collected_money를 올렸다면, 여기서 중복됩니다.
        # 현재 코드는 purchase_drink 현금 구매 시 total_collected_money를 직접 올리지 않으므로, 아래 로직 유지.
        self.total_collected_money += collected_this_time
        self.show_toast_message(f"총 {collected_this_time:,}원 수거. (누적 수익 업데이트됨)", duration_ms=2000)
        self.update_admin_money_display(); self.update_display()

    def show_toast_message(self, message, duration_ms=2000, bg_color="black", fg_color="white"):
        if self.toast_window is not None:
            if self.toast_timer_id: self.master.after_cancel(self.toast_timer_id)
            self.toast_label.config(text=message, bg=bg_color, fg=fg_color)
            self.update_toast_position(self.toast_window); self.toast_window.lift()
        else:
            self.toast_window = tk.Toplevel(self.master); self.toast_window.overrideredirect(True)
            self.toast_label = tk.Label(self.toast_window, text=message, bg=bg_color, fg=fg_color, font=("Malgun Gothic", 10), padx=10, pady=5)
            self.toast_label.pack(expand=True, fill="both"); self.update_toast_position(self.toast_window)
        self.toast_timer_id = self.master.after(duration_ms, self._destroy_toast)

    def update_toast_position(self, toast_win):
        toast_win.update_idletasks()
        master_x = self.master.winfo_x(); master_y = self.master.winfo_y()
        master_width = self.master.winfo_width(); master_height = self.master.winfo_height()
        toast_width = toast_win.winfo_width(); toast_height = toast_win.winfo_height()
        x = master_x + master_width - toast_width - 20; y = master_y + master_height - toast_height - 20
        toast_win.geometry(f"+{x}+{y}")

    def _destroy_toast(self):
        if self.toast_window:
            self.toast_window.destroy()
            self.toast_window = None; self.toast_label = None; self.toast_timer_id = None

if __name__ == "__main__":
    root = tk.Tk()
    app = VendingMachineApp(root)
    root.mainloop()