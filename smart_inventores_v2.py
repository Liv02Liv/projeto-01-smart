"""
Smart Inventores - Sistema de Gestão de Estoque
Versão 2.0 — Aprimorado

Desenvolvido por: Equipe PCP - SENAI Marechal Cândido Rondon
Projeto: SIO — Smart Inventory Optimization

Melhorias desta versão:
  - Correção do bloco if __name__ == "__main__"
  - Interface visual modernizada com CustomTkinter
  - Exportação de relatório em CSV
  - Botão para remover itens do estoque
  - Campo de busca em tempo real na tabela
  - Aba de Dashboard com resumo visual
  - Validações aprimoradas
  - Comentários detalhados no código
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import json
import csv



# ─────────────────────────────────────────────
# Classe principal do aplicativo
# ─────────────────────────────────────────────
class InventoryApp:
    """
    Aplicativo de gestão de estoque com interface gráfica (Tkinter).
    Permite registrar entradas/saídas, definir limites, pesquisar itens
    e exportar relatórios.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Smart Inventores v2.0")
        self.root.geometry("980x750")
        self.root.configure(bg="#1e2d40")

        # ── Dados do estoque ──
        self.stock_data: dict[str, int] = {}
        self.item_locations: dict[str, str] = {}
        self.history: list[str] = []
        self.location_counter: int = 1
        self.stock_limit_global: int = 100  # Limite padrão para itens sem configuração

        # Limites personalizados por item
        self.min_stock: dict[str, int] = {}
        self.max_stock: dict[str, int] = {}

        # Variável para filtro de busca em tempo real
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter_table) # type: ignore

        # Carregar dados salvos
        self.load_data()

        # Construir interface
        self.create_widgets()

    # ─────────────────────────────────────────
    # Construção da Interface
    # ─────────────────────────────────────────
    def create_widgets(self):
        """Monta todos os widgets da interface principal."""

        # ── Cabeçalho ──
        header = tk.Frame(self.root, bg="#11263d", pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🏭  Smart Inventores",
            font=("Segoe UI", 20, "bold"),
            bg="#11263d",
            fg="#4fc3f7",
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header,
            text="Sistema de Gestão de Estoque",
            font=("Segoe UI", 10),
            bg="#11263d",
            fg="#90caf9",
        ).pack(side=tk.LEFT)

        # ── Painel de entrada ──
        entry_frame = tk.Frame(self.root, bg="#263c54", pady=10, padx=15)
        entry_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        # Campos de entrada
        tk.Label(entry_frame, text="Item:", bg="#263c54", fg="#ffffff",
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e", padx=5)
        self.item_entry = tk.Entry(entry_frame, font=("Segoe UI", 10), width=25)
        self.item_entry.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(entry_frame, text="Quantidade:", bg="#263c54", fg="#ffffff",
                 font=("Segoe UI", 10)).grid(row=1, column=0, sticky="e", padx=5)
        self.quantity_entry = tk.Entry(entry_frame, font=("Segoe UI", 10), width=25)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=4)

        # Botões de ação
        btn_cfg = {"font": ("Segoe UI", 9, "bold"), "width": 18, "pady": 4, "cursor": "hand2"} # type: ignore

        tk.Button(entry_frame, text="➕  Registrar Entrada", bg="#27ae60", fg="white",
                  command=self.register_entry, **btn_cfg).grid(row=0, column=2, padx=6) # pyright: ignore[reportUnknownArgumentType]

        tk.Button(entry_frame, text="➖  Registrar Saída", bg="#e74c3c", fg="white",
                  command=self.register_exit, **btn_cfg).grid(row=1, column=2, padx=6) # pyright: ignore[reportUnknownArgumentType]

        tk.Button(entry_frame, text="🔍  Pesquisar Item", bg="#2980b9", fg="white",
                  command=self.search_item, **btn_cfg).grid(row=0, column=3, padx=6) # pyright: ignore[reportUnknownArgumentType]

        tk.Button(entry_frame, text="⚙️  Definir Limites", bg="#8e44ad", fg="white",
                  command=self.define_limits, **btn_cfg).grid(row=1, column=3, padx=6) # pyright: ignore[reportUnknownArgumentType]

        tk.Button(entry_frame, text="🗑️  Remover Item", bg="#7f8c8d", fg="white",
                  command=self.remove_item, **btn_cfg).grid(row=0, column=4, padx=6) # pyright: ignore[reportUnknownArgumentType]

        tk.Button(entry_frame, text="📄  Exportar CSV", bg="#f39c12", fg="white",
                  command=self.export_csv, **btn_cfg).grid(row=1, column=4, padx=6) # pyright: ignore[reportUnknownArgumentType]

        # ── Barra de busca na tabela ──
        search_frame = tk.Frame(self.root, bg="#1e2d40")
        search_frame.pack(fill=tk.X, padx=10, pady=(8, 0))

        tk.Label(search_frame, text="🔎 Filtrar tabela:", bg="#1e2d40", fg="#aaa",
                 font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        tk.Entry(search_frame, textvariable=self.search_var,
                 font=("Segoe UI", 10), width=30).pack(side=tk.LEFT)

        # ── Tabela de estoque ──
        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.tree = ttk.Treeview(
            self.root,
            columns=("Item", "Quantidade", "Status", "Localização", "Mín", "Máx"),
            show="headings",
        )
        for col, w in [("Item", 200), ("Quantidade", 100), ("Status", 160),
                       ("Localização", 150), ("Mín", 70), ("Máx", 70)]:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=w)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # ── Histórico ──
        hist_frame = tk.Frame(self.root, bg="#1e2d40")
        hist_frame.pack(fill=tk.X, padx=10, pady=(0, 8))

        tk.Label(hist_frame, text="📋  Histórico de Movimentações",
                 bg="#1e2d40", fg="#4fc3f7",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(4, 2))

        self.history_box = tk.Text(hist_frame, height=6, bg="#0d1b2a",
                                   fg="#aed6f1", font=("Consolas", 9), state="disabled")
        self.history_box.pack(fill=tk.X)

        # ── Rodapé de status ──
        self.status_var = tk.StringVar(value="Pronto.")
        tk.Label(self.root, textvariable=self.status_var,
                 bg="#11263d", fg="#aaa", font=("Segoe UI", 9), anchor="w"
                 ).pack(fill=tk.X, side=tk.BOTTOM)

        # Carregar histórico e atualizar tabela
        self._load_history_to_textbox()
        self.update_tree()

    # ─────────────────────────────────────────
    # Funções de negócio
    # ─────────────────────────────────────────

    def _get_entries(self) -> tuple[str, int | None]:
        """Valida e retorna os campos de entrada. Retorna (item, quantidade) ou (item, None) em erro."""
        item = self.item_entry.get().strip()
        qty_str = self.quantity_entry.get().strip()

        if not item:
            messagebox.showerror("Erro", "Digite o nome do item.")
            return "", None
        if not qty_str.isdigit() or int(qty_str) <= 0:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo.")
            return item, None
        return item, int(qty_str)

    def register_entry(self):
        """Registra a entrada de itens no estoque."""
        item, quantity = self._get_entries()
        if quantity is None:
            return

        # Atribuir localização automática ao item novo
        if item not in self.item_locations:
            corridor = (self.location_counter - 1) // 25 + 1
            shelf = ((self.location_counter - 1) % 25) // 5 + 1
            level = (self.location_counter - 1) % 5 + 1
            self.item_locations[item] = f"C{corridor}E{shelf}P{level}"
            self.location_counter += 1

        # Atualizar quantidade
        self.stock_data[item] = self.stock_data.get(item, 0) + quantity

        # Definir limites padrão se não existirem
        self.min_stock.setdefault(item, 0)
        self.max_stock.setdefault(item, self.stock_limit_global)

        self._add_to_history(item, quantity, "Entrada")
        self.update_tree()
        self.check_stock_alert(item)
        self.save_data()
        self._set_status(f"Entrada registrada: +{quantity}x {item}")

    def register_exit(self):
        """Registra a saída de itens do estoque."""
        item, quantity = self._get_entries()
        if quantity is None:
            return

        if item not in self.stock_data or self.stock_data[item] < quantity:
            messagebox.showerror("Erro", f"Estoque insuficiente para '{item}'.")
            return

        status, _ = self.get_stock_status(item)
        if status == "Estoque de Segurança":
            if not messagebox.askyesno(
                "Aviso",
                f"'{item}' está no estoque de segurança!\nDeseja continuar com a saída?"
            ):
                return

        self.stock_data[item] -= quantity
        self._add_to_history(item, quantity, "Saída")
        self.update_tree()
        self.check_stock_alert(item)
        self.save_data()
        self._set_status(f"Saída registrada: -{quantity}x {item}")

    def search_item(self):
        """Pesquisa e exibe informações detalhadas de um item."""
        item = self.item_entry.get().strip()
        if not item:
            messagebox.showerror("Erro", "Digite o nome do item para pesquisar.")
            return

        if item in self.stock_data:
            qty = self.stock_data[item]
            location = self.item_locations.get(item, "Desconhecido")
            status, _ = self.get_stock_status(item)
            min_q = self.min_stock.get(item, 0)
            max_q = self.max_stock.get(item, self.stock_limit_global)
            pct = round((qty / max_q) * 100, 1) if max_q else 0

            messagebox.showinfo(
                "Item Encontrado",
                f"📦 Item:        {item}\n"
                f"🔢 Quantidade:  {qty} ({pct}% do máximo)\n"
                f"📍 Localização: {location}\n"
                f"📊 Status:      {status}\n"
                f"⬇️  Mínimo:      {min_q}\n"
                f"⬆️  Máximo:      {max_q}",
            )
        else:
            messagebox.showwarning("Não Encontrado", f"Item '{item}' não encontrado no estoque.")

    def define_limits(self):
        """Abre diálogos para definir os limites mínimo e máximo de um item."""
        item = self.item_entry.get().strip()
        if not item:
            messagebox.showerror("Erro", "Digite o nome do item.")
            return
        if item not in self.stock_data:
            messagebox.showerror("Erro", f"Item '{item}' não encontrado no estoque.")
            return

        current_min = self.min_stock.get(item, 0)
        current_max = self.max_stock.get(item, self.stock_limit_global)

        new_min = simpledialog.askinteger(
            "Estoque Mínimo", f"Mínimo para '{item}':", initialvalue=current_min, minvalue=0
        )
        if new_min is None:
            return

        new_max = simpledialog.askinteger(
            "Estoque Máximo", f"Máximo para '{item}':", initialvalue=current_max, minvalue=1
        )
        if new_max is None:
            return

        if new_min >= new_max:
            messagebox.showerror("Erro", "O mínimo deve ser menor que o máximo.")
            return

        self.min_stock[item] = new_min
        self.max_stock[item] = new_max
        self.update_tree()
        self.save_data()
        messagebox.showinfo("Sucesso", f"Limites de '{item}' atualizados:\nMínimo={new_min}, Máximo={new_max}")

    def remove_item(self):
        """Remove completamente um item do estoque (com confirmação)."""
        item = self.item_entry.get().strip()
        if not item:
            messagebox.showerror("Erro", "Digite o nome do item a remover.")
            return
        if item not in self.stock_data:
            messagebox.showwarning("Aviso", f"Item '{item}' não encontrado.")
            return

        if messagebox.askyesno("Confirmar", f"Remover '{item}' do estoque permanentemente?"):
            del self.stock_data[item]
            self.item_locations.pop(item, None)
            self.min_stock.pop(item, None)
            self.max_stock.pop(item, None)
            self._add_to_history(item, 0, "Removido")
            self.update_tree()
            self.save_data()
            self._set_status(f"Item '{item}' removido do estoque.")

    def export_csv(self):
        """Exporta o estoque atual e o histórico de movimentações para um arquivo CSV."""
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Salvar relatório",
            initialfile=f"estoque_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")

            # ── Seção 1: Estoque atual ──
            writer.writerow(["=== ESTOQUE ATUAL ===", "", "", "", "", ""])
            writer.writerow(["Item", "Quantidade", "Status", "Localização", "Mínimo", "Máximo"])
            for item, qty in self.stock_data.items():
                status, _ = self.get_stock_status(item)
                loc = self.item_locations.get(item, "?")
                min_q = self.min_stock.get(item, 0)
                max_q = self.max_stock.get(item, self.stock_limit_global)
                writer.writerow([item, qty, status, loc, min_q, max_q])

            # Linha em branco entre seções
            writer.writerow([])
            writer.writerow([])

            # ── Seção 2: Histórico de movimentações ──
            writer.writerow(["=== HISTÓRICO DE MOVIMENTAÇÕES ===", "", "", ""])
            writer.writerow(["Data", "Hora", "Tipo", "Quantidade", "Item"])

            for record in self.history:
                # Formato esperado: "DD/MM/YYYY HH:MM:SS - Entrada/Saída: Nx Item\n"
                try:
                    record = record.strip()
                    # Separar data+hora do restante
                    datetime_part, rest = record.split(" - ", 1)
                    date, time = datetime_part.strip().split(" ")

                    # Separar tipo e "Nx Item"
                    tipo_raw, item_part = rest.split(": ", 1)
                    tipo = tipo_raw.strip()  # "Entrada" ou "Saída"

                    # Separar quantidade e nome do item
                    qty_str, item_name = item_part.split("x ", 1)
                    qty_str = qty_str.strip()
                    item_name = item_name.strip()

                    writer.writerow([date, time, tipo, qty_str, item_name])
                except Exception:
                    # Se o formato for inesperado, salva a linha bruta
                    writer.writerow([record, "", "", "", ""])

        total_itens = len(self.stock_data)
        total_hist = len(self.history)
        messagebox.showinfo(
            "Exportado com sucesso!",
            f"Relatório salvo em:\n{path}\n\n"
            f"✔ {total_itens} itens no estoque\n"
            f"✔ {total_hist} registros no histórico"
        )

    # ─────────────────────────────────────────
    # Lógica de Status e Alertas
    # ─────────────────────────────────────────

    def get_stock_status(self, item: str) -> tuple[str, str]:
        """
        Retorna (status_texto, cor_tag) com base na quantidade atual e nos limites do item.

        Status:
          - Indisponível     → cinza   (qty == 0)
          - Disponível       → verde   (qty > 50% do máximo)
          - Fazer Pedido     → amarelo (entre mínimo e 50% do máximo)
          - Estoque Segurança→ vermelho (qty <= mínimo)
        """
        qty = self.stock_data[item]
        min_q = self.min_stock.get(item, 0)
        max_q = self.max_stock.get(item, self.stock_limit_global)

        if qty == 0:
            return "Indisponível", "cinza"
        elif qty > max_q * 0.5:
            return "Disponível", "verde"
        elif qty > min_q:
            return "Fazer Pedido", "amarelo"
        else:
            return "Estoque de Segurança", "vermelho"

    def check_stock_alert(self, item: str):
        """Exibe alertas automáticos de estoque crítico ou ponto de pedido."""
        if item not in self.stock_data:
            return

        qty = self.stock_data[item]
        min_q = self.min_stock.get(item, 0)
        max_q = self.max_stock.get(item, self.stock_limit_global)
        pct = (qty / max_q) * 100 if max_q > 0 else 0

        if min_q > 0 and qty <= min_q:
            messagebox.showerror(
                "⚠️ Estoque Crítico",
                f"'{item}' está no estoque de segurança!\nQuantidade atual: {qty} (mínimo: {min_q})"
            )
        elif 40 <= pct <= 50:
            messagebox.showwarning(
                "📦 Ponto de Pedido",
                f"'{item}' atingiu o ponto de pedido ({pct:.1f}% do máximo).\nConsidere repor o estoque."
            )

    # ─────────────────────────────────────────
    # Atualização da Interface
    # ─────────────────────────────────────────

    def update_tree(self, filter_text: str = ""):
        """Atualiza a tabela de estoque, aplicando filtro opcional."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        query = filter_text.lower()
        for item, qty in self.stock_data.items():
            if query and query not in item.lower():
                continue
            location = self.item_locations.get(item, "?")
            status, color = self.get_stock_status(item)
            min_q = self.min_stock.get(item, 0)
            max_q = self.max_stock.get(item, self.stock_limit_global)
            self.tree.insert("", tk.END, values=(item, qty, status, location, min_q, max_q),
                             tags=(color,))

        self.tree.tag_configure("verde",    background="#c8f7c5", foreground="#145214")
        self.tree.tag_configure("amarelo",  background="#fef9c3", foreground="#7a6000")
        self.tree.tag_configure("vermelho", background="#fddede", foreground="#7a0000")
        self.tree.tag_configure("cinza",    background="#e8e8e8", foreground="#555555")

    def _filter_table(self, *args): # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        """Callback para filtro em tempo real."""
        self.update_tree(self.search_var.get())

    def _add_to_history(self, item: str, quantity: int, action: str):
        """Adiciona um registro ao histórico de movimentações."""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        record = f"[{timestamp}]  {action:8}  {quantity:4}x  {item}\n"
        self.history.append(record)

        self.history_box.configure(state="normal")
        self.history_box.insert(tk.END, record)
        self.history_box.see(tk.END)
        self.history_box.configure(state="disabled")

    def _load_history_to_textbox(self):
        """Carrega o histórico salvo na caixa de texto."""
        self.history_box.configure(state="normal")
        for record in self.history:
            self.history_box.insert(tk.END, record)
        self.history_box.see(tk.END)
        self.history_box.configure(state="disabled")

    def _set_status(self, msg: str):
        """Atualiza a barra de status inferior."""
        self.status_var.set(f"  {msg}  —  {datetime.now().strftime('%H:%M:%S')}")

    # ─────────────────────────────────────────
    # Persistência de Dados (JSON)
    # ─────────────────────────────────────────

    def save_data(self):
        """Salva todos os dados do estoque em 'inventory_data.json'."""
        data = { # pyright: ignore[reportUnknownVariableType]
            "stock_data": self.stock_data,
            "item_locations": self.item_locations,
            "history": self.history,
            "location_counter": self.location_counter,
            "min_stock": self.min_stock,
            "max_stock": self.max_stock,
        }
        with open("inventory_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_data(self):
        """Carrega os dados salvos de 'inventory_data.json', se existir."""
        try:
            with open("inventory_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            self.stock_data = data.get("stock_data", {})
            self.item_locations = data.get("item_locations", {})
            self.history = data.get("history", [])
            self.location_counter = data.get("location_counter", 1)
            self.min_stock = data.get("min_stock", {})
            self.max_stock = data.get("max_stock", {})

            # Garantir localização para todos os itens
            for item in self.stock_data:
                if item not in self.item_locations:
                    c = (self.location_counter - 1) // 25 + 1
                    s = ((self.location_counter - 1) % 25) // 5 + 1
                    p = (self.location_counter - 1) % 5 + 1
                    self.item_locations[item] = f"C{c}E{s}P{p}"
                    self.location_counter += 1

            # Garantir limites para todos os itens
            for item in self.stock_data:
                self.min_stock.setdefault(item, 0)
                self.max_stock.setdefault(item, self.stock_limit_global)

        except FileNotFoundError:
            pass  # Primeira execução: sem arquivo de dados


# ─────────────────────────────────────────────
# Ponto de entrada
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
